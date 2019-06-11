#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import os
import os.path
import paradux
import paradux.logging
import tempfile

def run(args, settings) :
    """
    Run this command.

    args: parsed command-line arguments
    settings: settings for this paradux instance
    """
    tmpDir = None
    try :
        settings.mountImage()

        metadataLocations = settings.getMetadataLocationsConfiguration().getMetadataLocations()
        if len(metadataLocations) == 0:
            paradux.logging.fatal( "No metadata locations have been defined. To configure, run 'paradux edit-metadata-locations'." )

        # Export into a private temp directory
        tmpDir  = tempfile.mkdtemp(prefix='paradux-')
        tmpFile = tmpDir + '/paradux.img'
        settings.exportMetadataToFile(tmpFile)

        for metadataLocation in metadataLocations:
            settings.uploadToDataLocation(tmpFile, metadataLocation)

    finally:
        settings.cleanup()

        if tmpDir is not None and os.path.isdir(tmpDir):
            for f in os.listdir(tmpDir):
                os.remove( tmpDir + '/' + f )
            os.rmdir(tmpDir)

    return 0


def addSubParser(parentParser, cmdName) :
    """
    Enable this command to add its own command-line options
    parentParser: the parent argparse parser
    cmdName: name of this command
    """
    parser = parentParser.add_parser( cmdName, help='Publish the paradux metadata to the defined metadata locations.' )
