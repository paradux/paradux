#!/usr/bin/python
#
# Collection of utility functions.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import pkgutil

def findSubmodules(packageName) :
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(packageName.__path__):
        ret.append(modname)
    return ret

