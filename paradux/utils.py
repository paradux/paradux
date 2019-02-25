#!/usr/bin/python
#
# Collection of utility functions.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import os
import pkgutil
import paradux.log

def findSubmodules(packageName) :
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(packageName.__path__):
        ret.append(modname)
    return ret

def myexec(cmd):
    paradux.log.trace('myexec: ' + cmd )
    ret = os.system(cmd)
    return ret
