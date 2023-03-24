# -*- coding: utf-8 -*-
"""
Autodoc CLI
"""
import os
from os import path
from glob import glob
from pprint import pprint

import click

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import status
from uvicorn.server import Server, Config
from jinja2 import FileSystemLoader, Environment, select_autoescape

from hapdoc.autodocker import generate, all_project_types
from hapdoc.md import Md2Html


@click.group()
def hapdoc():
    """
    Autodoc CLI tool for making project's cute docs
    """


@hapdoc.command()
def project_types():
    """
    Shows all available project types
    """
    all_types = all_project_types()
    for project_type in all_types:
        click.echo(f'- {project_type}')


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
def gen(
        project_path: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
):
    """
    Generates docs for file or project
    """
    ignore_list = [
        ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}'
        for ext in ignore.split(',')
    ]
    with click.progressbar(
        label='Generating docs',
        fill_char=click.style('#', 'bright_green'),
        empty_char=' ',
        show_percent=True,
        length=1,
    ) as progress:
        for i in generate(
                project_path, None, ignore_list, document_type, extend, output
        ):
            progress.length = i[1]
            progress.update(i[0])


@hapdoc.command()
@click.option(
    '-h', '--host', 'host',
    default='127.0.0.1',
    type=str
)
@click.option(
    '-p', '--port', 'port',
    default='5000',
    type=str
)
@click.option(
    '-d', '--docs', 'docs',
    default='docs',
    type=str
)
@click.option(
    '-t', '--template', 'templates_folder',
    default='hapdoc/templates/vitepress',
    type=str
)
@click.option(
    '-T', '--title', 'title',
    default='HapDoc',
    type=str
)
@click.option(
    '-a', '--accent', 'accent_color',
    default='#c27bd4',
    type=str
)
@click.option(
    '-b', '--background', 'background_color',
    default='#212121',
    type=str
)
@click.option(
    '-s', '--surface', 'surface_color',
    default='#343434',
    type=str
)
def serve(
        host: str,
        port: str,
        docs: str,
        templates_folder: str,
        title: str,
        accent_color: str,
        background_color: str,
        surface_color: str,
):
    """
    Launches FastAPI docs server

    :param host: hostname
    :param port: port to serve
    :param docs: docs folder
    :param templates_folder: folder with templates
    :param title: web title
    :param accent_color: docs accent color
    :param background_color: docs background color
    :param surface_color: docs surface color
    """
    app = FastAPI(docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    )
    env = Environment(
        loader=FileSystemLoader(templates_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')
    md_files = [
        f.replace(path.normpath(docs), '')
        for f in glob(path.normpath(docs + '/**/*.md'), recursive=True)
    ]
    print(md_files)

    sidebar = {}

    for mdf in md_files:
        mdf = mdf.strip('\\').strip('/')
        directory = [i for i in mdf.split(os.sep) if i]
        mdf = mdf.replace('\\', '/')
        print(directory)
        temp_sidebar: dict = sidebar
        for idx, temp_path in enumerate(directory):
            # File
            print(idx, temp_path, len(directory))
            if idx == len(directory)-1:
                file = temp_path.rsplit('.', 1)[0]
                print(temp_sidebar)
                temp_sidebar[file] = {
                    '_data': {
                        'id': mdf.replace('\\', '_'),
                        'title': file,
                        'url': f'/{mdf}'
                    },
                    '_items': {}
                }
            else:
                # Directory
                if temp_path in temp_sidebar:
                    temp_sidebar = temp_sidebar[temp_path]['_items']
                else:
                    temp_sidebar[temp_path] = {
                        '_data': {
                            'id': mdf.replace('\\', '_'),
                            'title': temp_path,
                            'url': ''
                        },
                        '_items': {}
                    }
                    temp_sidebar = temp_sidebar[temp_path]['_items']
    pprint(sidebar)

    @app.get('/{doc:path}')
    async def get_md_at(doc: str):
        if not doc.endswith('.md'):
            doc += '.md'
        full_path = path.join(docs, doc)
        print(full_path)
        if path.exists(full_path) and path.isfile(full_path):
            with open(full_path, 'r', encoding='utf-8') as filename:
                data = filename.read()
            return HTMLResponse(
                template.render(
                    pageData=Md2Html.cast(data),
                    title=title,
                    side=sidebar,
                    nav={"links": [
                        {"title": "Github", "url": "https://github.com/hapticx/hapdoc"},
                    ]},
                    accentColor=accent_color,
                    backgroundColor=background_color,
                    surfaceColor=surface_color,
                    selected=doc
                )
            )
        return HTMLResponse(
            '<h1>Not Found</h1>',
            status_code=status.HTTP_404_NOT_FOUND
        )

    server = Server(
        config=Config(
            app,
            host=host,
            port=port
        )
    )
    click.echo(f'Your server runs at http://{host}:{port}')
    server.run()


if __name__ == '__main__':
    hapdoc()
