# -*- coding: utf-8 -*-
"""
Describes Python file type
"""
from re import findall, compile, sub, MULTILINE
from typing import Iterable

from ..abc import ABCFileType


class Py(ABCFileType):
    """
    Provides Python to Markdown translator
    """

    @staticmethod
    def _process(functions: list[tuple]) -> Iterable[tuple[str]]:
        for i in functions:
            decorator, _, is_async, name, arguments, return_type, _, docs = i
            # description
            description = findall(r'\s*([^:]+)', docs)
            description = description[0].rstrip(' \n') if description else ''
            # decorators
            decorators = [i.strip() for i in decorator.split('@')[1:]] if decorator else []
            # return type
            return_type = f' -> {return_type[3:-1]}' if return_type.startswith('->') else ''
            # arguments
            arg_list = [
                {'name': arg[0], 'desc': arg[1]}
                for arg in findall(r':param\s+([^\s:]+?)\s*:\s*([^\n]+)\s*\n', docs)
            ]
            arguments = sub(r'\s{4,}', r'\n   ', arguments)
            arguments = sub(r'\s+\)\Z', r'\n', arguments)
            if arguments.endswith(')'):
                arguments = arguments[:-1]
            yield description, decorators, return_type, arg_list, is_async, name, arguments[1:]

    @staticmethod
    def process_funcs(
            functions: list[tuple]
    ) -> str:
        """
        Process functions and methods in .py files

        :param source: source python file
        :param functions: list of parsed functions (via regex)
        :return: md formatted string
        """
        methods_text = []
        for desc, decorators, ret_type, arg_list, is_async, name, arguments in Py._process(functions):
            params = '\n- '.join([f'`{i["name"]}` - {i["desc"]}' for i in arg_list if i['desc']])
            params = f'\n- {params}' if params else ''
            decorator_text = '\n@'.join(decorators)
            decorator_text = f'@{decorator_text}\n' if decorators else ''
            arguments_text = f'{arguments}' if arguments else ''
            methods_text.append(
                f'\n```python\n{decorator_text}{is_async}def '
                f'{name}({arguments_text}){ret_type}:\n```'
                f'\n{desc}\n{params}\n')
        return '\n___\n'.join(methods_text)

    @staticmethod
    def process(
            cls,
            filepath: str,
            output: str = 'docs',
            one_file: bool = False
    ):
        """
        Translates python script into md file.

        :param cls: Class
        :param filepath: path to python script
        :param output: output directory
        :param one_file: True when file flag is True
        :return:
        """
        source, end_path, filename = cls.pre(filepath, output, one_file)
        data = f'# {filename}\n'

        description = findall(compile(r'^"{3}\s*([\s\S]+?)\s*"{3}', MULTILINE), source)
        if description:
            data += f'\n{description[0].strip()}'

        # Handle classes
        classes = findall(compile(r'^\s*class +([^:]+?):\n(\s+)([^\n]+(\n+\2[ \S]*)+)', MULTILINE), source)
        classes_text = []
        for class_data in classes:
            name = class_data[0]
            doc = findall(r'"{3}\s*([\s\S]+?)"{3}', class_data[2])
            doc = f'{doc[0]}' if doc else ''
            class_text = f'\n### `{name}`\n{doc}'
            # Handle class methods
            methods = findall(
                r"^\s*((@[\S]+\(\)|@[\S]+\([\S\s]+?\)|\s*|@[\S]+\s*)+)?"
                r"\s+(async +)?def +([^_][^\s(]+)(\(\)|\([\s\S]+?\))\s*(->\s*[^:]+:|\s*:)"
                r"\s+(\"{3}([\s\S]+?)\"{3})?",
                class_data[2],
                MULTILINE
            )
            class_text += '\n#### methods'
            class_text += cls.process_funcs(methods)
            classes_text.append(class_text)
        # write classes data
        if classes_text:
            class_text = '\n'.join(classes_text)
            data += f'\n## Classes\n{class_text}'

        # Handle functions
        functions = findall(
            r'^((@[\S]+\s*\(\)\s*|@[\S]+\s*\([\s\S]+?\)\s*|@[\S]+\s*)+)?\s+'
            r'^(async +)?def +([^_][^\s(]+)(\(\)|\([\s\S]+?\))\s*(->\s*[^:]+:|\s*:)'
            r'\s+(\"{3}([\s\S]+?)\"{3})?',
            source,
            MULTILINE
        )
        if functions:
            data += f'\n### Functions\n{cls.process_funcs(functions)}'

        with open(end_path, 'w', encoding='utf-8') as file:
            file.write(data)
