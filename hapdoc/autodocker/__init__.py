# -*- coding: utf-8 -*-
from typing import Iterable

from .abc import ABCDocType
from .doctypes import PyDoc
from .filetypes import Py


__all__ = ['generate']


_config = {
    'py': PyDoc
}


def generate(
        project_path: str,
        config: dict[str, ABCDocType] = None,
        ignore_list: list[str] = None,
        document_type: str = 'py',
        extend: list[str] = None,
        output: str = 'docs'
) -> Iterable[tuple[int, int]]:
    if config is None:
        config = _config
    if document_type not in config:
        raise RuntimeError('Unknown document type.')
    doctype = config[document_type]
    for i in doctype().process(project_path, output, ignore_list, extend):
        yield i[0], i[1]
