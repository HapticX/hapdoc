# -*- coding: utf-8 -*-
"""
Autodoc CLI
"""
from json import dumps
from os import path, remove, makedirs, getcwd

import click
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import status
from jinja2 import FileSystemLoader, Environment, select_autoescape

from .md import Md2Html
from .utils import (
    show_all_projects, generate_md_files,
    cast_md_dir_to_json, load_user_templates,
    create_new_user_template, get_user_template_path,
    load_conf
)
from . import __version__


app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)


@click.group(invoke_without_command=True)
@click.option(
    '-v/--version', 'show_version',
    default=False, type=bool
)
def hapdoc(show_version: bool):
    """
    HapDoc is a powerful command-line interface tool that automates the process of
    generating documentation for various types of projects.
    With HapDoc, you can easily create high-quality documentation for
    Python, FastAPI, Vue, and many other types of projects.
    """
    if show_version:
        click.echo(click.style(f'HapDoc v{__version__}', fg='bright_blue'))


@hapdoc.command()
def project_types():
    """
    This command displays a list of all available project
    types that can be used in doc generating.
    """
    show_all_projects()


@hapdoc.command()
def tmpl_list():
    """
    This command displays a list of all templates that have been saved by the current user.
    It is useful for quickly checking which templates are available for use.
    """
    load_user_templates()


@hapdoc.command()
def tmpl_new():
    """
    The `tml_new` command creates a new template and saves it for future use.
    The user will be prompted to provide a name for the template and
    specify whether Tailwind CSS should be included.
    """
    create_new_user_template()


@hapdoc.command()
@click.argument("directory", type=str)
@click.option(
    '-o', '--output', 'output_file',
    help='Output file name',
    default='overview.json', type=str
)
@click.option(
    '-O', '--outdir', 'output_directory',
    help='Output directory path',
    default=None, type=str
)
@click.option(
    '-r', '--root', 'root',
    help='Root path, by default uses working directory',
    default=None, type=str
)
@click.option(
    '-e', '--extension', 'ext',
    help='File extensions in generated JSON',
    default=None, type=str
)
def md2json(directory: str, output_directory: str, output_file: str, root: str, ext: str):
    """
    The md2json command converts Markdown files (.md) in a directory to JSON format,
    which can be used for rendering the files using the jinja2 templating engine.
    This command is useful for converting Markdown files to a format that
    can be easily parsed and manipulated by other tools.
    """
    root = load_conf('root', root, '')

    if ext is None:
        ext = ".md"
    data = cast_md_dir_to_json(directory, root, False, ext)
    click.echo(click.style("Generated", fg="bright_green"))

    if output_directory is not None:
        makedirs(output_directory, exist_ok=True)
        with open(path.join(output_directory, output_file), 'w', encoding='utf-8') as file:
            file.write(dumps(data, indent=4))
        click.echo(click.style(f"Saved at {output_directory}/{output_file}", fg="bright_green"))
    else:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(dumps(data, indent=4))
        click.echo(click.style(f"Saved at {output_file}", fg="bright_green"))


@hapdoc.command()
@click.argument('project_path', type=str)
@click.option(
    '-d', '--doctype', 'document_type',
    help='Select project type',
    default='py', type=str
)
@click.option(
    '-i', '--ignore', 'ignore',
    help='Ignore file extensions separated by comma',
    default='', type=str
)
@click.option(
    '-e', '--extend', 'extend',
    help='Extend doc by specified doctypes separated by comma',
    default=None, type=str
)
@click.option(
    '-o', '--out', 'output',
    help='Output docs folder',
    default='docs', type=str
)
def gen(
        project_path: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
):
    """
    This command generates Markdown files with documentation for a project or file.
    The user provides a path to the project or file that needs documentation.
    """
    generate_md_files(project_path, document_type, ignore, extend, output)


