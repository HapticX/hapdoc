# -*- coding: utf-8 -*-
"""
Autodoc CLI
"""
from os import path
from glob import glob

import click

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import status
from uvicorn.server import Server, Config
from jinja2 import FileSystemLoader, Environment, select_autoescape

from hapdoc.autodocker import generate
from hapdoc.autodocker.doctypes import PyDoc
from hapdoc.md import Md2Html


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
    ignore_list = [ext.strip() for ext in ignore.split(',')]
    generate(
        project_path,
        {
            'py': PyDoc,
        },
        ignore_list,
        document_type,
        extend,
        output
    )


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
def serve(
        host: str,
        port: str,
        docs: str,
        templates_folder: str,
        title: str,
):
    """
    Launches FastAPI docs server

    :param host: hostname
    :param port: port to serve
    :param docs: docs folder
    :param templates_folder: folder with templates
    :param title: web title
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
    md_files = [f.replace(path.normpath(docs), '')[1:-3] for f in glob(path.normpath(docs + '/**/*.md'), recursive=True)]
    print(md_files)

    @app.get('/docs/{doc:path}')
    async def get_md_at(doc: str):
        if not doc.endswith('.md'):
            doc += '.md'
        p = path.join(docs, doc)
        if path.exists(p) and path.isfile(p):
            with open(p, 'r', encoding='utf-8') as f:
                data = f.read()
            return HTMLResponse(
                template.render(
                    pageData=Md2Html.cast(data),
                    title=title,
                    side=[
                        {
                            'title': 'All',
                            'id': 'something',
                            'data': [
                                {
                                    'title': path.split(f)[1],
                                    'url': f'http://localhost:5000/docs/{f}'
                                }
                                for f in md_files
                            ]
                        }
                    ],
                    nav=[{
                        "links": [{
                            "title": "Github",
                            "url": "https://github.com/hapticx/hapdoc"
                        }]
                    }],
                    accentColor='#5ECED4'
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
    server.run()


if __name__ == '__main__':
    hapdoc()
