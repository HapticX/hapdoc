# -*- coding: utf-8 -*-
from re import findall, sub
from os import mkdir, path, makedirs, sep

from .abc import ABCFileType

from hapdoc.md import Md2Html


class Py(ABCFileType):
    @staticmethod
    def process(
            filepath: str,
            output: str = 'docs'
    ):
        source, end_path, filename = Py.pre(filepath, output)
        data = f'# {filename}\n'

        description = findall(r'[^ \r\t]\"{3}([\s\S]+?)\"{3}', source)
        if description:
            data += f'\n> {description[0]}'

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
                    arg_desc = findall(r':param\s+' + name + r'\s*:\s+([^\n]+)', docs)
                    arg_desc = arg_desc[0].strip() if arg_desc else ''
                    arguments.append({
                        'name': arg_name,
                        'type': arg_type,
                        'default': default_value,
                        'desc': description,
                        'text': f'{arg_name}: {arg_type} = {default_value}'
                                if default_value else f'{arg_name}: {arg_type}'
                                if arg_type else arg_name
                    })
                arguments_text = ",\n    ".join([i["text"] for i in arguments])
                methods_text.append(
                    f'\n```py\ndef {name}(\n    {arguments_text}\n){return_type}:\n```' \
                    f'\n{description}')
            class_text += '\n___\n'.join(methods_text)
            classes_text.append(class_text)
        # write classes data
        if classes_text:
            class_text = '\n'.join(classes_text)
            data += f'## Classes\n{class_text}'

        with open(end_path, 'w', encoding='utf-8') as f:
            f.write(data)
