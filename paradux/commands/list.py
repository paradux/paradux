#!/usr/bin/python
#
# Sub-command that lists all currently known sub-commands.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.utils

def run() :
    cmds = paradux.utils.findSubmodules(paradux.commands)
    print('List of known sub-commands:')
    for cmd in sorted(cmds) :
        print( '    ' + cmd )
