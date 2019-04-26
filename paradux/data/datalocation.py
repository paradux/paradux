#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging


def parseSourceDataLocationJson(j):
    """
    Helper function to parse a JSON source data location definition into an instance
    of SourceDataLocation

    j: JSON fragment
    return: instance of SourceDataLocation
    """
    paradux.logging.trace('parseSourceDataLocationJson')

    name        = j['name']                               if 'name'        in j else None
    description = j['description']                        if 'description' in j else None
    url         = j['url']                                # required
    credentials = _parseCredentialsJson(j['credentials']) if 'credentials' in j else None

    return SourceDataLocation(name, description, url, credentials)


def parseDestinationDataLocationJson(j):
    """
    Helper function to parse a JSON destination data location definition into an
    instance of DestinationDataLocation

    j: JSON fragment
    return: instance of DestinationDataLocation
    """
    paradux.logging.trace('parseDestinationDataLocationJson')

    name        = j['name']                               # required
    description = j['description']                        if 'description' in j else None
    url         = j['url']                                # required
    credentials = _parseCredentialsJson(j['credentials']) if 'credentials' in j else None
    frequency   = _parseFrequencyJson(  j['frequency']  ) if 'frequency'   in j else None
    encryption  = _parseEncryptionJson( j['encryption'] ) if 'encryption'  in j else None

    return DestinationDataLocation(name, description, url, credentials, frequency, encryption)


def _parseFrequencyJson(j):
    # FIXME
    return None


def _parseEncryptionJson(j):
    # FIXME
    return None


class DataLocation:
    """
    Represents the location of a bunch of data somewhere.

    name: name used to refer to it within paradux (required)
    description: text that reminds the user about this data location (optional)
    url: how to access this data location (required)
    credentials: access credentials (optional)
    """
    def __init__(self, name, description, url, credentials):
        self.name        = name
        self.description = description
        self.url         = url
        self.credentials = credentials


class SourceDataLocation(DataLocation):
    """
    A DataLocation that is used as a source in a Dataset.
    """
    def __init__(self, name, description, url, credentials):
        super().__init__(name, description, url, credentials)


class DestinationDataLocation(DataLocation):
    """
    A DataLocation that is used as a destination in a Dataset.
    """
    def __init__(self, name, description, url, credentials, frequency, encryption_info):
        super().__init__(name, description, url, credentials, frequency, encryption_info )

