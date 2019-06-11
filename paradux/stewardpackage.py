#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#


class StewardPackage:
    """
    Encapsulates all information conveyed to a Steward.

    user: the user whose paradux instance this is
    steward: the steward to whom the StewardPackage is conveyed
    stewardShare: the share-related information conveyed to the steward
    mersenne: the mersenn-th Mersenne prime number was used
    minStewards: the minimum number of stewards required to restore
    metadataLocationsConf: the configuration of the metadata locations
    paraduxVersion: the version of paradux that was used
    """
    def __init__(self, user, steward, stewardShare, mersenne, minStewards, metadataLocationsConf, paraduxVersion):
        self.user                  = user
        self.steward               = steward
        self.stewardShare          = stewardShare
        self.mersenne              = mersenne
        self.minStewards           = minStewards
        self.metadataLocationsConf = metadataLocationsConf
        self.paraduxVersion        = paraduxVersion


    def asText(self):
        """
        Obtain the content of this StewardPackage as text that can be
        shown/printed for a steward.

        return: plain text
        """

        shamirShare       = self.stewardShare.getShamirShare()
        metadataLocations = self.metadataLocationsConf.getMetadataLocations()

        ret = """Dear {steward.name:s},

you have graciously agreed to help
    {user.name:s}
recover from personal data disasters that might befall them or their family.
This sheet contains all information you need to have to assist when needed.
Please keep it in a place where it safe from disasters (like fires) and
unauthorized access (like burglars).

Should you note unauthorized access, loss of this sheet, or if you do not
want to assist {user.name:s} any more, please notify them immediately""".format(user = self.user, steward = self.steward)

        if self.user.contactEmail is not None and self.user.contactPhone is not None:
            ret += """ at:
"""
            if self.user.contactEmail is not None:
                ret += """    e-mail: {user.contactEmail:s}
""".format(user = self.user)

            if self.user.contactPhone is not None:
                ret += """    phone: {user.contactPhone:s}
""".format(user = self.user)

        else:
            ret += """.
"""

        if self.paraduxVersion is not None:
            ret += """
Paradux version:
    {version:s}
""".format(version = self.paraduxVersion)

        ret += """
Your recovery fragment:
    x = {shamir.x:d}
    y = {shamir.y:d}
    m = {mersenne:d}
    k = {minStewards:d}
""".format(     shamir      = shamirShare,
                mersenne    = self.mersenne,
                minStewards = self.minStewards)

        ret += """
Locations of the paradux metadata:
"""
        if metadataLocations is not None and len(metadataLocations) > 0:
            for metadataLocation in metadataLocations:
                ret += """    {url:s}
""".format(url = str(metadataLocation))

        else:
            ret += """    <currently none known>
"""

        return ret


    def asJson(self):
        """
        Obtain the content of this StewardPackage as JSON fragment.

        return JSON fragment
        """
        ret = {
            'user'         : self.user.asJson(),
            'steward'      : self.steward.asJson(),
            'stewardshare' : self.stewardShare.asJson(),
            'mersenne'     : self.mersenne,
            'min-stewards' : self.minStewards
        }

        return ret
