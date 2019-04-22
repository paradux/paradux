#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.configuration import Configuration
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

    datasets = _parseDatasetsJson(j)

    return DatasetsConfiguration(masterFile, tmpFile, datasets)


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
    

def _parseDatasetsJson(j):
    """
    Helper function to parse a JSON fragment into an array of Dataset

    j: JSON fragment
    return: array of Dataset
    """
    datasets = []

    for datasetJ in j['datasets']:
        dataset = _parseDatasetJson(datasetJ)
        datasets.append(dataset)

    return datasets


def _parseDatasetJson(j):
    """
    Helper function to parse a JSON dataset definition into an instance of Dataset

    j: JSON fragment
    return: instance of Dataset
    """
    name        = j['name']        # required
    description = j['description'] if 'description' in datasetJ else None
    sourceJ     = j['source']      # required

    source       = _parseSourceDataLocationJson(sourceJ)
    destinations = []

    if 'destinations' in j:
        for destinationJ in j['destinations']:
            destination = _parseDestinationDataLocationJson(destinationJ)
            destinations.append(destination)

    return Dataset(name,description,source,destinations)


def _parseSourceDataLocationJson(j):
    """
    Helper function to parse a JSON source data location definition into an instance
    of SourceDataLocation

    j: JSON fragment
    return: instance of SourceDataLocation
    """
    name        = j['name']        # required
    description = j['description'] if 'description' in j else None
    url         = j['url']         # required
    credentials = _parseCredentialsJson(j['credentials']) if 'credentials' in j else None

    return SourceDataLocation(name, description, url, credentials)


def _parseDestinationDataLocationJson(j):
    """
    Helper function to parse a JSON destination data location definition into an
    instance of DestinationDataLocation

    j: JSON fragment
    return: instance of DestinationDataLocation
    """
    name        = j['name']        # required
    description = j['description'] if 'description' in j else None
    url         = j['url']         # required
    credentials = _parseCredentialsJson(j['credentials']) if 'credentials' in j else None
    frequency   = _parseFrequencyJson(  j['frequency']  ) if 'frequency'   in j else None
    encryption  = _parseEncryptionJson( j['encryption'] ) if 'encryption'  in j else None

    return DestinationDataLocation(name, description, url, credentials, frequency, encryption)


def _parseCredentialsJson(j):
    """
    Helper function to parse a JSON credentials definition into an instance
    of the right subclass of Credentials.

    j: JSON fragment
    return: instance of a subclass of Credentials
    """
    # FIXME
    return None

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



class Dataset:
    """
    Encapsulates everything there's to be said about a Dataset.
    """
    def __init__(self, name, description, source, destinations):
        """
        Constructor.

        name: the name of this Dataset
        description: any description for this Dataset
        source: the sourceDataLocation for this Dataset
        destinations: the array of DestinationDataLocation for this Dataset
        """
        self.name         = name
        self.description  = description
        self.source       = source
        self.destinations = destinations
        

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


    def createReport(fileName):
        """
        Overrides
        """

        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            datasets = _parseDatasetsJson(j)
        except Exception as e:
            reportItems.append( ReportItem( Level.ERROR, e ))
            
        return Report(exportItems)


    def asText(self):
        """
        Show this DatasetsConfiguration to the user in plain text.

        return: plain text
        """
        if len(self.datasets) == 0:
            t = """You currently have 0 datasets configured. To configure some, run 'paradux edit-datasets'\n"""

        else:
            t = """You currently have {0,d} dataset(s) configured. They are:""".format(len(self.datasets))
            for dataset in self.datasets:
                t.append( "* name:        %s\n").format( dataset.name )
                if dataset.description != None:
                    t.append( " description:  %s\n").format( dataset.description )
                if dataset.source != None:
                    t.append( " source:       %s\n").format( dataset.source.url )
                for destination in dataset.destinations:
                    t.append( " destination:  %s\n").format( destination.url )

        return t
        
