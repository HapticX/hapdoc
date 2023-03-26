"""
Provides setup script
"""
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


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
    version='1.5.0',
    packages=find_packages(),
    py_modules=['hapdoc'],
    install_requires=['click', 'colorama', 'fastapi', 'uvicorn'],
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
