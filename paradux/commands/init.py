#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import paradux
import re


def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    try :
        settings.createAndMountImage()

        settings.initConfiguration()

    finally:
        settings.cleanup()

    return True
    


def addSubParser( parentParser, cmdName ) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """

    def valid_disk_size(value):
        """
        Check and convert valid disk image size
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
            
        
    parser = parentParser.add_parser(cmdName, help='Sets up a Paradux installation for the first time.')
    parser.add_argument('--image-size', type=valid_disk_size, default='24 M', help='Size of the LUKS disk image for secrets.')

