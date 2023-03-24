from setuptools import setup, find_packages

setup(
    name='hapdoc',
    description='autodoc tool for everything',
    author='Ethosa',
    author_email='social.ethosa@gmail.com',
    maintainer='HapticX',
    maintainer_email='hapticx.company@gmail.com',
    url='https://github.com/HapticX/hapdoc',
    version='1.0.1',
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
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation'
    ]
)
