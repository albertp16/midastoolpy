# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 21:40:29 2022

@author: alber
"""

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Midas Gen Tool - Python library'
LONG_DESCRIPTION = 'A package aid structural engineers using Midas Gen'

setup(
    name="midastoolpy",
    version=VERSION,
    author="albertp16 (Albert Pamonag)",
    author_email="<albertpamonag@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
