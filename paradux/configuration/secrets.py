#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.shamir import ShamirSecretSharing
import paradux.configuration


def createAndSaveInitial(nbits, recoverySecret, requiredShares, fileName):
    """
    Create the initial secrets, and save the initial JSON content of a
    SecretsConfiguration to this file.

    return: void
    """

    mersenne = paradux.shamir.mersenneForBits(nbits)

    shamir    = ShamirSecretSharing(mersenne)
    generator = shamir.split(recoverySecret,requiredShares)

    j = {}
    j['mersenne']        = mersenne
    j['polynomial']      = generator.getPolyK1()
    j['recovery-secret'] = recoverySecret

    paradux.utils.writeJsonToFile(fileName, j, 0o600)


def createFromFile(masterFile):
    """
    Create a SecretsConfiguration that uses the specified file.

    masterFile: name of a JSON file containing the current master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    mersenne       = j['mersenne']                       # required
    recoverySecret = j['recovery-secret']                # required
    polyK1         = _parseIntegerArray(j['polynomial']) # required
    
    stewardShares = {}
    for stewardId, stewardShareJ in j['stewardshares']:
        stewardShare = _parseShareJson(j)
        stewardsShares[stewardId] = stewardShare
    
    return SecretsConfiguration(masterFile, mersenne, recoverySecret, polyK1, stewardShares)


def _parseShareJson(j):
    """
    Helper function to parse a JSON fragment into a Shamir Share

    j: JSON fragment
    return: Shamir share
    """
    x     = j['x']     # required
    value = j['value'] # required

    return ShamirSecretSharing.Share(x, value)


def _parseIntegerArray(j):
    """
    Helper function to parse a JSON fragment into an array of integer

    j: JSON fragment
    return: array of integer
    """
    ret = []
    for jj in j:
        ret.append(int(jj))
    return ret


class SecretsConfiguration:
    """
    Encapsulates the configuration information related to secrets.
    """
    def __init__(self, masterFile, mersenne, polyK1, stewardShares):
        """
        Constructor.

        mersenne: an integer indicating the nth Mersenne Prime
        recoverySecret: the recovery secret
        polyK1: the coefficients of the Shamir polynomial, from a[k] to a[1]
        stewardShares: dict of created shares, keyed by steward id
        """
        self.mersenne       = mersenne
        self.recoverySecret = recoverySecret
        self.polyK1         = polyK1
        self.stewardShares  = stewardShares
        
