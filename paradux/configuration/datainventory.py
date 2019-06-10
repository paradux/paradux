#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.configuration import Configuration
from paradux.configuration.report import Level, Report, ReportItem
import paradux.data.datalocation
import paradux.utils


def saveInitial(fileName):
    """
    Save the initial JSON content of DataInventoryLocations to this file.

    return: void
    """
    content = """{
    "locations" : []
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a DataInventoryConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    dataInventoryLocations = []

    for locationJ in j['locations']:
        dataInventoryLocation = paradux.data.datalocation.parseDataInventoryLocationJson(locationJ)
        dataInventoryLocations.append( dataInventoryLocation )

    return DataInventoryConfiguration(masterFile, tmpFile, dataInventoryLocations)


class DataInventoryConfiguration(Configuration):
    """
    Encapsulates the configuration information related to the locations
    of the copies of the data inventory.
    """
    def __init__(self, masterFile, tmpFile, dataInventoryLocations):
        """
        Constructor.

        dataInventoryLocations: array of DataInventoryLocation
        """
        super().__init__(masterFile, tmpFile)
        self.dataInventoryLocations = dataInventoryLocations


    def getDataInventoryLocations(self):
        """
        Obtain the data inventory locations of this paradux installation

        return: array of DataInventoryLocation
        """
        return self.dataInventoryLocations


    def createReport(self,fileName):
        """
        Implementation for this subclass.
        """
        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            for locationJ in j['locations']:
                paradux.data.datalocation.parseDataInventoryLocationJson(locationJ)

        except Exception as e:
            reportItems.append(ReportItem(Level.ERROR, str(type(e)) + ': ' + str(e)))

        return Report(reportItems)


    def asText(self):
        """
        Show this DataInventoryConfiguration to the user in plain text.

        return: plain text
        """
        if self.dataInventoryLocations is not None and len(self.dataInventoryLocations) > 0:
            for dataInventoryLocation in self.dataInventoryLocations:
                if dataInventoryLocation.name is not None:
                    t  = "* Name:        {0:s}\n".format( dataInventoryLocation.name )
                    t += "  URL:         {0:s}\n".format( dataInventoryLocation.url )
                    t += "  Description: {0:s}\n".format( "<not set>" if dataInventoryLocation.description is None else dataInventoryLocation.description )
                else:
                    t  = "* URL:         {0:s}\n".format( dataInventoryLocation.url )
                    t += "  Description: {0:s}\n".format( "<not set>" if dataInventoryLocation.description is None else dataInventoryLocation.description )

        else:
            t = """You currently don't have a data inventory locations configured. To configure, run 'paradux edit-data-inventory-locations'\n"""

        return t
