#!/usr/bin/python
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

import abc
import os
from paradux.configuration.report import Level, Report, ReportItem
import paradux.logging
import shutil


class Configuration:
    """
    Abstract superclass for all configurations. This defines code common
    to all of them.
    """
    def __init__(self, masterFile, tmpFile):
        """
        Constructor.

        masterFile: name of a JSON file containing the current master
        tmpFile: potential name of a JSON file containing the current in-progress edits to the master
        """
        self.masterFile = masterFile
        self.tmpFile    = tmpFile


    def editTempAndReport(self):
        """
        Create a copy of this configuration, and allow the user to edit
        it. Then, run an error check on it, and return a report.

        return: Report, or None if editing problem
        """
        paradux.logging.info('Editing temporary configuration file:', self.tmpFile)

        if not os.path.isfile(self.tmpFile):
            shutil.copyfile(self.masterFile, self.tmpFile)
            os.chmod(self.tmpFile, 0o600)

        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
            if paradux.utils.myexec(editor + " '" + self.tmpFile + "'"):
                paradux.logging.fatal('editing file failed')

        else:
            paradux.logging.error('No EDITOR environment variable set. Cannot edit file.')
            return None

        return self.createReport(self.tmpFile)


    @abc.abstractmethod
    def createReport(self, fileName):
        """
        Create a report for a candidate config file.

        fileName: name of the file to report on
        return: Report
        """
        return Report( [
            ReportItem( Level.ERROR, 'FIXME override' )
        ] )


    def promoteTemp(self):
        """
        Promote the temporary config JSON file to master. This presupposes
        that the temporary config JSON is valid.

        return: void
        """

        paradux.logging.info('Promoting temporary configuration file')

        # if temp config JSON file exists, move it to config JSON file
        paradux.logging.trace('file exists?', self.tmpFile)
        if os.path.isfile(self.tmpFile):
            paradux.logging.trace('promoting', self.tmpFile, '->', self.masterFile)
            os.replace(self.tmpFile, self.masterFile)


    def abortTempConfiguration(self):
        """
        Abort the editing of temporary config JSON file.

        return: void
        """

        paradux.logging.info('Aborting edit of temporary configuration file')

        if os.path.isfile(self.tmpFile):
            paradux.logging.trace('Deleting:', self.tmpFile)
            os.remove(self.tmpFile)

        else:
            paradux.logging.trace('No need to delete, does not exist:', self.tmpFile)
