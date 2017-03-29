#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    author="Diogo Fernandes",
    author_email="diogoabfernandes@gmail.com",
    description="A Python RESTful API framework for online malware and URL analysis services.",
    name="malsub",
    version="1.2",
    license="see LICENSE",
    packages=find_packages(),
    scripts=["malsub"],
    url="https://github.com/diogo-fernan/malsub",
)
