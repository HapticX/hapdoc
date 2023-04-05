# -*- coding: utf-8 -*-
"""
Describes JavaScript file type
"""
from re import findall, compile, sub, split, Pattern, IGNORECASE, MULTILINE

from ..abc import ABCFileType


class JavaScript(ABCFileType):
    """
    Provides JavaScript to Markdown translator
    """
    class_pattern = compile(
        r'(^ */\*+\n((\s*\*)([^\n]*\n))+)?(\s*)class +\b([\w\d]+) *{([\s\S]+?(?<!\w))^\5}',
        MULTILINE or IGNORECASE
    )
    strip_new_lines = compile(
        r'(\A\s*|\s*\Z)', MULTILINE or IGNORECASE
    )
    left_strip_lines = compile(
        r'^ *( \*)', MULTILINE or IGNORECASE
    )
    args_sep = compile(
        r'\s*,\s*', MULTILINE or IGNORECASE
    )
    method_pattern = compile(
        r'(^ */\*+\n((\s*\*)([^\n]*\n))+)?(\s*)'
        r'(function |\s*)([\w\d]+)\s*\(([\s\S]*?)\)'
        r'\s*{(\s+)([\s\S]+?)\9}',
        MULTILINE or IGNORECASE
    )
    func_pattern = compile(
        r'(^ */\*+\n((\s*\*)([^\n]*\n))+)?(\s*)'
        r'^(function +)([\w\d]+)\s*\(([\s\S]*?)\)'
        r'\s*{(\s+)([\s\S]+?)}',
        MULTILINE or IGNORECASE
    )

    @staticmethod
    def process_functions(source: str, pattern: Pattern) -> str:
        result = ''
        for func in findall(pattern, source):
            print(func)
            _comment, _, _, _, _, _, _name, _args, _, _data = func
            _comment = sub(JavaScript.left_strip_lines, r'\1', _comment)
            _args = split(JavaScript.args_sep, _args)
            _args_data = []
            for arg in _args:
                if not arg:
                    continue
                arg_data = arg
                if param := findall(r'@param *{([^}]+?)} *' + arg, _comment):
                    arg_data += f': {param[0].lower()}'
                _args_data.append(arg_data)
            _args_data = ', '.join(_args_data)
            return_type = findall(r'@returns? *{([^}]+?)}', _comment)
            return_type = f' -> {return_type[0].lower()}' if return_type else ''
            result += f'\n```javascript\n{_comment}function {_name}({_args_data}){return_type}\n```\n\n'
        return result

    @staticmethod
    def process(cls, filepath: str, output: str = 'docs', one_file: bool = False):
        source, end_path, filename = cls.pre(filepath, output, one_file)

        data = f'# {filename}\n\n'
        description = findall(compile(r'^/\*\*([\s\S]+?)\*/', MULTILINE), source)[0]
        description = sub(compile(r'(\A *| *\Z|^ *)', MULTILINE or IGNORECASE), '', description)
        data += f'{description}\n\n'
        data += '## Classes\n'

        for class_data in findall(cls.class_pattern, source):
            _comment, _, _, _, _, _name, _data = class_data
            text = f'\n### {_name}\n'
            _comment = sub(cls.left_strip_lines, r'\1', _comment)
            text += "#### Methods\n"
            text += cls.process_functions(_data, cls.method_pattern)
            # If methods does not found
            if text.endswith('#### Methods\n'):
                text = text[:-13]
            data += text
        if data.endswith('## Classes\n'):
            data = data[:-11]

        data += "\n\n### Functions\n"
        data += cls.process_functions(source, cls.func_pattern)
        # If methods does not found
        if data.endswith('### Functions\n'):
            data = data[:-15]

        with open(end_path, 'w', encoding='utf-8') as file:
            file.write(data)
