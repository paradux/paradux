#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#


class Person:
    """
    Represents a Person.
    """
    def __init__(self, name, address, contactEmail, contactPhone):
        self.name         = name
        self.address      = address
        self.contactEmail = contactEmail
        self.contactPhone = contactPhone


def parsePersonJson(j):
    """
    Help function to parse a JSON fragment into an instance of Person

    j: JSON fragment
    return: Person
    """
    name         = j['name']          # required
    address      = j['address']       if 'address'       in j else None
    contactEmail = j['contact-email'] if 'contact-email' in j else None
    contactPhone = j['contact-phone'] if 'contact-phone' in j else None

    return Person(name, address, contactEmail, contactPhone)

