#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from paradux.data.person import Person
import paradux.logging
import paradux.utils


def parseStewardJson(j):
    """
    Help function to parse a JSON fragment into an instance of Steward

    j: JSON fragment
    return: Steward
    """
    paradux.logging.trace('parseStewardJson')

    name         = j['name']          # required
    address      = j['address']       if 'address'       in j else None
    contactEmail = j['contact-email'] if 'contact-email' in j else None
    contactPhone = j['contact-phone'] if 'contact-phone' in j else None
    acceptedOn   = j['accepted-on']   # required

    acceptedTs = paradux.utils.string2time(acceptedOn)

    return Steward(name, address, contactEmail, contactPhone, acceptedTs)


class Steward(Person):
    """
    All information we have about and related to a Steward.
    """
    def __init__(self, name, address, contactEmail, contactPhone, acceptedTs):
        super().__init__(name, address, contactEmail, contactPhone)
        self.acceptedTs   = acceptedTs
