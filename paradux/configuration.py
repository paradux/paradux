#!/usr/bin/python
#
# Configuration of the Paradux installation.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import pathlib
import posixpath

DEFAULT_CONFIG_DATA_IMAGE      = posixpath.join(pathlib.Path.home(), '.paradux/config.img' )
DEFAULT_CONFIG_DATA_IMAGE_SIZE = 2**26 # 64M

class ParaduxConfiguration:
    """
    Collects information about the current Paradux installation
    """
    def __init__(
            self,
            config_data_image      = DEFAULT_CONFIG_DATA_IMAGE,
            config_data_image_size = DEFAULT_CONFIG_DATA_IMAGE_SIZE ) :

        self.config_data_image      = config_data_image
        self.config_data_image_size = config_data_image_size


    def get_config_data_image(self):
        """
        Obtain the path to the encrypted config data image
        """
        return self.config_data_image


    def get_config_data_image_size(self):
        """
        Obtain the desired size of the image containing the encrypted
        file system for the config data
        """
        return self.config_data_image_size


    def get_crypt_device_name(self):
        """
        Obtain the name of the device created by cryptsetup.
        """
        return 'paradux'


    def get_config_data_mountpoint(self):
        """
        Obtain the directory where the device created by cryptsetup
        will be mounted
        """
        return '.paradux-mount'

