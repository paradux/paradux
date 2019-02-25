#!/usr/bin/python
#
# Initial setup.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import paradux

def run(conf) :
    """
    Run this command with configuration conf
    """
    paradux.init_mount_config_data_image(conf)

    paradux.make_unavailable_config_data(conf)


def description() :
    return """
Sets up a Paradux installation for the first time.
"""
