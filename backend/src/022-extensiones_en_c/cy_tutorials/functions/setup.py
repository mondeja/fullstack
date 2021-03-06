#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("funciones_cy",
              sources=["funciones_cy.pyx"],
    ),
]

setup(ext_modules=cythonize(ext_modules))

"""
Para compilar:
python3 setup.py build_ext -i
"""
