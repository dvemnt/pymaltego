#!/usr/bin/env python
# coding=utf-8

from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '1.1.5'

BASE_DIR = path.abspath(path.dirname(__file__))

PACKAGES = [
    'pymaltego'
]

REQUIRES = [
    'lxml'
]

with open(path.join(BASE_DIR, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pymaltego',
    version=VERSION,
    packages=PACKAGES,
    install_requires=REQUIRES,
    description='Package for developing Maltego Transforms',
    long_description=LONG_DESCRIPTION,
    author='Vitalii Maslov',
    author_email='me@pyvim.com',
    url='https://github.com/pyvim/pymaltego',
    download_url='https://github.com/pyvim/pyvim/tarball/master',
    license='MIT',
    keywords='Maltego, transforms',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
