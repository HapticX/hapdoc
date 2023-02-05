# -*- coding: utf-8 -*-
import click

from hapdoc.rules import RegexRules


@click.group()
def hapdoc():
    """
    Autodoc CLI tool for making project's cute docs
    """


@hapdoc.command()
@click.option(
    '--doctype', '-d', 'document_type',
    help='Select project type',
    default='fastapi',
    type=str
)
@click.option(
    '--ignore', '-i', 'ignore',
    help='Ignore file extensions separated by comma',
    default='',
    type=str
)
@click.option(
    '--project', '-p', 'generate_target',
    flag_value='project',
    default=True,
    type=str,
)
@click.option(
    '--file', '-f', 'generate_target',
    flag_value='file',
    type=str,
)
def generate(
        document_type: str,
        ignore: str,
        generate_target: str
):
    """
    Generates docs for file or project
    """
    ignore_list = [ext.strip() for ext in ignore.split(',')]
    RegexRules.process(
        [],
        document_type,
        ignore_list,
    )


if __name__ == '__main__':
    hapdoc()
