#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

class StewardPackage:
    """
    Encapsulates all information conveyed to a Steward.
    """
    def __init__(self, paraduxUserName, paraduxUserContact, stewardName, secretShare, configurationLocations, paraduxVersion=paradux.__version__):
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
