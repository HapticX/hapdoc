from setuptools import setup, find_packages

setup(
    name='hapdoc',
    version='0.1',
    packages=find_packages(),
    py_modules=['hapd'],
    install_requires=['click', 'colorama'],
    entry_points={
        'console_scripts': [
            'hapdoc = hapdoc.hapd:hapdoc'
        ]
    }
)
