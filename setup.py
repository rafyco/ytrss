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
        "Changelog": "https://github.com/rafyco/ytrss/blob/master/docs/changelog.rst",
        "Documentation": "https://ytrss.readthedocs.io"
    },
    packages=find_packages(),
    include_package_data=True,
    package_dir={'ytrss': 'ytrss'},
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Topic :: Multimedia :: Sound/Audio',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Video',
        'Typing :: Typed'
    ],
    install_requires=[
        'pyyaml',
        'astroid ~= 2.5',
        'jinja2 >= 3.0.3,< 3.2.0',
        'youtube_dl ~= 2021.12.17',
        'locks ~= 0.1.1',
        'mutagen ~= 1.45.1'
    ],
    extras_require={
        "optional": [
            "argcomplete"
        ],
        "unittests": [
            "pytest"
        ],
        "style": [
            "pylint == 2.14.0",
            "pep8 == 1.7.1",
            "pycodestyle == 2.8.0"
        ],
        "typing": [
            "mypy == 0.960",
            "types-PyYAML == 6.0.8"
        ],
        "documentation": [
            "Sphinx == 5.0.1",
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
