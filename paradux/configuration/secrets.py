#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.shamir import ShamirSecretSharing
import paradux.configuration


def createAndSaveInitial(nbits, secret, requiredShares, fileName):
    """
    Create the initial secrets, and save the initial JSON content of a
    SecretsConfiguration to this file.

    return: void
    """

    mersenne = paradux.shamir.mersenneForBits(nbits)

    shamir    = ShamirSecretSharing(mersenne)
    generator = shamir.split(secret,requiredShares)

    j = {}
    j['mersenne']   = mersenne
    j['polynomial'] = generator.getPolyK1()
    j['secret']     = generator.getSecret()

    paradux.utils.writeJsonToFile(fileName, j, 0o600)


def createFromFile(masterFile):
    """
    Create a SecretsConfiguration that uses the specified file.

    masterFile: name of a JSON file containing the current master
    """
    j = paradux.utils.readJsonFromFile(masterFile)

    mersenne       = j['mersenne']       # required
    polyK1         = _parseIntegerArray(j['polynomial'])
    
    stewardShares = {}
    for stewardId, stewardShareJ in j['stewardshares']:
        stewardShare = _parseShareJson(j)
        stewardsShares[stewardId] = stewardShare
    
    return SecretsConfiguration(masterFile, mersenne, polyK1, stewardShares)


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


def secretToPassphrase(secret):
    """
    Convert an integer (used as secret for Shamir) to a passphrase for
    cryptsetup. Use only 7bit ASCII. Cryptsetup supports up to 512 chars.
    Just to be extra safe, we use the range from 32 (space, inclusive)
    through 127 (DEL, exclusive).

    Note: if you change this algorith, you will break everybody's
    recovery!

    secret: the integer secret
    return: passphrase
    """
    minC =  32
    maxC = 127
    dC   = minC - maxC

    ret = ''
    for i in range(512):
        if secret == 0:
            break
        c = ( secret % dC ) + minC
        ret += chr(c)
        secret = secret // dC
    return ret

    
class StewardSecret:
    """
    Encapsulates the stewawrd-specific secret information
    """
    def __init__(self, id, share):
        """
        Constructor.

        id: the id of the Steward as defined in the Stewards JSON file
        share: the Shamir share for this Steward
        """
        self.id    = id
        self.share = share



class SecretsConfiguration:
    """
    Encapsulates the configuration information related to secrets.
    """
    def __init__(self, masterFile, mersenne, polyK1, stewardShares):
        """
        Constructor.

        mersenne: an integer indicating the nth Mersenne Prime
        polyK1: the coefficients of the Shamir polynomial, from a[k] to a[1]
        stewardShares: dict of created shares, keyed by steward id
        """
        self.mersenne      = mersenne
        self.polyK1        = polyK1
        self.stewardShares = stewardShares
        
