#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import paradux


def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    try :
        settings.mountImage()

        conf = settings.getConfiguration()

        # stdout only right now
        for stewardPackage in conf.getStewardPackages():
            print("=== Steward Package start === CUT HERE ===")
            print(stewardPackage.asText())
            print("=== Steward Package end === CUT HERE ===")

    finally:
        settings.cleanup()

    return True


def addSubParser( parentParser, cmdName ) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Export the steward package for one or more stewards.' )
    # FUTURE: parser.add_argument( '--paper',     action='store_const', const=True, help='Print to paper instead of USB sticks.' )
    # FUTURE: parser.add_argument( '--usbsticks', action='store_const', const=True, help='Save to USB sticks instead of printing to paper.' )

