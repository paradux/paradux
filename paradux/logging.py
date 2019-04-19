#!/usr/bin/python
#
# Logging functions
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import json
import logging
import logging.config
import os.path
import paradux.utils
import sys
import traceback

logging.config.dictConfig({
    'version'                  : 1,
    'disable_existing_loggers' : False,
    'formatters'               : {
        'standard' : {
            'format' : '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt' : '%Y%m%d-%H%M%S'
        },
    },
    'handlers' : {
        'default' : {
            'level'     : 'DEBUG',
            'formatter' : 'standard',
            'class'     : 'logging.StreamHandler',
            'stream'    : 'ext://sys.stderr'
        }
    },
    'loggers' : {
        '' : { # root logger
            'handlers'  : [ 'default' ],
            'level'     : 'WARNING',
            'propagate' : True
        }
    }
})

DEBUG = False
LOG   = logging.getLogger(sys.argv[0][ sys.argv[0].rfind('/')+1 : ] if sys.argv[0].rfind('/') >= 0 else sys.argv[0])

def initialize(
        verbosity = 0,
        debug     = False):
    """
    Invoked at the beginning of a script, this initializes logging.
    
    verbosity: integer capturing the level of verbosity (0 and higher)
    debug: yes or no: if yes, stop and wait for keyboard input in key locations
    """

    global LOG
    global DEBUG

    if verbosity == 1:
        LOG.setLevel('INFO')

    elif verbosity >= 2:
        LOG.setLevel('DEBUG')

    DEBUG = debug;


def trace(*args):
    """
    Emit a trace message.
    args: the message or message components
    """
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.debug(_constructMsg(True, False, args))


def isTraceActive() :
    """
    Is trace logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor(logging.DEBUG)


def info(*args):
    """
    Emit an info message.
    args: msg: the message or message components
    """
    if LOG.isEnabledFor(logging.INFO):
        LOG.info(_constructMsg(False, False, args))


def isInfoActive():
    """
    Is info logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor(logging.INFO)


def warning(*args):
    """
    Emit a warning message.
    args: the message or message components
    """

    if LOG.isEnabledFor(logging.WARNING):
        LOG.warn(_constructMsg(False, LOG.isEnabledFor(logging.DEBUG), args))


def isWarningActive():
    """
    Is warning logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor(logging.WARNING)


def error(*args):
    """
    Emit an error message.
    args: the message or message components
    """
    if LOG.isEnabledFor(logging.ERROR):
        LOG.error(_constructMsg(False, LOG.isEnabledFor(logging.DEBUG), args))


def isErrorActive():
    """
    Is error logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor(logging.ERROR)


def fatal(*args):
    """
    Emit a fatal error message and exit with code 1.
    args: the message or message components
    """
    if args:
        if LOG.isEnabledFor(logging.CRITICAL):
            LOG.critical(_constructMsg(False, LOG.isEnabledFor(logging.DEBUG), args))

    exit(1)


def isFatalActive():
    """
    Is fatal logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor(logging.CRITICAL)


def isDebugAndSuspendActive():
    """
    Is debug logging and suspending on?
    return: 1 or 0
    """
    return DEBUG;


def debugAndSuspend(*args):
    """
    Emit a debug message, and then wait for keyboard input to continue.
    args: the message or message components; may be empty
    return: 1 if debugAndSuspend is active
    """
    if DEBUG:
        if args:
            sys.stderr.write("DEBUG: " + _constructMsg(False, False, args) + "\n")

        sys.stderr.write("** Hit return to continue. ***\n")
        input();

    return DEBUG;


def _constructMsg(withLoc, withTb, *args):
    """
    Construct a message from these arguments.

    withLoc: construct message with location info
    withTb: construct message with traceback if an exception is the last argument
    args: the message or message components
    return: string message
    """
    if withLoc:
        frame  = sys._getframe(2)
        loc    = frame.f_code.co_filename
        loc   += '#'
        loc   += str(frame.f_lineno)
        loc   += ' '
        loc   += frame.f_code.co_name
        loc   += ':'
        ret = loc
    else:
        ret = ''

        
    def m(a):
        if a is None:
            return '<undef>'
        if callable(a):
            return a()
        if isinstance(a, OSError):
            return type(a).__name__ + ' ' + str(a)
        return a

    args2 = map(m, *args)
    ret += ' '.join(map(lambda o: str(o), args2))

    if withTb and len(*args) > 0:
        *_, last = iter(*args)
        if isinstance(last, BaseException):
            ret += ''.join(traceback.format_exception(type(last), last, last.__traceback__))

    return ret

