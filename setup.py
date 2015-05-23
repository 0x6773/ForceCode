#!/usr/bin/env python2

from distutils import log
from setuptools import setup, find_packages
from src import __version__
import os

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        """
        Allows for clean uninstall
        """
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names

def packages():
    pkg = find_packages()
    return pkg

README = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name = 'ForceCode',
    version = __version__,
    author = 'Govind Sahai',
    author_email = 'gsiitbhu@gmail.com',
    description = ('codeforces helper'),
    long_description = open(README).read(),
    license = 'MIT',
    keywords = 'codeforces forcecoders',
    url = 'http://github.com/mafiya69/ForceCoders',
    packages=packages(),
    scripts = ['forcecode/forcecode.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix'
    ],
)
