#!/usr/bin/env python
# coding=utf-8

from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '1.0.4'

here = path.abspath(path.dirname(__file__))

packages = [
    'pymaltego'
]

requires = [
    'lxml'
]

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='pymaltego',
    version=VERSION,
    packages=packages,
    install_requires=requires,
    description='Package for developing Maltego Transforms',
    long_description=long_description,
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
