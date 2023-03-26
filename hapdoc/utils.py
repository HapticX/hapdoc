# -*- coding: utf-8  -*-
"""
Provides some CLI utils
"""
import click

from glob import glob
from os import path, sep
from time import time

from .autodocker import generate, all_project_types


def show_all_projects():
    """
    Shows all project types
    """
    all_types = all_project_types()
    for project_type in all_types:
        click.echo(f'- {project_type}')


def generate_md_files(
        project_path: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
):
    """
    Generates docs for file or project

    :param project_path: Path to project directory or file
    :param document_type: Available file extension
    :param ignore: Ignore file extensions separated by comma
    :param extend: Extend file extensions separated by comma
    :param output: Output directory
    """
    ignore_list = [
        ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}'
        for ext in ignore.split(',')
    ]
    start = time()
    with click.progressbar(
            label='Generating docs',
            fill_char=click.style('#', 'bright_green'),
            empty_char=' ',
            bar_template='%(label)s  [%(bar)s]',
            show_percent=True,
            length=1,
    ) as progress:
        for i in generate(
                project_path, None, ignore_list, document_type, extend, output
        ):
            progress.length = i[1]
            progress.update(i[0])
    click.echo(f'Generated in {round(time() - start)} seconds')


def cast_md_dir_to_json(
        directory: str,
        root: str = '',
        return_md_files: bool = False,
        extension: str = '.md',
) -> dict[str, dict] | tuple[dict[str, dict], list[str]]:
    """
    Casts directory of md files to JSON representation

    :param directory: Directory with Markdown files
    :param root: Root directory
    :param return_md_files: Returns list of Markdown files when True
    :param extension: File extension in JSON url
    """
    result = {}
    md_files = [
        f.replace(path.normpath(directory), '')
        for f in glob(path.normpath(directory + '/**/*.md'), recursive=True)
    ]

    if not extension.startswith('.'):
        extension = f'.{extension}'

    for mdf in md_files:
        mdf = mdf.strip('\\').strip('/').rsplit('.', 1)[0]
        directory = [i for i in mdf.split(sep) if i]
        mdf = mdf.replace('\\', '/')
        temp_sidebar: dict = result
        for idx, temp_path in enumerate(directory):
            if idx == len(directory) - 1:
                # File
                file = temp_path.rsplit('.', 1)[0]
                temp_sidebar[file] = {
                    '_data': {
                        'id': mdf.replace('\\', '_'),
                        'title': file,
                        'url': f'{root}/{mdf}{extension}'.replace('\\', '/')
                    },
                    '_items': {}
                }
            elif temp_path in temp_sidebar:
                # Available Directory
                temp_sidebar = temp_sidebar[temp_path]['_items']
            else:
                # New directory
                temp_sidebar[temp_path] = {
                    '_data': {
                        'id': mdf.replace('\\', '_'),
                        'title': temp_path,
                        'url': ''
                    },
                    '_items': {}
                }
                temp_sidebar = temp_sidebar[temp_path]['_items']
    if return_md_files:
        return result, md_files
    return result
