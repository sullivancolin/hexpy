#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages

requirements = ['clint>=0.5.1', 'requests>=2.18.4', 'ratelimiter>=1.2.0']

setup_requirements = ['pytest-runner', 'setuptools-markdown']

test_requirements = ['pytest']

setup(
    name='hexpy',
    version='0.1.0',
    description="Python Client for Crimson Hexagon API",
    long_description_markdown_filename='README.md',
    author="Colin Sullivan",
    author_email='csullivan@crimsonhexagon.com',
    url='https://github.com/sullivancolin/hexpy',
    packages=find_packages(include=['hexpy']),
    entry_points={'console_scripts': ['hexpy=hexpy.cli:main']},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='hexpy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers', 'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements, )
