#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import json
import paradux
import paradux.data.stewardshare
from paradux.shamir import ShamirSecretSharing
import sys

def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    print( "Enter recovery JSON, EOF when done:")

    recoveryJ = json.load(sys.stdin)

    mersenne     = None
    minStewards  = None
    shamirShares = []

    for stewardPackageJ in recoveryJ:
        if mersenne == None:
            mersenne = stewardPackageJ['mersenne']
        elif mersenne != stewardPackageJ['mersenne']:
            paradux.logging.fatal('Different mersenne values, cannot recover:', mersenne, stewardPackageJ['mersenne'])

        if minStewards == None:
            minStewards = stewardPackageJ['min-stewards']
        elif minStewards != stewardPackageJ['min-stewards']:
            paradux.logging.fatal('Different min-stewards values, cannot recover:', minStewards, stewardPackageJ['min-stewards'])

        shamirShares.append( paradux.data.stewardshare.parseShamirSecretShare( stewardPackageJ['stewardshare']['shamir-share']))

    if len(shamirShares) < minStewards:
        paradux.logging.fatal( 'Not enough stewards contributed their shares, cannot recover:', len(shamirShares), '<', minStewards )
    if len(shamirShares) > minStewards:
        paradux.logging.fatal( 'Too many stewards contributed their shares, only submit the ones to use:', len(shamirShares), '>', minStewards )
        
    shamir = ShamirSecretSharing(mersenne)
    recoverySecret = shamir.restore(shamirShares)

    try:
        settings.recoverSetEverydayPassphrase(recoverySecret)

    finally:
        settings.cleanup()

    return True


def addSubParser( parentParser, cmdName ) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Recover the paradux configuration from steward packages.' )
    parser.add_argument( '--json', action='store_const', const=True, required=True, help='Recover from JSON input at stdin (currently required(' )
