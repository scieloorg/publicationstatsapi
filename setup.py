#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'thriftpy',
    'requests'
]

setup(
    name="publicationstatsapi",
    version="1.2.1",
    description="SciELO PublicationStats service SDK for Python",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    url="http://github.com/scieloorg/publicationstatsapi",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    test_suite='tests',
    install_requires=install_requires
)
