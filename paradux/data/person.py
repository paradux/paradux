#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging


def parsePersonJson(j):
    """
    Help function to parse a JSON fragment into an instance of Person

    j: JSON fragment
    return: Person
    """
    paradux.logging.trace('parsePersonJson')

    name         = j['name']          # required
    address      = j['address']       if 'address'       in j else None
    contactEmail = j['contact-email'] if 'contact-email' in j else None
    contactPhone = j['contact-phone'] if 'contact-phone' in j else None

    return Person(name, address, contactEmail, contactPhone)


class Person:
    """
    Represents a Person. This is used for the User and for Stewards.
    """
    def __init__(self, name, address, contactEmail, contactPhone):
        """
        Constructor.

        name: the name of the Person, such as John P Steward
        address: the physical address of the Person, sufficient to locate them
        contactEmail: an e-mail address they have provided as a way to contact them about
             matters related to this paradux configuration
        contactPhone: a phone number they have provided as a way to contact them about
             matters related to this paradux configuration
        """
        self.name         = name
        self.address      = address
        self.contactEmail = contactEmail
        self.contactPhone = contactPhone


    def asJson(self):
        """
        Obtain in JSON format.

        return: json
        """
        ret = {
            'name' : self.name
        }
        if self.address is not None:
            ret['address'] = self.address
        if self.contactEmail is not None:
            ret['contact-email'] = self.contactEmail
        if self.contactPhone is not None:
            ret['contact-phone'] = self.contactPhone

        return ret
