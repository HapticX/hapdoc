# -*- coding: utf-8 -*-
from os import path

from .abc import ABCDocType

from .filetypes import Py


class PyDoc(ABCDocType):
    def process(
            self,
            project_path: str,
            output_dir: str = 'docs',
            ignore_files: list[str] = None,
            extend: list['ABCDocType'] = None,
    ):
        if path.isdir(project_path):
            for i in self.iter(project_path):
                Py.process(f'{path.join(project_path, i)}', output_dir)
        else:
            Py.process(project_path, output_dir, True)
