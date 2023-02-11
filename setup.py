from setuptools import setup, find_packages

with open('./readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hapdoc',
    description='autodoc tool for everything',
    long_description=long_description,
    version='0.3',
    packages=find_packages(),
    py_modules=['hapdoc'],
    install_requires=['click', 'colorama', 'fastapi', 'uvicorn'],
    entry_points={
        'console_scripts': [
            'hapdoc = hapdoc.hapdoc:hapdoc'
        ]
    }
)
