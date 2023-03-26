# -*- coding: utf-8 -*-
"""
Describes Python file type
"""
from re import findall, IGNORECASE

from .py import Py


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
        for desc, decorators, _, arg_list, _, _, arguments in FastApi._process(functions):
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
            params = '\n- '.join([f'`{i["name"]}` - {i["desc"]}' for i in arg_list if i['desc']])
            params = f'\n- {params}' if params else ''
            query_text = f'#### Query Params:\n{params}'
            methods_text.append(
                f'\n```http\n{req_method} {req_route} HTTP/1.1\n```'
                f'\n{desc}\n{query_text}\n')
        return '\n___\n'.join(methods_text)
