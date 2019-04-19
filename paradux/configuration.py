#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging

def parse_json(filename):
    """
    Parse a configuration JSON file and return a Configuration object.
    This assumes the JSON is well-formed syntactically and semantically.

    filename: name of the JSON file to parse
    return: the Configuration object
    """
    return Configuration() # FIXME


def analyze_json(filename):
    """
    Analyze a potential configuration JSON file and return a
    ConfigurationReport object.

    filename: name of the JSON file to parse
    return: the ConfigurationReport object
    """
    items = [] # FIXME
    return ConfigurationReport(items)
    

class Configuration:
    @classmethod

    def __init__(self, ...) :


    def asText(self):
        """
        Obtain a description of this Configuration as text that can
        be show to the user.

        return: text
        """
        paradux.logging.fatal('FIXME')


    def getStewardPackages(self):
        """
        Obtain the Steward packages.

        return: array of StewardPackage
        """
        paradux.logging.fatal('FIXME')
        
