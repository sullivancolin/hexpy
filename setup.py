#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'clint>=0.5.1', 'requests>=2.18.4', 'ratelimiter>=1.2.0', 'halo>=0.0.7',
    'click>=6.7'
]

setup_requirements = ['pytest-runner', 'setuptools-markdown']

test_requirements = ['pytest']

scripts_requirements = ["pandas>=0.20.3", "openpyxl>=2.4.8"]

setup(
    name='hexpy',
    version='0.1.0',
    description="Python Client for Crimson Hexagon API",
    long_description_markdown_filename='README.md',
    author="Colin Sullivan",
    author_email='csullivan@crimsonhexagon.com',
    url='https://github.com/sullivancolin/hexpy',
    packages=find_packages(include=['hexpy']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='hexpy',
    extras_require={'cli': scripts_requirements},
    entry_points={'console_scripts': [
        'hexpy = hexpy.hexpy:cli [cli]',
    ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers', 'Natural Language :: English',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements)