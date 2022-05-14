#!/usr/bin/env python3
from __future__ import unicode_literals
from setuptools import setup
from setuptools import find_packages


def read_description(local_current_package):
    module_doc = local_current_package.__doc__.splitlines()
    result = ""
    for line in module_doc:
        if line:
            result = line
            break
    return result


current_package = __import__('ytrss')

data_files = []

setup(
    name=current_package.__title__,
    version=current_package.__version__,
    license=current_package.__license__,
    author=current_package.__author__,
    author_email=current_package.__author_email__,
    description=read_description(current_package),
    python_requires='>={}.{}'.format(*current_package.__required_python__),
    long_description=open("README.rst").read(),
    url=current_package.__url__,
    project_urls={
        "Source": "https://github.com/rafyco/ytrss",
        "Tracker": "https://github.com/rafyco/ytrss/issues",
        "Changelog": "https://github.com/rafyco/ytrss/blob/master/dosc/changelog.rst",
        "Documentation": "https://ytrss.readthedocs.io"
    },
    packages=find_packages(),
    include_package_data=True,
    package_dir={'ytrss': 'ytrss'},
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
        'pyyaml',
        'astroid ~= 2.5',
        'jinja2 ~= 3.0.3',
        'youtube_dl ~= 2021.12.17',
        'locks ~= 0.1.1'
    ],
    extras_require={
        "optional": [
            "argcomplete"
        ],
        "unittests": [
            "pytest"
        ],
        "style": [
            "pylint == 2.5.3",
            "pep8 == 1.7.1",
            "pycodestyle == 2.8.0"
        ],
        "typing": [
            "mypy == 0.910",
            "types-PyYAML == 6.0"
        ],
        "documentation": [
            "Sphinx == 4.3.1",
            "sphinx-epytext == 0.0.4",
            "sphinx-autorun == 1.1.1"
        ]
    },
    entry_points={
        'console_scripts': [
            'ytrss = ytrss.client:main',
        ]
    },
    command_options={
        'build_spninx': {
            'project': ('setup.py', current_package.__title__),
            'version': ('setup.py', current_package.__version__),
            'release': ('setup.py', current_package.__version__),
            'source_dir': ('setup.py', 'docs')
        }
    },
    platforms="Any",
    keywords="youtube, console, download, rss, mp3, service"
)
