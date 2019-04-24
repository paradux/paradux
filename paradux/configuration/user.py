#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.configuration import Configuration
from paradux.configuration.report import Level, Report, ReportItem
import paradux.data.person
import paradux.utils


def saveInitial(fileName):
    """
    Save the initial JSON content of a UserConfiguration to this file.

    return: void
    """
    content = """{
    "name" : "Unnamed Paradux User"
}"""
    paradux.utils.saveFile(fileName, content, 0o600)


def createFromFile(masterFile, tmpFile):
    """
    Create a UserConfiguration that reads from and uses the specified files.

    masterFile: name of a JSON file containing the current master
    tmpFile: potential name of a JSON file containing the current in-progress edits to the master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    user = paradux.data.person.parsePersonJson(j)

    return UserConfiguration(masterFile, tmpFile, user)


class UserConfiguration(Configuration):
    """
    Encapsulates the configuration information related to the paradux user.
    """
    def __init__(self, masterFile, tmpFile, user):
        """
        Constructor.

        user: the paradux user
        """
        super().__init__(masterFile, tmpFile)
        self.user = user


    def getUser(self):
        """
        Obtain the user of this paradux installation

        return: the User
        """
        return self.user


    def createReport(self,fileName):
        """
        Overrides
        """

        reportItems = []
        try :
            j = paradux.utils.readJsonFromFile(fileName)
            paradux.data.person.parsePersonJson(j)

        except Exception as e:
            reportItems.append(ReportItem(Level.ERROR, str(type(e)) + ': ' + str(e)))

        return Report(reportItems)


    def asText(self):
        """
        Show this UserConfiguration to the user in plain text.

        return: plain text
        """
        if self.user is None:
            t = """You currently don't have a user configured. To configure, run 'paradux edit-user'\n"""

        else:
            t  = "Name:           {0:s}\n".format( self.user.name )
            t += "Address:        {0:s}\n".format( "<not set>" if self.user.address      is None else self.user.address )
            t += "Contact e-mail: {0:s}\n".format( "<not set>" if self.user.contactEmail is None else self.user.contactEmail )
            t += "Contact phone:  {0:s}\n".format( "<not set>" if self.user.contactPhone is None else self.user.contactPhone )

        return t
        
