# -*- coding: utf-8 -*-
from os import path, listdir
from typing import Iterable, Type

from .abc import ABCDocType, ABCFileType
from .filetypes import Py, FastApi


__all__ = ['generate', 'all_project_types']


_config = {
    'py': {
        'file_types': {
            '.py': Py
        }
    },
    'fastapi': {
        'file_types': {
            '.py': FastApi
        }
    }
}


def all_project_types() -> list[str]:
    return [i for i in _config.keys()]


def generate(
        project_path: str,
        config: dict[str, Type[ABCFileType]] = None,
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
    for i in _process(
            project_path, output, ignore_list, extend, doctype['file_types']
    ):
        yield i[0], i[1]


def _iter_dir(directory: str) -> Iterable[str]:
    """
    Go over directory and yields all files

    :param directory: path to directory
    :return: file paths
    """
    res = listdir(directory)
    for i in res:
        p = path.join(directory, i)
        if path.isdir(p):
            for j in _iter_dir(p):
                yield j
        else:
            yield p


def _process(
        project_path: str,
        output_dir: str = 'docs',
        ignore_files: list[str] = None,
        extend: dict[str, Type[ABCFileType]] = None,
        file_types: dict[str, Type[ABCFileType]] = None,
) -> Iterable[tuple[int, int]]:
    """
    Processes project and generating docs from it

    :param project_path: path to project
    :param output_dir: output directory name
    :param ignore_files: ignore file extensions list
    :param extend: extended file types list
    :param file_types: dictionary of supported file types
    :return:
    """
    file_extensions = (
        [i for i in file_types.keys() if i not in ignore_files]
        if ignore_files else
        [i for i in file_types.keys()]
    )
    if path.isdir(project_path):
        files = [i for i in _iter_dir(project_path) if path.splitext(i)[1] in file_extensions]
        length = len(files)
        for i, v in enumerate(files):
            file, ext = path.splitext(v)
            file_types[ext].process(f'{path.join(project_path, v)}', output_dir)
            yield i, length
    else:
        file, ext = path.splitext(project_path)
        file_types[ext].process(project_path, output_dir, True)
        yield 1, 1
