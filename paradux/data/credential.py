#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import abc
import paradux.logging


def parseCredentialsJson(j, url=None):
    """
    Helper function to parse a JSON credentials definition into an instance
    of the right subclass of Credentials. If u is given, also check that
    these Credentials work with the URL with this protocol.

    j: JSON fragment
    url: parsed URL
    return: instance of a subclass of Credentials
    """
    paradux.logging.trace('parseCredentialsJson')

    ret = None
    if 'user' in j and 'password' in j:
        ret = PasswordCredentials( j['user'], j['password'] )

    elif 'ssh-user' in j and 'ssh-private-key' in j:
        ret = SshCredentials( j['ssh-user'], j['ssh-private-key'] )

    elif 'aws-access-key' in j and 'aws-secret-key' in j:
        ret = AwsApiCredentials( j['aws-access-key'], j['aws-secret-key'] )

    if ret is None:
        raise ValueError( 'Unknown credential type' )

    if url is not None:
        if ret is not None and not ret.isSuitableForProtocol(url.scheme):
            raise ValueError('Credential type not suitable for protocol ' + url.scheme + ': ' + str(type(ret)))

    return ret


class Credentials:
    """
    Abstract superclass for all types of username/password and the like
    """

    @abc.abstractmethod
    def isSuitableForProtocol(self, proto):
        """
        Returns True if this CredentialType is suitable for the provided
        data transfer protocol, e.g. 'scp'.
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


    def isSuitableForProtocol(self, proto):
        # FIXME
        return False


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


    def isSuitableForProtocol(self, proto):
        return 'scp' == proto


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


    def isSuitableForProtocol(self, proto):
        return 's3' == proto

