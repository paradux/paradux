#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.data.stewardshare import StewardShare
from paradux.shamir import ShamirSecretSharing
import paradux.configuration
import time


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
    j['watermark-x']     = 1 # the next x value to be issued
    j['recovery-secret'] = recoverySecret
    j['issued-shares']   = {}

    paradux.utils.writeJsonToFile(fileName, j, 0o600)


def createFromFile(masterFile):
    """
    Create a SecretsConfiguration that uses the specified file.

    masterFile: name of a JSON file containing the current master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    mersenne       = j['mersenne']                         # required
    polyK1         = _parseIntegerArray(j['polynomial'])   # required
    watermarkX     = j['watermark-x']                      # required
    recoverySecret = j['recovery-secret']                  # required
    
    issuedStewardShares = {}
    for stewardId, stewardShareJ in j['issued-shares'].items():
        stewardShare = paradux.data.stewardshare.parseStewardShareJson(stewardShareJ)
        issuedStewardShares[stewardId] = stewardShare
    
    return SecretsConfiguration(masterFile, mersenne, polyK1, watermarkX, recoverySecret, issuedStewardShares)


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
    def __init__(self, masterFile, mersenne, polyK1, watermarkX, recoverySecret, issuedStewardShares):
        """
        Constructor.

        masterFile: stores the secrets
        mersenne: an integer indicating the nth Mersenne Prime
        polyK1: the coefficients of the Shamir polynomial, from a[k] to a[1]
        watermarkX: the next x to issue
        recoverySecret: the recovery secret
        issuedStewardShares: dict of issued shares, keyed by steward id
        """
        self.masterFile          = masterFile
        self.mersenne            = mersenne
        self.polyK1              = polyK1
        self.watermarkX          = watermarkX
        self.recoverySecret      = recoverySecret
        self.issuedStewardShares = issuedStewardShares
        

    def getIssuedStewardShare(self, stewardId):
        """
        Obtain a previously-issued StewardShare.

        stewardId: identifier of the Steward to whom the StewardShare was issued
        return: StewardShare, or None if none
        """
        if stewardId in self.issuedStewardShares:
            return self.issuedStewardShares[stewardId]

        return None


    def getMersenne(self):
        """
        Obtain which Mersenne prime is to be used

        return: n if the nth Mersenne prime was used
        """
        return self.mersenne


    def getMinStewards(self):
        """
        Obtain how many shares are required to reconstitute the secret.

        return: k
        """
        return len(self.polyK1)+1


    def issueStewardShare(self, stewardId):
        """
        Issue a new share. Note that after this has been invoked,
        save() must be invoked otherwise the new share will not be
        recorded.

        stewardId: identifier of the Steward to whom the StewardShare shall be issued
        return: the new StewardShare, or None if issued already
        """
        if stewardId in self.issuedStewardShares:
            return None

        shamir    = ShamirSecretSharing(self.mersenne)
        generator = shamir.split(self.recoverySecret, len(self.polyK1))

        shamirShare = generator.obtainShare(self.watermarkX)
        self.watermarkX += 1

        ret = StewardShare(shamirShare, time.time())
        self.issuedStewardShares[stewardId] = ret
        return ret


    def save(self):
        """
        Save this SecretsConfiguration to disk. Needs to be invoked after issuing
        new StewardShare(s).

        return: void
        """
        j = {
            'mersenne'        : self.mersenne,
            'polynomial'      : self.polyK1,
            'watermark-x'     : self.watermarkX,
            'recovery-secret' : self.recoverySecret,
            'issued-shares'   : {}
        }
        for stewardId, issuedStewardShare in self.issuedStewardShares.items():
            j['issued-shares'][stewardId] = issuedStewardShare.asJson()

        paradux.utils.writeJsonToFile(self.masterFile, j, 0o600)
