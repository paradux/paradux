#!/usr/bin/python
#
# The central entry point into paradux.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import importlib
import os.path
import paradux.commands
import paradux.settings
from paradux.logging import FatalException
import paradux.utils
from pkg_resources import get_distribution
import secrets
import sys


def run():
    """
    Main entry point into Paradux
    """
    cmdNames = paradux.utils.findSubmodules(paradux.commands)

    parser = argparse.ArgumentParser()
    parser.add_argument('--directory',     action='store',       default=paradux.settings.DEFAULT_DIRECTORY, help='Directory containing the paradux data.' )
    parser.add_argument('-v', '--verbose', action='count',       default=0,  help='Display extra output. May be repeated for even more output.')
    parser.add_argument('--debug',         action='store_const', const=True, help='Suspend execution at certain points for debugging' )
    cmdParsers = parser.add_subparsers( dest='command', required=True )

    cmds = {}
    for cmdName in cmdNames:
        mod = importlib.import_module('paradux.commands.' + cmdName)
        mod.addSubParser( cmdParsers, cmdName )
        cmds[cmdName] = mod

    args,remaining = parser.parse_known_args(sys.argv[1:])
    cmdName = args.command

    paradux.logging.initialize(args.verbose, args.debug)

    if len(remaining)>0 :
        parser.print_help()
        exit(0)

    cmdName = args.command

    settings = paradux.settings.create(args)

    if cmdName in cmdNames:
        try :
            ret = cmds[cmdName].run(args, settings)
            exit( 0 if ret == 1 else 1 )

        except Exception as e:
            paradux.logging.fatal( str(type(e)), '--', e )

    else:
        paradux.logging.fatal('Sub-command not found:', cmdName, '. Add --help for help.' )


def run_not_implemented(args,conf):
    paradux.logging.fatal('Not implemented yet! Sorry. Want to help? https://github.com/paradux')


def version():
    """
    Obtain the current paradux version

    return: version string
    """

    ret = get_distribution('paradux').version
    print( "XXX version is " + ret )
    return ret