@hapdoc.command()
@click.argument('docs', type=str)
@click.option(
    '-h', '--host', 'host',
    default='127.0.0.1', type=str
)
@click.option(
    '-p', '--port', 'port',
    default='5000', type=str
)
@click.option(
    '-t', '--template', 'templates_folder',
    default=None, type=str
)
@click.option(
    '-T', '--title', 'title',
    default=None, type=str
)
@click.option(
    '-a', '--accent', 'accent_color',
    default='#c27bd4', type=str
)
@click.option(
    '-b', '--background', 'background_color',
    default='#212121', type=str
)
@click.option(
    '-s', '--surface', 'surface_color',
    default='#343434', type=str
)
@click.option(
    '-la', '--light-accent', 'light_accent_color',
    help='Light Accent color',
    default='#b26bc4', type=str
)
@click.option(
    '-lb', '--light-background', 'light_background_color',
    help='Light Background color',
    default='#cacaca', type=str
)
@click.option(
    '-ls', '--light-surface', 'light_surface_color',
    help='Light Surface color',
    default='#dedede', type=str
)
@click.option(
    '-dv', '--doc-version', 'doc_version',
    help='Generated documentation version',
    default=None, type=str
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
        light_accent_color: str,
        light_background_color: str,
        light_surface_color: str,
        doc_version: str,
):
    """
    The `serve` command starts a web server using FastAPI and uvicorn and
    provides access to Markdown files in a web browser.
    """
    doc_version = load_conf('version', doc_version, '1.0.0')
    title = load_conf('title', title, 'HapDoc')
    templates_folder = load_conf('template', templates_folder, 'hapdoc/templates/vitepress')

    user_template = get_user_template_path(templates_folder)
    env = Environment(
        loader=FileSystemLoader(user_template if user_template else templates_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')
    sidebar = cast_md_dir_to_json(docs)

    @app.get('/{doc:path}')
    async def get_md_at(doc: str):
        if not doc.endswith('.md'):
            doc += '.md'
        full_path = path.join(docs, doc)
        if path.exists(full_path) and path.isfile(full_path):
            with open(full_path, 'r', encoding='utf-8') as filename:
                data = filename.read()
            page = Md2Html.cast(data)
            page, title_refs = Md2Html.rand_title_ref(page)
            return HTMLResponse(
                template.render(
                    pageData=page,
                    title=title,
                    titleRefs=title_refs,
                    side=sidebar,
                    nav={"links": [
                        {
                            "title": "Github",
                            "icon": "fab fa-github",
                            "show_text": True,
                            "url": "https://github.com/hapticx/hapdoc"
                        },
                    ]},
                    docVersion=doc_version,
                    accentColor=accent_color,
                    backgroundColor=background_color,
                    surfaceColor=surface_color,
                    lightAccentColor=light_accent_color,
                    lightBackgroundColor=light_background_color,
                    lightSurfaceColor=light_surface_color,
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
    '-d', '--doctype', 'document_type',
    help='Select project type',
    default='py', type=str
)
@click.option(
    '-i', '--ignore', 'ignore',
    help='Ignore file extensions separated by comma',
    default='', type=str
)
@click.option(
    '-e', '--extend', 'extend',
    help='Extend doc by specified docs types separated by comma',
    default=None, type=str
)
@click.option(
    '-o', '--out', 'output',
    help='Output docs folder',
    default='buildocs', type=str
)
@click.option(
    '-t', '--template', 'templates_folder',
    default=None, type=str
)
@click.option(
    '-T', '--title', 'title',
    help='Page title',
    default=None, type=str
)
@click.option(
    '-a', '--accent', 'accent_color',
    help='Accent color',
    default='#c27bd4', type=str
)
@click.option(
    '-b', '--background', 'background_color',
    help='Background color',
    default='#212121', type=str
)
@click.option(
    '-s', '--surface', 'surface_color',
    help='Surface color',
    default='#343434', type=str
)
@click.option(
    '-la', '--light-accent', 'light_accent_color',
    help='Light Accent color',
    default='#b26bc4', type=str
)
@click.option(
    '-lb', '--light-background', 'light_background_color',
    help='Light Background color',
    default='#dfdfdf', type=str
)
@click.option(
    '-ls', '--light-surface', 'light_surface_color',
    help='Light Surface color',
    default='#cacaca', type=str
)
@click.option(
    '-r', '--root', 'root',
    help='Root path, by default uses working directory',
    default=None, type=str
)
@click.option(
    '-dv', '--doc-version', 'doc_version',
    help='Generated documentation version',
    default=None, type=str
)
@click.option(
    '-fm', '--from-markdown', 'from_markdown',
    help='Generate HTML from markdown',
    default=None, type=bool
)
def build(
        docs: str,
        templates_folder: str,
        title: str,
        accent_color: str,
        background_color: str,
        surface_color: str,
        light_accent_color: str,
        light_background_color: str,
        light_surface_color: str,
        document_type: str,
        ignore: str,
        extend: str,
        output: str,
        root: str,
        doc_version: str,
        from_markdown: bool
):
    """
    This command generates documentation for a project by first creating Markdown
    files and then converting them to HTML files.
    """
    doc_version = load_conf('version', doc_version, '1.0.0')
    root = load_conf('root', root, '/')
    title = load_conf('title', title, 'HapDoc')
    templates_folder = load_conf('template', templates_folder, 'hapdoc/templates/vitepress')

    user_template = get_user_template_path(templates_folder)
    env = Environment(
        loader=FileSystemLoader(user_template if user_template else templates_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')
    if not from_markdown:
        generate_md_files(docs, document_type, ignore, extend, output)
        if root is None:
            root = path.join(getcwd(), output, docs)

    if path.isfile(docs):
        docs, filename = path.split(docs)
    docs = path.join(output, docs)
    sidebar, md_files = cast_md_dir_to_json(docs, root, True, '.html')
    md_files = [path.join(docs, i[1:]) for i in md_files]

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
                        {
                            "title": "Github",
                            "icon": "fab fa-github",
                            "show_text": True,
                            "url": "https://github.com/hapticx/hapdoc"
                        },
                    ]},
                    docVersion=doc_version,
                    accentColor=accent_color,
                    backgroundColor=background_color,
                    surfaceColor=surface_color,
                    lightAccentColor=light_accent_color,
                    lightBackgroundColor=light_background_color,
                    lightSurfaceColor=light_surface_color,
                    selected=f'{root}{filename[:-len(extension)]}.html'.replace('\\', '/')
                )
            )
