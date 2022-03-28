#!/usr/bin/env python3
from __future__ import unicode_literals
import sys
from setuptools import setup
from setuptools import find_packages


def read_description(module_name):
    module_doc = __import__(module_name).__doc__.splitlines()
    result = ""
    for line in module_doc:
        if line:
            result = line
            break
    return result


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# TODO: change package name
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of template-python-package requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have Python {}.{} or newer, then try again:

    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install template-python-package 

""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON + REQUIRED_PYTHON)))
    sys.exit(1)

package_name = 'template-python-package'
version = __import__(package_name).version

data_files = []

setup(
    name=package_name,
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description=read_description(package_name),
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    long_description=open("README.rst").read(),
    url="https://github.com/rafyco/template-python-package",
    project_urls={
        "Source": "https://github.com/rafyco/template-python-package",
        "Tracker": "https://github.com/rafyco/template-python-package/issues",
        "Documentation": "https://template-python-package.readthedocs.io/en/latest/"
    },
    packages=find_packages(),
    include_package_data=True,
    package_dir={'template-python-package': 'template-python-package'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
    ],
    extras_require={
        "unittests": [
            "pytest"
        ],
        "style": [
            "pylint == 2.5.3",
            "pep8 == 1.7.1",
            "pycodestyle == 2.8.0"
        ],
        "typing": [
            "mypy == 0.910"
        ],
        "documentation": [
            "Sphinx == 4.3.1",
            "sphinx-epytext == 0.0.4"
        ]
    },
    command_options={
        'build_spninx': {
            'project': ('setup.py', package_name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs')
        }
    },
    platforms="Any",
    keywords=""
)
