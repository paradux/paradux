#!/usr/bin/python
#
# Collection of utility functions.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import calendar
import json
import os
import pkgutil
import paradux.logging
import re
import subprocess
import time


def findSubmodules(package) :
    """
    Find all submodules in the named package

    package: the package
    return: array of module names
    """
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        ret.append(modname)
    return ret


def myexec(cmd,stdin=None, captureStdout=False, captureStderr=False):
    """
    Wrapper around executing sub-commands, so we can log what is happening.

    cmd: the command to be executed by the shell
    stdin: content to be piped into the command, if any
    captureStdout: if true, capture the commands stdout and return 
    captureStderr: if true, capture the commands stderr and return 
    return: if no capture: return code; otherwise tuple
    """
    if stdin == None:
        paradux.logging.debugAndSuspend('myexec:', cmd)
    else:
        paradux.logging.debugAndSuspend('myexec:', cmd, 'with stdin:', stdin)
    paradux.logging.trace(cmd, 'None' if stdin==None else len(stdin))

    ret = subprocess.run(
            cmd,
            shell=True,
            input=stdin,
            stdout=subprocess.PIPE if captureStdout else None,
            stderr=subprocess.PIPE if captureStderr else None)

    if captureStdout or captureStderr:
        return (ret.returncode,
                ret.stdout if hasattr(ret, 'stdout') else None,
                ret.stderr if hasattr(ret, 'stderr') else None )
    else:
        return ret.returncode


def readJsonFromFile( fileName ):
    """
    Read and parse JSON from a file. In addition, accept # for comments.

    fileName: the JSON file to read
    return: the parsed JSON
    """
    paradux.logging.trace( fileName )

    with open(fileName, 'r') as fd:
        jsonContent = fd.read()

    jsonContent = re.sub(r'(?<!\\)#.*', '', jsonContent)
    ret         = json.loads(jsonContent)
    return ret


def writeJsonToFile(fileName, j, mode=None ) :
    """
    Write JSON to a file.

    fileName: name of the file to write
    j: the JSON object to write
    mode: the file permissions to set; default is: umask
    """
    with open(fileName, 'w') as fd:
        json.dump(j, fd, indent=4, sort_keys=True)

    if mode != None:
        os.chmod(fileName, mode)


def writeJsonToStdout(j) :
    """
    Write JSON to stdout.

    j: the JSON object to write
    """
    print(json.dumps(j, indent=4, sort_keys=True))


def saveFile(fileName, content, mode=None) :
    """
    Save content to a file.

    fileName: name of the file to write
    content: the content to write
    mode: the file permissions to set; default is: umask
    """
    with open(fileName, 'w') as fd:
        fd.write(content)

    if mode != None:
        os.chmod(fileName, mode)


def time2string(t):
    """
    Format time consistently
    
    t: the time to be formatted
    return: formatted time
    """
    ts  = time.gmtime(t)
    ret = time.strftime('%Y%m%d-%H%M%S', ts)
    return ret


def string2time(s):
    """
    Parse formatted timed consistently

    s: the string produced by time2string
    return: UNIX time
    """
    parsed = time.strptime(s, '%Y%m%d-%H%M%S')
    ret    = calendar.timegm(parsed)
    return ret

    
