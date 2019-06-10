#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux
from paradux.configuration import Configuration
from paradux.configuration.report import Level, Report, ReportItem
import paradux.data.steward
import paradux.utils


def saveInitial(fileName):
    """
    Save the initial JSON content of a StewardsConfiguration to this file.

    return: void
    """
    content = """{
    "stewards" : {
    }
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a StewardsConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    stewards = {}
    for stewardId, stewardJ in j['stewards'].items():
        steward = paradux.data.steward.parseStewardJson(stewardJ)
        stewards[stewardId] = steward

    return StewardsConfiguration(masterFile, tmpFile, stewards)


class StewardsConfiguration(Configuration):
    """
    Encapsulates the configuration information related to stewards.
    """
    def __init__(self, masterFile, tmpFile, stewards):
        """
        Constructor.

        stewards: dict of of Steward, keyed by id
        """
        super().__init__(masterFile, tmpFile)
        self.stewards = stewards


    def getStewards(self):
        """
        Return the Stewards as dict, keyed by Steward id.

        return: dict
        """
        return self.stewards


    def createReport(self,fileName):
        """
        Implementation for this subclass.
        """

        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)

            for stewardId, stewardJ in j['stewards'].items():
                steward = paradux.data.steward.parseStewardJson(stewardJ)

        except Exception as e:
            reportItems.append(ReportItem(Level.ERROR, str(type(e)) + ': ' + str(e)))
            paradux.logging.error(e)
        return Report(reportItems)


    def asText(self):
        """
        Show this StewardsConfiguration to the user in plain text.

        return: plain text
        """
        if len(self.stewards) == 0:
            t = """You currently have 0 stewards configured. To configure some, run 'paradux edit-stewards'\n"""

        else:
            t = "You currently have {0:d} steward(s) configured. They are:\n".format(len(self.stewards))
            for stewardId, steward in self.stewards.items():
                t += "* ID:             {0:s}\n".format( stewardId )
                t += "  Name:           {0:s}\n".format( steward.name )
                t += "  Address:        {0:s}\n".format( "<not set>" if steward.address      is None else steward.address )
                t += "  Contact e-mail: {0:s}\n".format( "<not set>" if steward.contactEmail is None else steward.contactEmail )
                t += "  Contact phone:  {0:s}\n".format( "<not set>" if steward.contactPhone is None else steward.contactPhone )
                t += "  Accepted:       {0:s}\n".format( "<not set>" if steward.acceptedTs   is None else paradux.utils.time2string(steward.acceptedTs))

        return t

