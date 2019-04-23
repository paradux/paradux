#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from enum import Enum

class Level(Enum):
    """
    Defines the level of item in a report
    """

    ERROR   = ( 1, 'ERROR'   )
    WARNING = ( 2, 'WARNING' )
    NOTICE  = ( 3, 'NOTICE'  )

    def __init__(self, level, myname):
        self.level  = level
        self.myname = myname

    def __str__(self):
        return self.myname


class ReportItem:
    """
    A single item in a Report.
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
        return self.message
        # return str(self.level) + self.message
        # return "{0:7s}: {1:s}".format(str(self.level), self.message)
        

class Report:
    """
    The set of errors and warnings created by analyzing a (potential)
    Configuration.
    """

    def __init__(self,reportItems = []):
        self.reportItems = reportItems


    def isAllOk(self):
        """
        Return True if this report reports no issues.

        return: True or False
        """
        return len(self.reportItems) == 0


    def asText(self):
        """
        Return this ConfigurationReport as plain text that can be show
        to the user.

        return: text
        """
        ret = "\n".join( map( lambda item : item.asText(), self.reportItems ))
        return ret
            
