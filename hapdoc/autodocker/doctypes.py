# -*- coding: utf-8 -*-
from os import path

from .abc import ABCDocType

from .filetypes import Py


class PyDoc(ABCDocType):
    _file_extensions = ['.py']

    def process(
            self,
            project_path: str,
            output_dir: str = 'docs',
            ignore_files: list[str] = None,
            extend: list['ABCDocType'] = None,
    ):
        file_extensions = (
            [i for i in self._file_extensions if i not in ignore_files]
            if ignore_files else self._file_extensions
        )
        if path.isdir(project_path):
            for i in self.iter(project_path):
                p, ext = path.splitext(i)
                if ext in file_extensions:
                    Py.process(f'{path.join(project_path, i)}', output_dir)
        else:
            Py.process(project_path, output_dir, True)
