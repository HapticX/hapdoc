from setuptools import setup, find_packages

setup(
    name='hapdoc',
    description='autodoc tool for everything',
    version='0.1',
    packages=find_packages(),
    py_modules=['hapdoc'],
    install_requires=['click', 'colorama', 'fastapi', 'uvicorn'],
    entry_points={
        'console_scripts': [
            'hapdoc = hapdoc.hapdoc:hapdoc'
        ]
    }
)
