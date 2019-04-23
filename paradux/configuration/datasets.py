#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.configuration import Configuration
from paradux.configuration.report import Level, Report, ReportItem
import paradux.data.dataset
import paradux.utils


def saveInitial(fileName):
    """
    Save the initial JSON content of a DatasetsConfiguration to this file.

    return: void
    """
    content = """{
    "datasets" : [
    ]
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a DatasetsConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    datasets = []

    for datasetJ in j['datasets']:
        dataset = paradux.data.dataset.parseDatasetJson(datasetJ)
        datasets.append(dataset)

    return DatasetsConfiguration(masterFile, tmpFile, datasets)
    

class DatasetsConfiguration(Configuration):
    """
    Encapsulates the configuration information related to datasets.
    """
    def __init__(self, masterFile, tmpFile, datasets):
        """
        Constructor.

        datasets: list of Dataset
        """
        super().__init__(masterFile, tmpFile)
        self.datasets = datasets


    def createReport(self,fileName):
        """
        Overrides
        """

        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            for datasetJ in j['datasets']:
                paradux.data.dataset.parseDatasetJson(datasetJ)

        except Exception as e:
            reportItems.append(ReportItem(Level.ERROR, str(type(e)) + ': ' + str(e)))

        return Report(reportItems)


    def asText(self):
        """
        Show this DatasetsConfiguration to the user in plain text.

        return: plain text
        """
        if len(self.datasets) == 0:
            t = """You currently have 0 datasets configured. To configure some, run 'paradux edit-datasets'\n"""

        else:
            t = "You currently have {0:d} dataset(s) configured. They are:\n".format(len(self.datasets))
            for dataset in self.datasets:
                t += "* name:         {0:s}\n".format(dataset.name)
                if dataset.description != None:
                    t += "  description:  {0:s}\n".format(dataset.description)
                if dataset.source is not None:
                    t += "  source:       {0:s}\n".format(dataset.source.url)
                for destination in dataset.destinations:
                    t += "  destination:  {0:s}\n".format(destination.url)

        return t
        
