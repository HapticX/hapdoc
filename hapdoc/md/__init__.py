# -*- coding: utf-8 -*-
import re


class Md2Html:
    _rules = [
        (r'###### ([^\n]+)', r'<h6>\1</h6>'),
        (r'##### ([^\n]+)', r'<h5>\1</h5>'),
        (r'#### ([^\n]+)', r'<h4>\1</h4>'),
        (r'### ([^\n]+)', r'<h3>\1</h3>'),
        (r'## ([^\n]+)', r'<h2>\1</h2>'),
        (r'# ([^\n]+)', r'<h1>\1</h1>'),
        (r'!\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<img src="\2" alt="\1">'),
        (r'\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<a href="\2">\1</a>'),
    ]

    @staticmethod
    def cast(source: str) -> str:
        for pattern, repl in Md2Html._rules:
            source = re.sub(pattern, repl, source)
        return source
