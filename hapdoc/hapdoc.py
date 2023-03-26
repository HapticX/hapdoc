# -*- coding: utf-8 -*-
"""
Autodoc CLI
"""
import os
from os import path, remove
from glob import glob
from time import time
from pprint import pprint

import click
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import status
from jinja2 import FileSystemLoader, Environment, select_autoescape

from .autodocker import generate, all_project_types
from .md import Md2Html


app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)


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


@hapdoc.command()
@click.argument('docs', type=str)
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

    env = Environment(
        loader=FileSystemLoader(templates_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')
    md_files = [
        f.replace(path.normpath(docs), '')
        for f in glob(path.normpath(docs + '/**/*.md'), recursive=True)
    ]

    sidebar = {}

    for mdf in md_files:
        mdf = mdf.strip('\\').strip('/')
        directory = [i for i in mdf.split(os.sep) if i]
        mdf = mdf.replace('\\', '/')
        temp_sidebar: dict = sidebar
        for idx, temp_path in enumerate(directory):
            # File
            if idx == len(directory) - 1:
                file = temp_path.rsplit('.', 1)[0]
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
            page = Md2Html.cast(data)
            page, title_refs = Md2Html.rand_title_ref(page)
            print(title_refs)
            return HTMLResponse(
                template.render(
                    pageData=page,
                    title=title,
                    titleRefs=title_refs,
                    side=sidebar,
                    nav={"links": [
                        {"title": "Github", "url": "https://github.com/hapticx/hapdoc"},
                    ]},
                    accentColor=accent_color,
                    backgroundColor=background_color,
                    surfaceColor=surface_color,
                    selected=f'/{doc}'
                )
            )
        return HTMLResponse(
            '<h1>Not Found</h1>',
            status_code=status.HTTP_404_NOT_FOUND
        )

    click.echo(f'Your server runs at http://{host}:{port}')
    uvicorn.run(app, host=host, port=int(port))


@hapdoc.command()
@click.argument('docs', type=str)
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
    help='Extend doc by specified docs types separated by comma',
    default='',
    type=str
)
@click.option(
    '--out', '-o', 'output',
    help='Output docs folder',
    default='buildocs',
    type=str
)
@click.option(
    '-t', '--template', 'templates_folder',
    default='hapdoc/templates/vitepress',
    type=str
)
@click.option(
    '-T', '--title', 'title',
    help='Page title',
    default='HapDoc',
    type=str
)
@click.option(
    '-a', '--accent', 'accent_color',
    help='Accent color',
    default='#c27bd4',
    type=str
)
@click.option(
    '-b', '--background', 'background_color',
    help='Background color',
    default='#212121',
    type=str
)
@click.option(
    '-s', '--surface', 'surface_color',
    help='Surface color',
    default='#343434',
    type=str
)
@click.option(
    '-r', '--root', 'root',
    help='Root path, by default uses working directory',
    default=None,
    type=str
)
def build(
        docs: str,
        templates_folder: str,
        title: str,
        accent_color: str,
        background_color: str,
        surface_color: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
        root: str,
):
    """
    Automatically builds project

    :param docs: Path to docs
    :param templates_folder: path to templates folder
    :param title: Docs title
    :param accent_color: Accent color
    :param background_color: Background color
    :param surface_color: Surface color
    :param document_type: Type of project
    :param ignore: Ignore file extensions
    :param extend: Extend file extensions
    :param output: Output folder
    :param root: Root path
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
                docs, None, ignore_list, document_type, extend, output
        ):
            progress.length = i[1]
            progress.update(i[0])
    click.echo(f'Generated in {round(time() - start)} seconds')

    if root is None:
        root = path.join(os.getcwd(), output, docs)
    print(root)

    env = Environment(
        loader=FileSystemLoader(templates_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')
    docs = path.join(output, docs)
    md_files = [
        f.replace(path.normpath(docs), '')
        for f in glob(path.normpath(docs + '/**/*.md'), recursive=True)
    ]

    sidebar = {}

    for mdf in md_files:
        mdf = mdf.strip('\\').strip('/').rsplit('.', 1)[0]
        directory = [i for i in mdf.split(os.sep) if i]
        mdf = mdf.replace('\\', '/')
        temp_sidebar: dict = sidebar
        for idx, temp_path in enumerate(directory):
            # File
            if idx == len(directory) - 1:
                file = temp_path.rsplit('.', 1)[0]
                temp_sidebar[file] = {
                    '_data': {
                        'id': mdf.replace('\\', '_'),
                        'title': file,
                        'url': f'{root}/{mdf}.html'.replace('\\', '/')
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
    md_files = [
        path.join(docs, i[1:]) for i in md_files
    ]
    print(md_files)

    for filename in md_files:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        remove(filename)
        extension = '.' + filename.rsplit('.', 1)[1]
        page = Md2Html.cast(data)
        page, title_refs = Md2Html.rand_title_ref(page)
        with open(filename[:-len(extension)] + '.html', 'w', encoding='utf-8') as file:
            filename = path.normpath(filename).replace(docs, '')
            file.write(
                template.render(
                    pageData=page,
                    title=title,
                    titleRefs=title_refs,
                    side=sidebar,
                    nav={"links": [
                        {"title": "Github", "url": "https://github.com/hapticx/hapdoc"},
                    ]},
                    accentColor=accent_color,
                    backgroundColor=background_color,
                    surfaceColor=surface_color,
                    selected=(root + filename[:-len(extension)] + '.html').replace('\\', '/')
                )
            )
