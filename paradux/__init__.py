#!/usr/bin/python
#
# Setup the package.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import argparse
import importlib
import os.path
import paradux.commands
import paradux.configuration
import paradux.log
import paradux.utils
import sys

def run():
    """
    Main entry point into Paradux
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('command',                          help='The subcommand to invoke. Use "list" to show available sub-commands.')
    parser.add_argument('option', nargs=argparse.REMAINDER, help='Options for the sub-command.')
    parser.add_argument('-v', '--verbose',  action="count", help='Display extra output. May be repeated for even more output.')

    args,remaining = parser.parse_known_args(sys.argv[1:])
    cmd = args.command
    conf = configuration.ParaduxConfiguration()

    try:
        cmds = paradux.utils.findSubmodules(paradux.commands)
        if(cmd in cmds):
            mod=importlib.import_module('paradux.commands.' + cmd)
            mod.run(conf)
        else:
            print('Command not found')
    except log.FatalException as e:
        exit(1)


def init_mount_config_data_image(conf):
    """
    Initialize a new Paradux instance
    """
    config_data_image      = conf.get_config_data_image()
    config_data_image_size = conf.get_config_data_image_size()
    crypt_device_name      = conf.get_crypt_device_name()

    if os.path.isfile(config_data_image):
        log.fatal('File exists already: ' + str(config_data_image))

    if not os.path.isdir(os.path.dirname(config_data_image)):
        os.makedirs(os.path.dirname(config_data_image))

    with open(config_data_image, "w") as file:
        file.truncate(config_data_image_size)

    print( """Please enter your day-to-day passphrase for the Paradux configuration data
when asked. Make sure this password is long, hard to guess, and DO NOT
write this password down anywhere. (If you lose the password, Paradux
lets you recover with the help of your Stewards.)
""" )

    if utils.myexec( "cryptsetup luksFormat --batch-mode '" + config_data_image + "'" ):
        log.fatal('cryptsetup luksFormat failed')

    cryptsetup_open(conf)

    if utils.myexec("sudo mkfs.ext4 '/dev/mapper/" + crypt_device_name + "'"):
        log.fatal('making ext4 filesystem failed')

    mount_config_data_image(conf)



def make_available_config_data(conf):
    """
    Convenience method for the common case
    """
    cryptsetup_open(conf)
    mount_config_data_image(conf)


def make_unavailable_config_data(conf):
    """
    Convenience method for the common case
    """
    umount_config_data_image(conf)
    cryptsetup_close(conf)

    
def cryptsetup_open(conf):
    config_data_image      = conf.get_config_data_image()
    crypt_device_name      = conf.get_crypt_device_name()

    if utils.myexec("sudo cryptsetup open '" + config_data_image + "' '" + crypt_device_name + "'"):
        log.fatal('cryptsetup open failed')


def mount_config_data_image(conf):
    crypt_device_name      = conf.get_crypt_device_name()
    config_data_mountpoint = conf.get_config_data_mountpoint()

    if not os.path.isdir(config_data_mountpoint):
        os.makedirs(config_data_mountpoint)

    if utils.myexec("sudo mount '/dev/mapper/" + crypt_device_name + "' '" + config_data_mountpoint + "'"):
        log.fatal('mount failed')

    
def umount_config_data_image(conf):
    crypt_device_name = conf.get_crypt_device_name()

    if utils.myexec("sudo umount '/dev/mapper/" + crypt_device_name + "'"):
        log.fatal('umount failed')
    

def cryptsetup_close(conf):
    crypt_device_name = conf.get_crypt_device_name()

    if utils.myexec("sudo cryptsetup close '" + crypt_device_name + "'"):
        log.fatal('cryptsetup close failed')
