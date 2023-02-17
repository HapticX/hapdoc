# -*- coding: utf-8 -*-
from os import path
from typing import Iterable

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
    ) -> Iterable[tuple[int, int]]:
        file_extensions = (
            [i for i in self._file_extensions if i not in ignore_files]
            if ignore_files else self._file_extensions
        )
        if path.isdir(project_path):
            files = [i for i in self.iter(project_path) if path.splitext(i)[1] in file_extensions]
            length = len(files)
            for i, v in enumerate(files):
                Py.process(f'{path.join(project_path, v)}', output_dir)
                yield i, length
        else:
            Py.process(project_path, output_dir, True)
            yield 1, 1
