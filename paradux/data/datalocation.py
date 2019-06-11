#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.data.credential
import paradux.logging
from urllib.parse import urlparse


def parseSourceDataLocationJson(j):
    """
    Helper function to parse a JSON source data location definition into an instance
    of SourceDataLocation

    j: JSON fragment
    return: instance of SourceDataLocation
    """
    paradux.logging.trace('parseSourceDataLocationJson')

    name        = j['name']           if 'name'        in j else None
    description = j['description']    if 'description' in j else None
    url         = _parseUrl(j['url']) # required

    credentials = paradux.data.credential.parseCredentialsJson(j['credentials'], url) if 'credentials' in j else None

    return SourceDataLocation(name, description, url, credentials)


def parseDestinationDataLocationJson(j):
    """
    Helper function to parse a JSON destination data location definition into an
    instance of DestinationDataLocation

    j: JSON fragment
    return: instance of DestinationDataLocation
    """
    paradux.logging.trace('parseDestinationDataLocationJson')

    name        = j['name']                               if 'name'        in j else None
    description = j['description']                        if 'description' in j else None
    url         = _parseUrl(j['url'])                     if 'url'         in j else None
    frequency   = _parseFrequencyJson(  j['frequency']  ) if 'frequency'   in j else None
    encryption  = _parseEncryptionJson( j['encryption'] ) if 'encryption'  in j else None

    credentials = paradux.data.credential.parseCredentialsJson(j['credentials'], url) if 'credentials' in j else None

    return DestinationDataLocation(name, description, url, credentials, frequency, encryption)


def parseMetadataLocationJson(j):
    """
    Helper function to parse a JSON metadata location into an instance
    of MetadataLocation

    j: JSON fragment
    return: instance of MetadataLocation
    """
    paradux.logging.trace('parseMetadataLocationJson')

    name        = j['name']           if 'name'        in j else None
    description = j['description']    if 'description' in j else None
    url         = _parseUrl(j['url']) # required
    credentials = paradux.data.credential.parseCredentialsJson(j['credentials'], url) if 'credentials' in j else None

    return MetadataLocation(name, description, url, credentials)


def _parseUrl(u):
    """
    Parse a URL.

    u: URL as string
    return: ParseResult
    """
    return urlparse(u)


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
    url: how to access this data location (required), as a parsed URL
    credentials: access credentials (optional)
    """
    def __init__(self, name, description, url, credentials):
        self.name        = name
        self.description = description
        self.url         = url
        self.credentials = credentials


    """
    Convert to string, to be shown to the user

    return: string
    """
    def __str__(self):
        if self.url is not None:
            return self.url.geturl()

        if self.name is not None:
            return self.name

        return '<underspecified data location>'


class SourceDataLocation(DataLocation):
    """
    A DataLocation that is used as a source in a Dataset.
    """
    def __init__(self, name, description, url, downloadCredentials):
        super().__init__(name, description, url, downloadCredentials)


class DestinationDataLocation(DataLocation):
    """
    A DataLocation that is used as a destination in a Dataset.

    frequency: specifies how frequently a backup is created to this destination
    encryption_info: specifies how the backup is encrypted
    """
    def __init__(self, name, description, url, uploadCredentials, frequency, encryption_info):
        super().__init__(name, description, url, uploadCredentials )

        self.frequency       = frequency
        self.encryption_info = encryption_info


class MetadataLocation(DataLocation):
    """
    A DataLocation that is used as place where to deposit copies of
    the paradux metadata
    """
    def __init__(self, name, description, url, uploadCredentials):
        super().__init__(name, description, url, uploadCredentials)

