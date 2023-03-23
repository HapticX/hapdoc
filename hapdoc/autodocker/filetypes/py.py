# -*- coding: utf-8 -*-
"""
Describes Python file type
"""
from re import findall, sub, MULTILINE

from ..abc import ABCFileType


class Py(ABCFileType):
    """
    Provides Python file type behavior
    """

    @staticmethod
    def process_funcs(
            functions: list[tuple[str, str, str, str, str, str, str, str]]
    ) -> str:
        """
        Process functions and methods in .py files

        :param source: source python file
        :param functions: list of parsed functions (via regex)
        :return: md formatted string
        """
        methods_text = []
        for method in functions:
            decorator, _, is_async, name, arguments, return_type, _, docs = method
            # description
            description = findall(r'\s*([^:]+)', docs)
            description = description[0].rstrip(' \n') if description else ''
            # decorators
            decorators = [i.strip() for i in decorator.split('@')[1:]] if decorator else []
            # return type
            return_type = findall(r'->\s*([^:]+):', return_type)
            return_type = f' -> {return_type[0]}' if return_type else ''
            # arguments
            arguments = arguments[1:-1]
            arguments_typed = sub(r'\s+', r' ', arguments).split(',')
            arguments_typed = list(filter(lambda x: bool(x[0]), [
                (
                    i.split(':', 1)[0].strip(),
                    i.split(':', 1)[1].split('=')[0].strip() if ':' in i else '',
                    i.split('=', 1)[1].strip() if '=' in i else ''
                ) for i in arguments_typed
            ]))
            arguments = []
            for arg in arguments_typed:
                arg_name, arg_type, default_value = arg
                arg_desc = findall(r':param\s+' + arg_name.strip() + r'\s*:\s+([^\n]+)', docs)
                arguments.append({
                    'name': arg_name,
                    'desc': arg_desc[0].strip() if arg_desc else '',
                    'text': f'{arg_name}: {arg_type} = {default_value}'
                    if default_value else f'{arg_name}: {arg_type}'
                    if arg_type else arg_name
                })
            arguments_text = ",\n    ".join([i["text"] for i in arguments])
            params = '\n- '.join([f'`{i["name"]}` - {i["desc"]}' for i in arguments if i['desc']])
            params = f'\n- {params}' if params else ''
            decorator_text = '\n@'.join(decorators)
            decorator_text = f'@{decorator_text}\n' if decorators else ''
            arguments_text = f'\n    {arguments_text}\n' if arguments_text else ''
            methods_text.append(
                f'\n```python\n{decorator_text}{is_async}def '
                f'{name}({arguments_text}){return_type}:\n```'
                f'\n{description}\n{params}\n')
        return '\n___\n'.join(methods_text)

    @staticmethod
    def process(
            filepath: str,
            output: str = 'docs',
            one_file: bool = False
    ):
        """
        Translates python script into md file.

        :param filepath: path to python script
        :param output: output directory
        :param one_file: True when file flag is True
        :return:
        """
        source, end_path, filename = Py.pre(filepath, output, one_file)
        data = f'# {filename}\n'

        description = findall(r'^"{3}\s*([\s\S]+?)\s*"{3}', source, MULTILINE)
        if description:
            data += f'\n> {description[0].strip()}'

        # Handle classes
        classes = findall(r'(class +([^:]+):\n(\s+)[^\n]+(\n+\3[ \S]*)+)', source)
        classes_text = []
        for class_data in classes:
            class_code = class_data[0]
            name = findall(r'class +(\w+)', class_code)[0]
            doc = findall(r'class[^\n]+\s+"{3}\s*([\s\S]+?)"{3}', class_code)
            doc = f'> {doc[0]}' if doc else ''
            class_text = f'\n### `{name}`\n{doc}'
            # Handle class methods
            methods = findall(
                r"^\s*((@[\S]+\(\)|@[\S]+\([\S\s]+?\)|\s*|@[\S]+\s*)+)?"
                r"\s+(async +)?def +([^_][^\s(]+)(\(\)|\([\s\S]+?\))(\s*->\s*[^:]+:|\s*:)"
                r"\s+(\"{3}([\s\S]+?)\"{3})?",
                class_code,
                MULTILINE
            )
            class_text += '\n#### methods'
            class_text += Py.process_funcs(methods)
            classes_text.append(class_text)
        # write classes data
        if classes_text:
            class_text = '\n'.join(classes_text)
            data += f'\n## Classes\n{class_text}'

        # Handle functions
        functions = findall(
            r'^((@[\S]+\s*\(\)\s*|@[\S]+\s*\([\s\S]+?\)\s*|@[\S]+\s*)+)?\s+'
            r'^(async +)?def +([^_][^\s(]+)(\(\)|\([\s\S]+?\))(\s*->\s*[^:]+:|\s*:)'
            r'\s+(\"{3}([\s\S]+?)\"{3})?',
            source,
            MULTILINE
        )
        if functions:
            data += f'\n### Functions\n{Py.process_funcs(functions)}'

        with open(end_path, 'w', encoding='utf-8') as f:
            f.write(data)
