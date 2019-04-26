#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging
import paradux.data.datalocation

def parseDatasetJson(j):
    """
    Helper function to parse a JSON dataset definition into an instance of Dataset

    j: JSON fragment
    return: instance of Dataset
    """
    paradux.logging.trace('parseDatasetJson')

    name        = j['name']        # required
    description = j['description'] if 'description' in j else None
    sourceJ     = j['source']      # required

    source       = paradux.data.datalocation.parseSourceDataLocationJson(sourceJ)
    destinations = []

    if 'destinations' in j:
        for destinationJ in j['destinations']:
            destination = paradux.data.datalocation.parseDestinationDataLocationJson(destinationJ)
            destinations.append(destination)

    return Dataset(name,description,source,destinations)


class Dataset:
    """
    Encapsulates everything there's to be said about a Dataset.
    """
    def __init__(self, name, description, source, destinations):
        """
        Constructor.

        name: the name of this Dataset
        description: any description for this Dataset
        source: the sourceDataLocation for this Dataset
        destinations: the array of DestinationDataLocation for this Dataset
        """
        self.name         = name
        self.description  = description
        self.source       = source
        self.destinations = destinations

