"""
HapDoc is a Python-based tool that automates the process of generating documentation for your projects.
It supports `Python` and `FastAPI` project types and can generate Markdown files,
HTML files, and JSON structures of your project's Markdown directory.

This file provides `/hapdoc/readme`.

## Get Started
To install the tool, you can use pip. Open up your terminal and run the following command:
```bash
pip install hapdoc
```

## Usage
To generate documentation for your project using HapDoc,
you will need to run the autodoc command.
Here's an example of how to use it:
```bash
hapdoc gen path/to/project [--doctype py/fastapi] [-out docs]
```
This command generates Markdown files for a Python project in the output directory.
You can also use the `out` flag to specify output directory.
`doctype` flag specifies project type.

## Supported Project Types
hapDoc currently supports `Python` and `FastAPI` project types.
In the future, we plan to add support for `Nim`, `JS`, `Vue`, and many other project types.

## Command Line Interface
Here's a list of available commands you can use with HapDoc:
- `gen`: Generates Markdown files with documentation for project
- `build`: Generates like `gen` and builds from it the HTML files.
- `md2json`: Generates JSON file from directory of Markdown files.
- `project-types`: Displays available project types.
- `serve`: Starts server at host and port.
- `tmpl-list`: List of saved templates.
- `tmpl-new`: Create a new template.

"""

__version__ = '1.9.7'
