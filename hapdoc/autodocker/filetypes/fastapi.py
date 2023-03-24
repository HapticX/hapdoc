# -*- coding: utf-8 -*-
"""
Describes Python file type
"""
from re import findall, sub, MULTILINE, IGNORECASE

from . import Py


class FastApi(Py):
    """
    Provides Python file type behavior
    """

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
        for desc, decorators, ret_type, arguments, docs, is_async, name in FastApi._process(functions):
            req_method, req_route = '', ''
            # Find method and route path
            for decorator in decorators:
                data = findall(
                    r'(get|post|put|patch|delete|options|copy|link|unlink|purge|head)'
                    r'\((\'[^\']+?\'|"[^"]+")\)',
                    decorator, IGNORECASE)
                if data:
                    data = data[0]
                    req_method, req_route = data[0].upper(), data[1].strip('"').strip("'")
            if not req_method and not req_route:
                continue
            params = '\n- '.join([f'`{i["name"]}` - {i["desc"]}' for i in arguments if i['desc']])
            params = f'\n- {params}' if params else ''
            query_text = f'#### Query Params:\n{params}'
            methods_text.append(
                f'\n```http\n{req_method} {req_route} HTTP/1.1\n```'
                f'\n{desc}\n{query_text}\n')
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
        source, end_path, filename = FastApi.pre(filepath, output, one_file)
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
            class_text += FastApi.process_funcs(methods)
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
            data += f'\n### Functions\n{FastApi.process_funcs(functions)}'

        with open(end_path, 'w', encoding='utf-8') as f:
            f.write(data)
