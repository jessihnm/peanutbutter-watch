#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import os
from setuptools import setup, find_packages


local_file = lambda *f: open(os.path.join(os.path.dirname(__file__), *f), "r").read()


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = "version"

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_file("peanutbutter_watch", "version.py")))
    return finder.version


install_requires = ["requests", "click", "bs4", "lxml", "cssselect", "coloredlogs"]


setup(
    name="peanutbutter-watch",
    version=read_version(),
    description="\n".join(
        ["Berlin Bike Watch is a simple scraper for the Berlin Police Website"]
    ),
    long_description=local_file("README.rst"),
    entry_points={
        "console_scripts": ["peanutbutter-watch = peanutbutter_watch.cli:main"]
    },
    url="https://github.com/gabrielfalcao/peanutbutter-watch",
    packages=find_packages(exclude=["*tests*"]),
    include_package_data=True,
    package_data={"peanutbutter_watch": "README.rst *.rst docs/* docs/source/*".split()},
    zip_safe=False,
    author="Gabriel Falcao",
    author_email="gabriel@nacaolivre.org",
    install_requires=install_requires,
    dependency_links=[],
)
