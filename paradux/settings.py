#!/usr/bin/python
#
# Collects the settings for this instance of paradux
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import os
import os.path
import paradux.logging
import paradux.utils
import pathlib
import posixpath


# Default paradux data directory
DEFAULT_DIRECTORY = posixpath.join(pathlib.Path.home(), '.paradux')


def create(args):
    """
    Create a Settings objects from paradux defaults, overridden by command-
    line arguments if they are given.
    Note: this does not touch any of the private/encrypted info.

    args: parsed command-line arguments
    return: Settings object
    """
    if hasattr(args,'image_size'):
        return Settings(args.directory, args.image_size)
    else:
        return Settings(args.directory, None)


class Settings:
    """
    Collects information about the paradux settings in effect during this run

    directory: the paradux data directory
    """
    def __init__(self, directory, image_size) :
        if not os.path.isdir(directory):
            raise FileNotFoundError(directory)

        self.directory         = directory
        self.image_size        = image_size

        self.image_file        = self.directory + '/configuration.img'        # LUKS file
        self.crypt_device_name = 'paradux'                                    # short name of the device created by cryptsetup
        self.crypt_device_path = '/dev/mapper/' + self.crypt_device_name      # path name of the device created by cryptsetup
        self.image_mount_point = self.directory + '/configuration'            # mount point for the image
        self.config_file       = self.image_mount_point + '/paradux.json'     # master configuration JSON
        self.temp_config_file  = self.image_mount_point + '/paradux.tmp.json' # configuration JSON currently being edited

        self.recovery_key_size = 32 # LUKS parameter
        self.recovery_key_slot =  7 # LUKS parameter
        self.everyday_key_slot =  0 # LUKS parameter


    def createImage(self,recovery_secret):
        """
        Create the initial LUKS image. This does not initialize anything
        inside the image.

        recovery_secret:
        return: void
        throws: exception if the image exists already
        """

        paradux.logging.info('Creating image: ', self.image_file)

        # if image exists, throw exception
        if self._image_exists():
            raise FileExistsError(self.image_file)

        if self._cryptsetup_isopen():
            raise FileExistsError(self.crypt_device_path)
            
        # create image file
        self._image_create()

        # set up cryptsetup on it
        self._cryptsetup_open()
        
        # format image
        self._image_format()

        # unsetup cryptsetup
        self._cryptsetup_close()


    def mountImage(self):
        """
        Mount the LUKS image at the designated mount point

        return: void
        """

        paradux.logging.info('Mounting image: ', self.image_file)

        # check image exists
        if not self._image_exists():
            raise FileNotFoundError(self.image_file)

        # cryptsetup
        self._cryptsetup_open()
       
        # mount
        self._image_mount()


    def initConfiguration(self):
        """
        Initialize this configuration by creating default files inside the image.        

        return: void
        """

        paradux.logging.info('Initializing configuration -- FIXME')

        # check image mounted
        # check that no config JSON exists

        paradux.logging.fatal('FIXME')


    def editTempConfiguration(self):
        """
        Edit the temporary config JSON file. If it does not exist yet,
        create it from the master.

        return: True if saved affirmatively; False if editing was aborted
        """

        paradux.logging.info('Editing temporary configuration file -- FIXME')

        # check that config JSON file exists
        # if no temp config JSON file, copy
        # edit tmp config JSON

        paradux.logging.fatal('FIXME')


    def abortTempConfiguration(self):
        """
        Abort the editing of temporary config JSON file.

        return: void
        """

        paradux.logging.info('Aborting edit of temporary configuration file -- FIXME')

        # if temp config JSON file exists, delete

        paradux.logging.fatal('FIXME')


    def checkTempConfiguration(self):
        """
        Run checks on the temporary config JSON file, and return a report.

        return: ConfigurationReport
        """

        paradux.logging.info('Checking temporary configuration file')

        # create report
        # if no temp config JSON file exists, return empty report
        paradux.logging.trace('file exists?', self.temp_config_file)
        if os.path.is_file(self.temp_config_file):
            return paradux.configuration.analyze_json(self.temp_config_file)
        else:
            return ConfigurationReport()


    def promoteTempConfiguration(self):
        """
        Promote the temporary config JSON file to master. This presupposes
        that the temporary config JSON is valid.

        return: void
        """

        paradux.logging.info('Promoting temporary configuration file')

        # if temp config JSON file exists, move it to config JSON file
        paradux.logging.trace('file exists?', self.temp_config_file)
        if os.path.is_file(self.temp_config_file):
            paradux.logging.trace('promoting', self.temp_config_file, '->', self.config_file)
            os.replace(self.temp_config_file, self.config_file)


    def getConfiguration(self):
        """
        Obtain the current configuration from the master config JSON.

        return: Configuration object
        """

        ret = paradux.configuration.parse_json(self.config_file)
        return ret


    def cleanup(self):
        """
        Do whatever necessary to clean up and make private data
        inaccessible again.

        return: void
        """

        paradux.logging.info('Cleaning up')

        # if image is mounted, unmount
        if self._image_ismounted():
            self._image_umount()

        # if device exists, remove device
        if self._cryptsetup_isopen():
            self._cryptsetup_close()


    def _image_exists(self):
        """
        Determine whether the LUKS image exists

        return: True or False
        """
        paradux.logging.trace('file exists?', self.image_file)
        return os.path.isfile(self.image_file)


    def _image_create(self):
        """
        Create the image file

        return: void
        """
        image_dir = os.path.dirname(self.image_file)
        if not os.path.isdir(image_dir):
            paradux.logging.trace('creating path to', image_dir)
            os.makedirs(image_dir)

        with open(self.image_file, "w") as file:
            paradux.logging.trace('creating file', self.image_file, 'of size', self.image_size)
            file.truncate(self.image_size)

        if paradux.utils.myexec(
                  'cryptsetup luksFormat'
                + ' --batch-mode'
                + ' --key-slot=' + str(self.recovery_key_slot)
                + ' --key-file=-' # read from stdin
                + " '" + self.image_file + "'",
                recovery_secret):
            paradux.logging.fatal('cryptsetup luksFormat failed')

        print("""Please enter your everyday passphrase for paradux when asked.
Make sure this passphrase is long, hard to guess, and DO NOT write it
down anywhere. (If you lose it, paradux lets you recover with the help
of your stewards.)""")

        if paradux.utils.myexec(
                  'cryptsetup luksAddKey'
                + ' --batch-mode'
                + ' --key-slot=' + str(self.everyday_key_slot)
                + ' --key-file=-' # read from stdin
                + " '" + self.image_file + "'",
                recovery_secret):
            paradux.logging.fatal('cryptsetup luksAddKey failed')


    def _image_format(self):
        """
        Format the image by means of the cryptsetup device

        return: void
        """
        if paradux.utils.myexec("sudo mkfs.ext4 '" + self.crypt_device_path + "'"):
            paradux.logging.fatal('making ext4 filesystem failed')


    def _image_mount(self):
        """
        Mount the LUKS image

        return: void
        """
        paradux.logging.trace('mount path exists?', self.image_mount_point)
        if not os.path.isdir(self.image_mount_point):
            paradux.logging.trace('creating path to mount point', self.image_mount_point)
            os.makedirs(self.image_mount_point, mode=700)

        if paradux.utils.myexec("sudo mount '" + self.crypt_device_path + "' '" + self.image_mount_point + "'"):
            paradux.logging.fatal('mount failed')


    def _image_ismounted(self):
        """
        Determine whether the LUKS image is mounted

        return: True or False
        """
        paradux.logging.trace('is mounted?', self.image_mount_point)
        p = pathlib.Path(self.image_mount_point)
        return p != None and p.is_mount()


    def _image_umount(self):
        """
        Unmount the LUKE image.

        return: void
        """
        if paradux.paradux.utils.myexec("sudo umount '" + self.crypt_device_path + "'"):
            paradux.logging.fatal('umount failed')
    

    def _cryptsetup_open(self):
        """
        Create/open the cryptsetup device
        """
        if paradux.utils.myexec("sudo cryptsetup open '" + self.image_file + "' '" + self.crypt_device_path + "'"):
            paradux.logging.fatal('cryptsetup open failed')
        

    def _cryptsetup_isopen(self):
        """
        Determine whether the cryptsetup device is open

        return: True or False
        """
        paradux.logging.trace('is block device?', self.crypt_device_path)
        p = pathlib.Path(self.crypt_device_path)
        return p != None and p.is_block_device()
        

    def _cryptsetup_close(self):
        """
        Close the cryptsetup device
        """
        if paradux.utils.myexec("sudo cryptsetup close '" + self.crypt_device_name + "'"):
            paradux.logging.fatal('cryptsetup close failed')

