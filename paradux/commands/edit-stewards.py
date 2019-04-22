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

    conf = None
    try :
        settings.mountImage()

        conf = settings.getStewardsConfiguration()

        while True:
            report = conf.editTempAndReport()

            if report.isAllOk():
                conf.promoteTemp()
                break # we are done
                
            print( report.asText() )

            if input( 'Continue editing? Y/N: ' ).lower() == 'n':
                break

    finally:
        if conf != None:
            conf.abortTemp()
        settings.cleanup()

    return True


def addSubParser(parentParser, cmdName) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Edit the stewards in a paradux configuration.' )

