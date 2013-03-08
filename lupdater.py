#!/usr/bin/env python
# Author: Brian Tomlinson
# Contact: brian@brianctomlinson.com, darthlukan@gmail.com
# Description: Simple update notifier for Arch Linux,
# meant to be run via ~/.config/autostart/lupdater.desktop but
# can also be run from the applications menu.
# License: GPLv2

import os
import sys
import time
import logging
import subprocess
from PyQt4 import QtGui


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        menu = QtGui.QMenu(parent)
        menu.addAction("Check Updates", self.check_updates)
        menu.addAction("Exit", self.exit)

        self.setContextMenu(menu)

    def exit(self):
        sys.exit(0)

    def check_updates(self):

        uname = os.uname()
        if uname[2].endswith('ARCH'):
            p = Pacman()
            p.pac_update()
            return p.pac_list()
        else:
            sys.exit('This program only understands Pacman at this point. You\'re package manager is unsupported.')


class Pacman(object):
    """Provides functions to call pacman and update the repos, as well as
    return a list with number of updates. """

    def __init__(self):
        self.paclist = []
        self.critical = []
        self.numupdates = 0

    def pac_update(self):
        """Updates the repositories, notifies the user."""

        subprocess.call(['/usr/bin/notify-send', 'Updating repositories for update check...'], shell=False)

        upd = subprocess.Popen('/usr/bin/sudo pacman -Syy', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = upd.communicate()

        return True

    def pac_list(self):
        """Creates a list of packages needing to be updated and counts them,
        displays the count in a notification for user action."""

        subprocess.call(['/usr/bin/notify-send', 'Checking for updates...'], shell=False)

        # Clean up the list from previous checks so that we keep an accurate count.
        if len(self.paclist) > 0:
            for i in self.paclist:
                self.paclist.remove(i)

        lst = subprocess.Popen('/usr/bin/pacman -Qu', shell=True, stdout=subprocess.PIPE)

        for line in lst.stdout:
            line = str(line, encoding="utf8")
            line.rstrip("\r\n")
            self.paclist.append(line)

        self.numupdates = len(self.paclist)

        if self.numupdates >= 1:
            subprocess.call(['/usr/bin/notify-send',
                             '%s %s %s' % ('You have', self.numupdates, 'updates available!')], shell=False)
            logging.info(time.ctime() + ': lupdater had %s updates available.\n' % self.numupdates)
        else:
            subprocess.call(['/usr/bin/notify-send', 'Your system is already up to date! :)'], shell=False)
            logging.info(time.ctime() + ': No updates available, system is up to date.')

        return self.paclist

    def pac_check_list(self, paclist):
        """Checks specifically for linux kernel packages to let the user know
        of whether they need to reboot for changes to take effect."""
        # TODO: Check for other packages such as modules that require system
        if len(paclist) > 0:
            for i in paclist:
                if i.startswith('linux'):
                    self.critical.append(i)

        if len(self.critical) >= 1:
            for i in self.critical:
                subprocess.call(['/usr/bin/notify-send',
                                 '%s %s' % (i, 'is a critical update, it requires a system restart to take effect.')],
                                shell=False)

            logging.info(time.ctime() + ': Critical update detected, user notified via notify-send.')

        return self.critical


def main():

    version = sys.version

    if version.startswith('3'):

        logging.basicConfig(filename='/tmp/lupdater.log', level=logging.DEBUG)

        app = QtGui.QApplication(sys.argv)
        w = QtGui.QWidget()
        trayIcon = SystemTrayIcon(QtGui.QIcon("lupdater.png"), w)
        trayIcon.show()

        sys.exit(app.exec_())

    else:
        sys.exit('This program requires Python 3.x.x!')


if __name__ == '__main__':
    main()