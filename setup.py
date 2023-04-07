"""
Provides setup script
"""
from os import path, makedirs
from setuptools import setup, find_packages


# Load readme
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


# Write default template in Home directory
with open('hapdoc/templates/vitepress/index.html', 'r', encoding='utf-8') as file:
    default_template = file.read()
directory = path.join(path.expanduser('~'), 'HapticX', 'hapdoc', 'templates', 'default')
if not path.exists(directory):
    makedirs(directory)
with open(path.join(directory, 'index.html'), 'w', encoding='utf-8') as file:
    file.write(default_template)


setup(
    name='hapdoc',
    description='autodoc tool for everything',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ethosa',
    author_email='social.ethosa@gmail.com',
    maintainer='HapticX',
    maintainer_email='hapticx.company@gmail.com',
    url='https://github.com/HapticX/hapdoc',
    version='1.9.3',
    packages=find_packages(),
    py_modules=['hapdoc'],
    install_requires=['click', 'fastapi', 'uvicorn', 'jinja2'],
    package_data={
        'hapdoc': ['*.html']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hapdoc = hapdoc.hapdoc:hapdoc'
        ]
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation'
    ]
)
