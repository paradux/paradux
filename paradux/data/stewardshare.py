#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging
from paradux.shamir import Share
import paradux.utils


def parseStewardShareJson(j):
    """
    Help function to parse a JSON fragment into an instance of StewardShare

    j: JSON fragment
    return: StewardShare
    """
    paradux.logging.trace('parseStewardShareJson')

    shamirShare =_parseShamirSecretShare(j['shamir-share']) # required
    issuedOn    = j['issued-on']                            # required

    issuedTs = paradux.utils.string2time(issuedOn)

    return StewardShare(shamirShare, issuedTs)


def _parseShamirSecretShare(j):
    """
    Helper function to parse a JSON fragment into a Shamir Share

    j: JSON fragment
    return: Shamir share
    """
    x     = j['x']     # required
    value = j['y'] # required

    return Share(x, value)


class StewardShare:
    """
    All information issued to a Steward that is specific to that Steward.
    """
    def __init__(self, shamirShare, issuedTs):
        self.shamirShare = shamirShare
        self.issuedTs    = issuedTs


    def getShamirShare(self):
        """
        Obtain the Shamir share for this Steward

        return: the Shamir share
        """
        return self.shamirShare


    def asJson(self):
        """
        Convert this to JSON.

        return: JSON
        """
        j = {
            'shamir-share' : {
                'x' : self.shamirShare.getX(),
                'y' : self.shamirShare.getY()
            },
            'issued-on' : paradux.utils.time2string(self.issuedTs)
        }
        return j
