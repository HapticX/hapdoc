from setuptools import setup, find_packages

with open('./readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hapdoc',
    description='autodoc tool for everything',
    long_description=long_description,
    author='Ethosa',
    author_email='social.ethosa@gmail.com',
    maintainer='HapticX',
    maintainer_email='hapticx.company@gmail.com',
    url='https://github.com/HapticX/hapdoc',
    version='0.5',
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
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Documentation'
        'Topic :: Software Development :: Documentation'
    ]
)
