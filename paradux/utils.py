#!/usr/bin/python
#
# Collection of utility functions.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import os
import pkgutil
import paradux.logging
import subprocess


def findSubmodules(package) :
    """
    Find all submodules in the named package

    package: the package
    return: array of module names
    """
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        ret.append(modname)
    return ret


def myexec(cmd,stdin=None):
    """
    Wrapper around executing sub-commands, so we can log what is happening.

    cmd: the command to be executed by the shell
    stdin: content to be piped into the command, if any
    return: return code
    """
    paradux.logging.debugAndSuspend('myexec:', cmd, 'with stdin:', stdin)
    paradux.logging.trace(cmd, 'None' if stdin==None else len(stdin))

    ret = subprocess.run(cmd, shell=True, input=stdin)
    return ret.returncode

