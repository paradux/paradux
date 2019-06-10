#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import os.path
import paradux
import paradux.utils


def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    if args.json and os.path.isfile(args.json):
        raise FileExistsError(args.json)

    try :
        settings.mountImage()

        stewardPackages = settings.getStewardPackages()

        # stdout only right now

        if args.stewardid:
            if args.stewardid in stewardPackages:
                toExport = dict()
                toExport[args.stewardid] = stewardPackages[args.stewardid]
            else:
                paradux.logging.fatal( 'Cannot find steward with id:', args.stewardid )

        else:
            toExport = stewardPackages

        if args.json:
            j = []
            for stewardId, stewardPackage in toExport.items():
                j.append(stewardPackage.asJson())

            paradux.utils.writeJsonToFile(args.json, j, 0o600 )

        elif len(toExport) > 0:
            print( "\n=== CUT HERE ===\n\n".join(
                    map(lambda t : "--- Steward Package start ---\n\n"
                                   + t.asText()
                                   + "\n--- Steward Package end ---\n",
                        toExport.values() )))

        else:
            print( "No stewards have been defined. Not exporting any steward packages." )

    finally:
        settings.cleanup()

    return 0


def addSubParser(parentParser, cmdName) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Export the steward packages.' )
    parser.add_argument( '--json',      action='store', help='Export to a JSON file instead of plain text to the terminal.' )
    parser.add_argument( '--stewardid', action='store', help='ID of the steward.' )
    # FUTURE: parser.add_argument( '--paper',     action='store_const', const=True, help='Print to paper instead of USB sticks.' )
    # FUTURE: parser.add_argument( '--usbsticks', action='store_const', const=True, help='Save to USB sticks instead of printing to paper.' )

