# -*- coding: utf-8 -*-
from re import Pattern
from typing import Literal


class RegexRules:
    @staticmethod
    def process(
            rules: list[tuple[Pattern]],
            target: Literal['project', 'file'] = 'project',
            ignore_file_extensions: list[str] = None,
            output_dir: str = 'docs',
            doc_type: str = 'fastapi',
    ):
        """
        Rules should be:
            [
                ('file extension', )
            ]
        """
        pass
