#!/usr/bin/python
#
# Sub-command that lists all currently known sub-commands.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import importlib
import paradux.utils

def run(conf) :
    """
    Run this command with configuration conf
    """
    cmds = paradux.utils.findSubmodules(paradux.commands)
    print('paradux sub-commands:')
    for cmd in sorted(cmds) :
        print( '    ' + cmd )
        try:
            mod=importlib.import_module('paradux.commands.' + cmd)
            desc = mod.description()
            desc = desc.strip().replace( '!\s*\n\s*!', '\n        ' );
            print( '        ' + desc )

        except AttributeError:
            print()

def description() :
    return """
Prints out the known sub-commands.
"""
