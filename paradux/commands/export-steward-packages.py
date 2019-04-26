#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import paradux
import paradux.utils


def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    try :
        settings.mountImage()

        stewardPackages = settings.getStewardPackages()

        # stdout only right now
        if args.json:
            j = []
            for stewardPackage in stewardPackages:
                j.append(stewardPackage.asJson())

            paradux.utils.writeJsonToStdout(j)

        elif len(stewardPackages) > 0:
            print( "\n=== CUT HERE ===\n\n".join(
                    map(lambda t : "--- Steward Package start ---\n\n"
                                   + t.asText()
                                   + "\n--- Steward Package end ---\n",
                        stewardPackages)))

        else:
            print( "No stewards have been defined. Not exporting any steward packages." )

    finally:
        settings.cleanup()

    return True


def addSubParser(parentParser, cmdName) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Export the steward packages.' )
    parser.add_argument( '--json',     action='store_const', const=True, help='Export JSON instead of plain text.' )
    # FUTURE: parser.add_argument( '--paper',     action='store_const', const=True, help='Print to paper instead of USB sticks.' )
    # FUTURE: parser.add_argument( '--usbsticks', action='store_const', const=True, help='Save to USB sticks instead of printing to paper.' )
    # FUTURE: parser.add_argument( '--steward',   action='store',                   help='Name of the steward.' )

