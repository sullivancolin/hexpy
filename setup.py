#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    "clint>=0.5.1",
    "xlrd>=1.1.0",
    "requests>=2.18.4",
    "halo>=0.0.7",
    "click>=6.7",
    "click-help-colors>=0.4",
    "pandas>=0.20.3",
    "openpyxl>=2.4.8",
    "pendulum>=1.3.2",
]

setup_requirements = ["pytest-runner", "setuptools>=38.6.0", "wheel>=0.31.0"]

test_requirements = ["pytest"]

with open("README.md") as infile:
    long_description = infile.read()

setup(
    name="hexpy",
    version="0.4.5",
    description="Python Client for Crimson Hexagon API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Colin Sullivan",
    author_email="csullivan@crimsonhexagon.com",
    url="https://sullivancolin.github.io/hexpy/",
    packages=find_packages(include=["hexpy"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    zip_safe=False,
    keywords="hexpy",
    entry_points={"console_scripts": ["hexpy = hexpy.hexpy:cli"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
