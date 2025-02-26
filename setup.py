#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='OnzeDeLegende',
    version='1.0.0',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires = [
      'flask',
      'requests',
      'bs4',
      'honcho',
      'pandas',
      'selenium',
      'datetime'
    ],
    extras_require={
        'dev': [
            'honcho',
            'pylint',
            'coverage'
        ]
    },
    classifier= [
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: POSIX :: Linux'
    ],
)
