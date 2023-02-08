# -*- coding: utf-8 -*-
from os import path

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
):
    if config is None:
        config = _config
    if document_type in config:
        doctype = config[document_type]
        doctype().process(project_path, output, ignore_list, extend)
    else:
        raise RuntimeError('Unknown document type.')
