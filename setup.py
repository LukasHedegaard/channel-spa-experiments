#!/usr/bin/env python

from setuptools import find_packages, setup


def long_description():
    text = open("README.md", encoding="utf-8").read()
    # SVG images are not readable on PyPI, so replace them  with PNG
    text = text.replace(".svg", ".png")
    return text


def from_file(file_name: str = "requirements.txt", comment_char: str = "#"):
    """Load requirements from a file"""
    with open(file_name, "r") as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[: ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith("http"):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


setup(
    name="channel-spa-experiments",
    version="0.1.0",
    description="Research repository for LRP-based Structured Pruning",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Lukas Hedegaard, based on work of Seul-Ki Yeom",
    author_email="lukasxhedegaard@gmail.com",
    url="https://github.com/LukasHedegaard/LRP_pruning",
    install_requires=from_file("requirements.txt"),
    extras_require={"dev": from_file("requirements-dev.txt")},
    packages=find_packages(exclude=["test"]),
)
