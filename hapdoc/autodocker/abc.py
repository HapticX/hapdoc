# -*- coding: utf-8 -*-
from abc import abstractmethod
from os import path, listdir, sep, makedirs
from typing import Iterable


class ABCDocType:
    """
    Provides abstract behavior of inherited DocType classes
    """
    @abstractmethod
    def process(
            self,
            project_path: str,
            output_dir: str = 'docs',
            ignore_files: list[str] = None,
            extend: list['ABCDocType'] = None,
    ):
        """
        Process project and generate docs

        :param project_path: project path
        :param output_dir: output directory
        :param ignore_files: ignore files with extensions
        :param extend: extend other DocType classes
        :return:
        """
        raise RuntimeError('ABCDocType can not called.')

    @staticmethod
    def iter(directory: str) -> Iterable[str]:
        """
        Go over directory and yields all files

        :param directory: path to directory
        :return: file paths
        """
        res = listdir(directory)
        for i in res:
            p = path.join(directory, i)
            if path.isdir(p):
                for j in ABCDocType.iter(p):
                    yield j
            else:
                yield p


class ABCFileType:
    """
    Provides abstract behavior of inherited FileType classes
    """
    @staticmethod
    @abstractmethod
    def process(
            filepath: str,
            output: str = 'docs',
            one_file: bool = False
    ):
        """
        Process file and translate it into .md

        :param filepath: path to file
        :param output: output directory
        :param one_file: True when target is file
        """
        raise RuntimeError('Can not call this method')

    @staticmethod
    def pre(
            filepath: str,
            output: str = 'docs',
            one_file: bool = False,
    ) -> tuple[str, str, str]:
        """
        Preprocess file and making directories

        :param filepath: path to file
        :param output: output directory
        :param one_file: True when target is file
        """
        # get dir and file
        directory, file = path.split(filepath)
        if not one_file:
            directory = sep.join(directory.split(sep)[1:])
        # filename and extension
        filename, file_extension = path.splitext(file)
        filename = filename.replace('__init__', 'readme')

        end_path = f'{path.join(output, directory, filename)}.md'
        if not path.exists(end_path):
            try:
                makedirs(path.split(end_path)[0])
            except FileExistsError:
                pass

        with open(path.join(directory, file), 'r', encoding='utf-8') as f:
            source = f.read()

        return source, end_path, filename
