#!/usr/bin/env python
# Author: Brian Tomlinson
# Contact: brian@brianctomlinson.com, darthlukan@gmail.com
# Description: Simple update notifier for Arch Linux,
# meant to be run via ~/.config/autostart/lupdater.desktop but
# can also be run from the applications menu.
# License: GPLv2

import os
import pwd
import sys
import time
import notify2
import logging
import platform
import subprocess
from PyQt4 import QtGui


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        menu = QtGui.QMenu(parent)
        menu.addAction("About", self.about)
        menu.addAction("Check Updates", self.check_updates)
        menu.addAction("Exit", self.exit)

        self.setContextMenu(menu)

    def exit(self):
        sys.exit(0)

    def check_updates(self):

        system = Setup().distro()

        if system['distro'] == 'arch':
            return Setup().arch()
        elif system['distro'] == 'debian':
            return Setup().debian()
        elif system['distro'] == 'redhat':
            return Setup().redhat()
        else:
            return note_set_send(title="Not yet implemented", body="")

    def about(self):
        note_set_send(title="Not yet implemented", body="")


class Setup(object):

    def __init__(self):
        self.paclist = []
        self.critical = []
        self.numupdates = 0
        self.system = {'distro': '',
                       'pkgmgr': '',
                       'repoupd': '',
                       'pkglist': ''}

    def distro(self):

        debian = ['ubuntu', 'linuxmint', 'soluos', 'debian', 'peppermint']
        redhat = ['redhat', 'fedora', 'centos']
        distro = platform.linux_distribution()[0].lower()

        if distro == 'arch':
            self.system['distro'] = 'arch'
            self.system['pkgmgr'] = 'pacman'
            self.system['repoupd'] = '-Syy'
            self.system['pkglist'] = '-Qu'
        elif distro in debian:
            self.system['distro'] = 'debian'
            self.system['pkgmgr'] = 'apt-get'
            self.system['repoupd'] = 'update'
            self.system['pkglist'] = '-s upgrade'
        elif distro in redhat:
            self.system['distro'] = 'redhat'
            self.system['pkgmgr'] = 'yum'
            self.system['repoupd'] = 'update'
            self.system['pkglist'] = 'list updates'
        else:
            print('Your distribution is not supported.')
            raise NotImplementedError

        return self.system

    def user(self):
        pass

    def arch(self):
        p = Pacman()
        p.update()
        p.list_packs()
        return True

    def debian(self):
        a = Apt()
        a.update()
        a.list_packs()
        return True

    def redhat(self):
        r = Redhat()
        r.update()
        r.list_packs()
        return True


class Log(object):

    def __init__(self):
        logging.basicConfig(filename='/tmp/lupdater.log', level=logging.DEBUG)

    def updates(self, numupdates):
        if numupdates > 0:
            logging.info(time.ctime() + ': lupdater had %s updates available.\n' % numupdates)
        else:
            logging.info(time.ctime() + ': No updates available, system is up to date.')

    def critical(self, crit):
        if crit > 0:
            logging.info(time.ctime() + ': Critical update detected, user notified via notify-send.')


class Pacman(Setup):
    """Provides functions to call pacman and update the repos, as well as
    return a list with number of updates. """

    def __init__(self):
        setup = Setup()
        self.system = setup.distro()
        self.paclist = setup.paclist
        self.critical = setup.critical
        self.numupdates = setup.numupdates

    def update(self):
        """Updates the repositories, notifies the user."""

        pkgmgr = self.system['pkgmgr']
        repoupd = self.system['repoupd']
        args = ["/usr/bin/sudo", pkgmgr, repoupd]

        note_set_send(title="Updating repos", body="Getting latest package lists.")

        upd = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        stdout, stderr = upd.communicate()

        return True

    def list_packs(self):
        """Creates a list of packages needing to be updated and counts them,
        displays the count in a notification for user action."""

        pkgmgr = self.system['pkgmgr']
        pkglist = self.system['pkglist']
        args = [pkgmgr, pkglist]

        note_set_send(title="Checking packages", body="...")

        # Clean up the list from previous checks so that we keep an accurate count.
        if len(self.paclist) > 0:
            for i in self.paclist:
                self.paclist.remove(i)

        lst = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)

        for line in lst.stdout:
            line = str(line, encoding="utf8")
            line.rstrip("\r\n")
            self.paclist.append(line)

        self.numupdates = len(self.paclist)

        if self.numupdates >= 1:
            note_set_send(title="Updates Available!", body="You have %i updates available." % self.numupdates)
            self.check_critical(self.paclist)
        else:
            note_set_send(title="Nothing to do!", body="Your system is up to date.")

        return self.paclist

    def check_critical(self, paclist):
        """Checks specifically for linux kernel packages to let the user know
        of whether they need to reboot for changes to take effect."""
        # TODO: Check for other packages such as modules that require system/service restart.
        if len(paclist) > 0:
            for i in paclist:
                if i.startswith('linux'):
                    self.critical.append(i)

        if len(self.critical) >= 1:
            for i in self.critical:
                note_set_send(title="Critical Update!", body="%s is a critical update and requires a restart." % i)

        return self.critical


class Apt(Setup):

    def __init__(self):
        setup = Setup()
        self.system = setup.distro()
        self.paclist = setup.paclist
        self.critical = setup.critical
        self.numupdates = setup.numupdates

    def update(self):
        pass

    def list_packs(self):
        pass

    def check_critical(self):
        pass


class Redhat(Setup):

    def __init__(self):
        setup = Setup()
        self.system = setup.distro()
        self.paclist = setup.paclist
        self.critical = setup.critical
        self.numupdates = setup.numupdates

    def udpate(self):
        pass

    def list_packs(self):
        pass

    def check_critical(self):
        pass


def note_set_send(title, body):
    """ Sends and sends notification to DBUS for display."""
    notify2.init('lupdater')
    n = notify2.Notification(title, body)
    return n.show()


def main():

    version = sys.version

    if version.startswith('3'):

        app = QtGui.QApplication(sys.argv)
        w = QtGui.QWidget()
        trayIcon = SystemTrayIcon(QtGui.QIcon("lupdater.png"), w)
        trayIcon.show()

        sys.exit(app.exec_())

    else:
        sys.exit('This program requires Python 3.x.x!')


if __name__ == '__main__':
    main()