#!/usr/bin/python
#
# Logging functions
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import sys
import traceback

class FatalException(BaseException):
    def __init__(self, msg) :
        self.msg = msg

    def __str__(self):
        return self.msg

def fatal(msg):
    if isinstance(msg,BaseException):
        msg = traceback.format_exc() # Generates stack trace and message

    sys.stderr.write('FATAL: ' + msg + "\n" )
    raise FatalException( msg )

def error(msg):
    sys.stderr.write('ERROR: ' + msg + "\n")

def trace(msg):
    sys.stderr.write('TRACE: ' + msg + "\n")
