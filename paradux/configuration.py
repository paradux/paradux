#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import json
from paradux.configurationreport import ConfigurationReport, ConfigurationReportItem, Level
import paradux.logging
import re


def parse_json(filename):
    """
    Parse a configuration JSON file and return a Configuration object.
    This assumes the JSON is well-formed syntactically and semantically.

    filename: name of the JSON file to parse
    return: the Configuration object
    """
    with open(filename, 'r') as file:
        jsonText = file.read()

    withoutComments = re.sub(r'(?<!\\)#.*', '', jsonText)
    j = json.loads(withoutComments)

    return Configuration(jsonText)


def analyze_json(filename):
    """
    Analyze a potential configuration JSON file and return a
    ConfigurationReport object.

    filename: name of the JSON file to parse
    return: the ConfigurationReport object
    """
    items = []

    with open(filename, 'r') as file:
        jsonText = file.read()

    withoutComments = re.sub(r'(?<!\\)#.*', '', jsonText)
    j = json.loads(withoutComments)

    items.append( ConfigurationReportItem( Level.NOTICE, "Hi mom" ))

    return ConfigurationReport(items)
    

def default():
    """
    Obtain the default, empty, Configuration.

    return: the ConfigurationReport object
    """
    return Configuration(
"""{
    "datasets" : [
#        {
#            "name" : "home-myself",
#            "description" : "my own home directory",
#
#
#            "source" : {
#                "description" : "my own home directory on my laptop",
#                "url" : "rsync+ssh://laptop.local/home/myself",
#                "credentials" : {
#                    "ssh-user" : "me",
#                    "ssh-key"  : "ssh-rsa ..."
#                }
#            },
#
#            "destinations" : [
#                {
#                    "name" : "Apple Time Capsule",
#                    "location" : "Home office",
#                    "frequency" : "automatic"
#                },
#                {
#                    "name" : "Amazon S3",
#                    "url" : "s3://mybucket/home-myself",
#                    "credentials" : {
#                        "aws-access-key" : "Axxx",
#                        "aws-secret-key" : "Axxx"
#                    },
#                    "frequency" : 86400,
#                    "encryption" : {
#                        "gpg-keyid" : "..."
#                    }
#                }
#            ]
#        }
    ],
    "stewards" : [
#        {
#            "name": "John Doe"
#        }
    ]
}
""")

    
class Configuration:
    def __init__(self, jsonText) :
        self.jsonText = jsonText # We preserve the source, so we can keep comments around

    def asJson(self):
        """
        Obtain this Configuration as JSON
        """
        return self.jsonText


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
        

        conf = paradux.configuration.default()
