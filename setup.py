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
      author='Johannes Ernst',
      license='AGPLv3',
      description='Recovery from maximum personal data disaster',
      url='http://github.com/paradux/paradux',
      packages=[
          'paradux',
          'paradux.commands',
          'paradux.configuration',
          'paradux.data',
          'paradux.datatransfer'
      ],
      zip_safe=True)
