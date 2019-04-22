#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux
from paradux.configuration import Configuration
import paradux.utils


def saveInitial(fileName):
    """
    Save the initial JSON content of a StewardsConfiguration to this file.

    return: void
    """
    content = """{
    "stewards" : [
    ]
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a StewardsConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    stewardInfos = _parseStewardsJson(j)

    return StewardsConfiguration(masterFile, tmpFile, stewardInfos)


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

    # FIXME: check for non-overlapping ids for the Stewards

    items.append( ConfigurationReportItem( Level.NOTICE, "Hi mom" ))

    return ConfigurationReport(items)


def _parseStewardsJson(j):
    """
    Help function to parse a JSON fragment into an array of StewardInfo

    j: JSON fragment
    return: array of StewardInfo
    """
    stewardInfos = []

    for stewardJ in j['stewards']:
        stewardInfo = _parseStewardJson(stewardJ)
        stewardInfos.append(stewardInfo)

    return stewardInfos


def _parseStewardJson(j):
    """
    Help function to parse a JSON fragment into  StewardInfo

    j: JSON fragment
    return: StewardInfo
    """
    id           = j['id']            # required
    name         = j['name']          # required
    address      = j['address']       if 'address'       in j else None
    contactEmail = j['contact-email'] if 'contact-email' in j else None
    contactPhone = j['contact-phone'] if 'contact-phone' in j else None
    acceptedOn   = j['accepted-on']   # required

    acceptedTs = paradux.utils.string2time(acceptedOn)

    return StewardInfo(id, name, address, contactEmail, contactPhone, acceptedTs)


class StewardsConfiguration(Configuration):
    """
    Encapsulates the configuration information related to stewards.
    """
    def __init__(self, masterFile, tmpFile, stewardInfos):
        """
        Constructor.

        stewardInfos: list of StewardInfo
        """
        super().__init__(masterFile, tmpFile)
        self.stewardInfos = stewardInfos


    def createReport(fileName):
        """
        Overrides
        """

        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            datasets = _parseStewardsJson(j)
        except Exception as e:
            reportItems.append( ReportItem( Level.ERROR, e ))
            
        return Report(exportItems)


    def asText(self):
        """
        Show this StewardsConfiguration to the user in plain text.

        return: plain text
        """
        if len(self.stewardInfos) == 0:
            t = """You currently have 0 stewards configured. To configure some, run 'paradux edit-stewards'\n"""

        else:
            t = """You currently have {0,d} steward(s) configured. They are:""".format(len(self.stewardInfos))
            for stewardInfo in self.stewardInfos:
                t.append( "* name:        %s\n").format( stewardInfo.name )
                if stewardInfo.address != None:
                    t.append( " address:      %s\n").format( stewardInfo.address )
                if stewardInfo.contactEmail != None:
                    t.append( " contactEmail: %s\n").format( stewardInfo.contactEmail )
                if stewardInfo.contactPhone != None:
                    t.append( " contactPhone: %s\n").format( stewardInfo.contactPhone )
                if stewardInfo.acceptedTs != None:
                    t.append( " acceptedTs:   %s\n").format( stewardInfo.acceptedTs )

        return t


class StewardInfo:
    """
    All information we have about and related to a Steward.
    """
    def __init__(self, id, name, address, contactEmail, contactPhone, acceptedTs):
        self.id           = id
        self.name         = name
        self.address      = address
        self.contactEmail = contactEmail
        self.contactPhone = contactPhone
        self.acceptedTs   = acceptedTs


    
class StewardPackage:
    """
    Encapsulates all information conveyed to a Steward.
    """
    def __init__(self, paraduxUserName, paraduxUserContact, stewardName, secretShare, configurationLocations, paraduxVersion ):
        self.paraduxUserName        = paraduxUserName
        self.paraduxUserContact     = paraduxUserContact
        self.stewardName            = stewardName
        self.secretShare            = secretShare
        self.configurationLocations = configurationLocations
        self.paraduxVersion         = paraduxVersion


    def asText(self):
        """
        Obtain the content of this StewardPackage as text that can be
        shown/printed for a steward.

        return: plain text
        """

        formattedSecretShare            = self.secretShare # FIXME
        formattedConfigurationLocations = "\n".join(self.configurationLocations)

        return """Dear {2:s},

you have graciously agreed to help
    {0:s}
recover from personal data disasters that might befall them or their family.
This sheet contains all information you need to have to assist when needed.
Please keep it in a place where it safe from disasters (like fires) and
unauthorized access (like burglars).

Should you note unauthorized access, loss of this sheet, or if you do not
want to assist {0:s} any more, please notify {0:s)
immediately at:
    {1:s}

Name of the scheme:
    {5:s}|

Your recovery fragment:
    {3:s}

Locations for recovery data:
{4:s}""".format(
                self.paraduxUserName,
                self.paraduxUserContact,
                self.stewardName,
                formattedSecretShare,
                formattedConfigurationLocations )

