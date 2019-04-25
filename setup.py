#!/usr/bin/python
#
# Setup the package.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from setuptools import setup
import paradux

setup(name='paradux',
      version=paradux.version(),
      description='Recovery from maximum personal data disaster',
      url='http://github.com/paradux/paradux',
      packages=['paradux'],
      zip_safe=False,
      install_requires=['cryptography', 'secrets']])
