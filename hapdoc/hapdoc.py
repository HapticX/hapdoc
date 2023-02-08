# -*- coding: utf-8 -*-
"""
Autodoc CLI
"""
import click

from hapdoc.autodocker import generate as gen
from hapdoc.autodocker.doctypes import PyDoc


@click.group()
def hapdoc():
    """
    Autodoc CLI tool for making project's cute docs
    """


@hapdoc.command()
@click.argument('project_path', type=str)
@click.option(
    '--doctype', '-d', 'document_type',
    help='Select project type',
    default='py',
    type=str
)
@click.option(
    '--ignore', '-i', 'ignore',
    help='Ignore file extensions separated by comma',
    default='',
    type=str
)
@click.option(
    '--extend', '-e', 'extend',
    help='Extend doc by specified doctypes separated by comma',
    default='',
    type=str
)
@click.option(
    '--out', '-o', 'output',
    help='Output docs folder',
    default='docs',
    type=str
)
def generate(
        project_path: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
):
    """
    Generates docs for file or project
    """
    ignore_list = [ext.strip() for ext in ignore.split(',')]
    gen(
        project_path,
        {
            'py': PyDoc,
        },
        ignore_list,
        document_type,
        extend,
        output
    )


if __name__ == '__main__':
    hapdoc()
