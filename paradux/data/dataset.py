#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#


def _parseDatasetJson(j):
    """
    Helper function to parse a JSON dataset definition into an instance of Dataset

    j: JSON fragment
    return: instance of Dataset
    """
    name        = j['name']        # required
    description = j['description'] if 'description' in j else None
    sourceJ     = j['source']      # required

    source       = _parseSourceDataLocationJson(sourceJ)
    destinations = []

    if 'destinations' in j:
        for destinationJ in j['destinations']:
            destination = _parseDestinationDataLocationJson(destinationJ)
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
        
