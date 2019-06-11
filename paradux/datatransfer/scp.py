#!/usr/bin/python
#
# Functionality to copy files via scp
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import inspect
import os
from paradux.data.credential import SshCredentials
import paradux.utils
from tempfile import NamedTemporaryFile

def supportsProtocol(proto):
    """
    Determine whether this data transfer protocol support URL protocol
    proto.

    proto: the URL protocol, such as "scp"
    return: True or False
    """
    return 'scp' == proto


def upload(localFile, destination):
    """
    Upload the local file to the specified DataLocation.

    localFile: name of the local file
    destination: DataLocation for upload
    return: True if successful
    """

    ret = True
    try:
        cred = destination.credentials

        cmd = "scp"

        privKeyFile = None
        if cred:
            if isinstance(cred, SshCredentials):
                privKeyFile = NamedTemporaryFile(delete=False)
                privKeyFile.write(cred.private_key.encode())
                privKeyFile.close()

            else:
                paradux.logging.fatal('Should not happen:', cred)

        if privKeyFile is not None:
            cmd += " -i '" + privKeyFile.name + "'"

        host = destination.url.hostname
        path = destination.url.path

        if len(path) > 0:
            path = path[1:0] # remove leading /

        cmd += " '" + localFile + "'"

        if privKeyFile is not None:
            cmd += " '" + cred.username + "@" + host + ":" + path + "'"
        else:
            cmd += " '" + host + ":" + path + "'"

        exitCode = paradux.utils.myexec(cmd)
        if exitCode != 0:
            ret = 1

    finally:
        if privKeyFile is not None:
            os.unlink(privKeyFile.name)

    return ret
