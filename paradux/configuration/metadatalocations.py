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
    Save the initial JSON content of Metadata to this file.

    return: void
    """
    content = """{
    "locations" : []
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a MetadataLocationsConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    metadataLocations = []

    for locationJ in j['locations']:
        metadataLocation = paradux.data.datalocation.parseMetadataLocationJson(locationJ)
        metadataLocations.append( metadataLocation )

    return MetadataLocationsConfiguration(masterFile, tmpFile, metadataLocations)


class MetadataLocationsConfiguration(Configuration):
    """
    Encapsulates the configuration information related to the locations
    of the copies of the paradux metadata
    """
    def __init__(self, masterFile, tmpFile, metadataLocations):
        """
        Constructor.

        metadataLocations: array of MetadataLocation
        """
        super().__init__(masterFile, tmpFile)
        self.metadataLocations = metadataLocations


    def getMetadataLocations(self):
        """
        Obtain the metadata locations of this paradux installation

        return: array of MetadataLocation
        """
        return self.metadataLocations


    def createReport(self,fileName):
        """
        Implementation for this subclass.
        """
        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            for locationJ in j['locations']:
                paradux.data.datalocation.parseMetadataLocationJson(locationJ)

        except Exception as e:
            reportItems.append(ReportItem(Level.ERROR, str(type(e)) + ': ' + str(e)))

        return Report(reportItems)


    def asText(self):
        """
        Show this MetadataLocationsConfiguration to the user in plain text.

        return: plain text
        """
        if self.metadataLocations is not None and len(self.metadataLocations) > 0:
            for metadataLocation in self.metadataLocations:
                if metadataLocation.name is not None:
                    t  = "* Name:        {0:s}\n".format(metadataLocation.name)
                    t += "  URL:         {0:s}\n".format(str(metadataLocation))
                    t += "  Description: {0:s}\n".format("<not set>" if metadataLocation.description is None else metadataLocation.description)
                else:
                    t  = "* URL:         {0:s}\n".format(str(metadataLocation))
                    t += "  Description: {0:s}\n".format("<not set>" if metadataLocation.description is None else metadataLocation.description)

        else:
            t = """You currently have 0 metadata locations configured. To configure, run 'paradux edit-metadata-locations'\n"""

        return t
