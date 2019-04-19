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

logging.config.dictConfig( {
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
} )

DEBUG = False
LOG   = logging.getLogger( sys.argv[0][ sys.argv[0].rfind( '/' )+1 : ] if sys.argv[0].rfind( '/' ) >= 0 else sys.argv[0] )

def initialize(
        verbosity = 0,
        debug     = False ):
    """
    Invoked at the beginning of a script, this initializes logging.
    
    verbosity: integer capturing the level of verbosity (0 and higher)
    debug: yes or no: if yes, stop and wait for keyboard input in key locations
    """

    global LOG
    global DEBUG

    if verbosity == 1:
        LOG.setLevel( 'INFO' )

    elif verbosity >= 2:
        LOG.setLevel( 'DEBUG' )

    DEBUG = debug;


def trace(*args):
    """
    Emit a trace message.
    args: the message or message components
    """
    if LOG.isEnabledFor( logging.DEBUG ):
        LOG.debug( _constructMsgWithLocation( args ))


def isTraceActive() :
    """
    Is trace logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor( logging.DEBUG )


def info(*args):
    """
    Emit an info message.
    args: msg: the message or message components
    """
    if LOG.isEnabledFor( logging.INFO ):
        LOG.info( _constructMsg( args ))


def isInfoActive():
    """
    Is info logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor( logging.INFO )


def warning(*args):
    """
    Emit a warning message.
    args: the message or message components
    """

    if LOG.isEnabledFor( logging.WARNING ):
        LOG.warn( _constructMsg( args ))


def isWarningActive():
    """
    Is warning logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor( logging.WARNING )


def error(*args):
    """
    Emit an error message.
    args: the message or message components
    """
    if LOG.isEnabledFor( logging.ERROR ):
        LOG.error( _constructMsg( args ))


def isErrorActive():
    """
    Is error logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor( logging.ERROR )


def fatal(*args):
    """
    Emit a fatal error message and exit with code 1.
    args: the message or message components
    """
    if args:
        # print stack trace when debug is on
        if DEBUG:
            traceback.print_stack( sys.stderr )

        if LOG.isEnabledFor( logging.CRITICAL ):
            LOG.critical( _constructMsg( args ))

    exit( 1 )


def isFatalActive():
    """
    Is fatal logging on?
    return: 1 or 0
    """
    return LOG.isEnabledFor( logging.CRITICAL )


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
            sys.stderr.write( "DEBUG: " + _constructMsg( args ) + "\n" )

        sys.stderr.write( "** Hit return to continue. ***\n" )
        input();

    return DEBUG;


def _constructMsgWithLocation( *args):
    """
    Construct a message from these arguments.
    args: the message or message components
    return: string message
    """
    # first location in code: <file>#<line> <function>:
    frame  = sys._getframe(2)
    ret    = frame.f_code.co_filename
    ret   += '#'
    ret   += str( frame.f_lineno )
    ret   += ' '
    ret   += frame.f_code.co_name
    ret   += ':'

    # then arguments
    def m(a):
        if a is None:
            return '<undef>'
        if callable(a):
            return a()
        return a

    args2 = map( m, args )
    ret += ''.join( map( lambda o: ' ' + str(o), *args2 ))
    return ret


def _constructMsg( *args ):
    """
    Construct a message from these arguments.
    args: the message or message components
    return: string message
    """
    def m(a):
        if a is None:
            return '<undef>'
        if callable(a):
            return a()
        return a

    args2 = map( m, args )
    ret = ' '.join( map( lambda o: str(o), *args2 ))
    return ret

