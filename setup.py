#!/usr/bin/env python
"""The setup script."""

from setuptools import find_packages, setup

requirements = [
    "xlrd>=1.1.0",
    "requests>=2.22.0",
    "click>=7.0",
    "click-help-colors>=0.5",
    "pandas>=0.20.3",
    "openpyxl>=2.4.8",
    "pendulum>=1.3.2",
    "pydantic>=0.27",
    "ftfy>=5.5.1",
]

setup_requirements = ["pytest-runner", "setuptools>=38.6.0", "wheel>=0.31.0"]

test_requirements = ["pytest", "responses", "pytest-sugar"]

with open("README.md") as infile:
    long_description = infile.read()

setup(
    name="hexpy",
    version="0.6.1",
    description="Python Client for Crimson Hexagon API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Colin Sullivan",
    author_email="csullivan@crimsonhexagon.com",
    url="https://sullivancolin.github.io/hexpy/",
    packages=find_packages(where="src", include=["hexpy"]),
    package_dir={"": "src"},
    package_data={"hexpy": ["py.typed"]},
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
