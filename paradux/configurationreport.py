#!/usr/bin/python
#
# Collects the settings for this instance of paradux
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from enum import Enum

class Level(Enum):
    ERROR   = ( 1, 'ERROR'   )
    WARNING = ( 2, 'WARNING' )
    NOTICE  = ( 3, 'NOTICE'  )

    def __init__(self, level, name):
        self.level = level
        self.name  = name

    def __str__(self):
        return self.name


class ConfigurationReportItem:
    """
    A single item in a ConfigurationReport.
    """
    def __init__(self, level, message):
        """
        Constructor.

        level: the level of the item
        message: the message
    """
    self.level   = level
    self.message = message


    def asText(self):
        """
        Return as a text string that can be shown to the user

        return: text string
        """
        return "{0:7s}: {1:s}".format(self.level,self.message)
        

class ConfigurationReport:
    """
    The set of errors and warnings created by analyzing a (potential)
    Configuration.
    """

    def __init__(self,reportItems = []):
        self.reportItems = reportItems


    def isAllOk(self):
        return len(self.reportItems) == 0


    def asText(self):
        """
        Return this ConfigurationReport as plain text that can be show
        to the user.

        return: text
        """
        ret = "\n".join( map( lambda item : item.asText(), self.reportItems ))
        return ret
            
