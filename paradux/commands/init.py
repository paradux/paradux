#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import paradux
import paradux.logging
import random
import re


def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    try :
        nbits  = 512
        recoverySecret = random.SystemRandom().randint(0, 1<<nbits)

        paradux.logging.trace( 'recovery secret:', recoverySecret)

        settings.checkCanCreateImage()
        settings.createAndMountImage(recoverySecret)

        settings.populateWithInitialData(args.min_stewards, nbits, recoverySecret)

    finally:
        settings.cleanup()

    return 0



def addSubParser(parentParser, cmdName) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """

    def valid_disk_size(value):
        """
        Check and convert a string representing a disk size into an integer
        representing a disk size.

        value: the disk size string
        return: disk size integer
        throws argparse.ArgumentTypeException: if a syntax error occurred
        """
        factors = {
            'k'  : 1000,
            'ki' : 1024,
            'm'  : 1000 * 1000,
            'mi' : 1024 * 1024,
            'g'  : 1000 * 1000 * 1000,
            'gi' : 1024 * 1024 * 1024
        }

        m = re.match(r'(\d+(\.\d*)?)\s*(([kmg]i?)b?)?', value, re.IGNORECASE)
        if m:
            ret = float(m.group(1))
            mult = m.group(3).lower()
            if mult in factors:
                ret *= factors[mult]
            else:
                raise argparse.ArgumentTypeError('Unknown multiplier: ' + mult)

            ret = int(ret)
            if ret < 20 * 1000 * 1000:
                raise argparse.ArgumentTypeError('Must be at least 20MB')
            return ret
        else:
            raise argparse.ArgumentTypeError('Specify image size like this: 123 MiB')

    def min_stewards(value):
        """
        Enforce a minimum of 2 stewards.

        value: specified number of minimum stewards
        return: minimum number of stewards
        throws argparse.ArgumentTypeException: out of range

        """
        if value >= 2:
            raise argparse.ArgumentTypeError('Number of stewards must be at least 2')

        return value


    parser = parentParser.add_parser(cmdName, help='Sets up a Paradux installation for the first time.')
    parser.add_argument('--image-size',   type=valid_disk_size, default='24 M', help='Size of the LUKS disk image for secrets.')
    parser.add_argument('--min-stewards', type=min_stewards,    default=3,      help='Number of stewards required to recover (2 or more).')

