# -*- coding: utf-8 -*-
"""
Describes all FileTypes
"""
from re import findall, sub

from .abc import ABCFileType


class Py(ABCFileType):
    """
    Provides Python script translator behavior
    """

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

        description = findall(r'[^ \r\t]"{3}\s*([\s\S]+?)\s*"{3}', source)
        if description:
            data += f'\n> {description[0].strip()}'

        classes = findall(r'(class +([^:]+):\n(\s+)[^\n]+(\n+\3[ \S]*)+)', source)
        classes_text = []
        for c in classes:
            class_code = c[0]
            name = findall(r'class +(\w+)', class_code)[0]
            doc = findall(r'class[^\n]+\s+"{3}\s*([\s\S]+?)"{3}', class_code)
            doc = f'> {doc[0]}' if doc else ''
            class_text = f'\n### `{name}`\n{doc}'
            methods = findall(
                r'(@([\S]+\([\S\s]+?\))?|[\S]+)\s+def +([^\s(]+)\(\s*'
                r'((\b[\S]+\b\s*:\s*[^=,:]+\s*=\s*[^,)]+,?\s*|\b[\S]+\b=\s*[^,)]+,?\s*|'
                r'\b[\S]+\b\s*:\s*[^,)]+,?\s*|\b[\S]+\b\s*,?\s*)+)\)(\s*->\s*[^:]+:'
                r'|\s*:)\s+(\"{3}([\s\S]+?)\"{3})?', class_code)
            class_text += '\n#### methods'
            methods_text = []
            for method in methods:
                decorator, _, name, arguments, _, return_type, _, docs = method
                print(method)
                # description
                description = findall(r'\s*([^:]+)', docs)
                description = description[0].rstrip(' \n') if description else ''
                # return type
                return_type = findall(r'->\s*([^:]+):', return_type)
                return_type = f' -> {return_type[0]}' if return_type else ''
                # arguments
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
                params = '\n- '.join([f'`{i["name"]}`: {i["desc"]}' for i in arguments if i['desc']])
                params = f'\n- {params}' if params else ''
                methods_text.append(
                    f'\n```py\ndef {name}(\n    {arguments_text}\n){return_type}:\n```'
                    f'\n{description}\n{params}\n')
            class_text += '\n___\n'.join(methods_text)
            classes_text.append(class_text)
        # write classes data
        if classes_text:
            class_text = '\n'.join(classes_text)
            data += f'\n## Classes\n{class_text}'

        with open(end_path, 'w', encoding='utf-8') as f:
            f.write(data)
