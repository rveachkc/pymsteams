#!/usr/bin/env python

import os
import sys

from m2r import parse_from_file
from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.6"

def readme():
    """ print long description """
    return parse_from_file('README.md')
    #return pypandoc.convert('README.md', 'rst')
    #with open('README.md') as f:
    #    return f.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="pymsteams",
    version=VERSION,
    description="Format messages and post to Microsoft Teams.",
    long_description=readme(),
    url="https://github.com/rveachkc/pymsteams",
    author="Ryan Veach",
    author_email="rveach@gmail.com",
    license="Apache",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Groupware",
    ],
    keywords=['Microsoft', 'Teams'],
    packages=['pymsteams'],
    install_requires=[
        'requests==2.20.0',
    ],
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
