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

        settings.cleanup()

        # Export into a private temp directory
        tmpDir  = tempfile.mkdtemp(prefix='paradux-')
        tmpFile = tmpDir + '/paradux.img'
        settings.exportMetadataToFile(tmpFile)

        uploadCount = 0
        for metadataLocation in metadataLocations:
            if settings.uploadToDataLocation(tmpFile, metadataLocation):
                uploadCount += 1

        if uploadCount == 0:
            paradux.logging.error( 'No uploads performed; you cannot recover in case of a personal data disaster' )
        else:
            print( 'Published to ' + str(uploadCount) + ' locations.' )

    finally:
        settings.cleanup() # This probably will noop because we did it before, but might not in case of an error

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
