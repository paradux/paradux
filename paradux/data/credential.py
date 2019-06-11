#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux.logging


def parseCredentialsJson(j):
    """
    Helper function to parse a JSON credentials definition into an instance
    of the right subclass of Credentials.

    j: JSON fragment
    return: instance of a subclass of Credentials
    """
    paradux.logging.trace('parseCredentialsJson')

    if 'ssh-user' in j and 'ssh-private-key' in j:
        return SshCredentials( j['ssh-user'], j['ssh-private-key'] )
    elif 'aws-access-key' in j and 'aws-secret-key' in j:
        return AwsApiCredentials( j['aws-access-key'], j['aws-secret-key'] )
    else:
        raise ValueError( 'Unknown credential type' )


class Credentials:
    """
    Abstract superclass for all types of username/password and the like
    """
    pass


class PasswordCredentials(Credentials):
    """
    A username/password combination
    """
    def __init__(self, username, usersecret):
        """
        Constructor.

        username: user name
        usersecret: password that goes with the user name
        """
        self.username   = username
        self.usersecret = usersecret


class SshCredentials(Credentials):
    """
    A username/private key pair combination
    """
    def __init__(self, username, private_key):
        """
        Constructor.

        username: user name
        private_key: private SSH key that goes with the user name
        """
        self.username    = username
        self.private_key = private_key


class AwsApiCredentials(Credentials):
    """
    A pair of API key and secret access key to access Amazon Web Services via
    its API.
    """
    def __init__(self, awsAccessKey, awsSecretKey):
        """
        Constructor.

        awsAccessKey: the AWS access key
        awsSecretKey: the AWS secret key
        """
        self.awsAccessKey = awsAccessKey
        self.awsSecretKey = awsSecretKey

