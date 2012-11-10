#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Brian Tomlinson
# Contact: darthlukan@gmail.com
# Description: Simple update notifier for Liquid Lemur Linux, API.
# License: GPLv2

import sys
import time
import subprocess
import logging
import lupdater

# Create the log, set level to DEBUG so that all messages are available
logging.basicConfig(filename='/tmp/lupdater.log', level=logging.DEBUG)

# Global package list
'''List containing the packages available to be updated, defaulted to empty,
    package names are added via methods in the Pacman class.'''
paclist = []

class Pacman():
    '''Provides functions to call pacman and update the repos, as well as
    return a list with number of updates. '''
    def pac_update(self):
        '''Updates the repositories, notifies the user.'''
        subprocess.call(['/usr/bin/notify-send', 'Updating repositories for update check...'], shell=False)

        upd = subprocess.Popen('sudo pacman -Syy', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = upd.communicate()

    def pac_list(self):
        '''Creates a list of packages needing to be updated and counts them,
        displays the count in a notification for user action.'''
        subprocess.call(['/usr/bin/notify-send', 'Checking for updates...'], shell=False)

        # Clean up the list from previous checks so that we keep an accurate count.
        if len(paclist) > 0:
            for i in paclist:
                paclist.remove(i)

        lst = subprocess.Popen('pacman -Qu', shell=True, stdout=subprocess.PIPE)

        for line in lst.stdout:
            line.rstrip('\r\n')
            paclist.append(line)

        numupdates = len(paclist)

        if numupdates >= 1:
            subprocess.call(['/usr/bin/notify-send', '%s %s %s' % ('You have', numupdates, 'updates available!')], shell=False)
            # Here we set the status icon to change and start blinking
            lupblinker = lupdater.SystrayApp()
            lupblinker.blinker()
            lupblinker(sys.exit(0))
            logging.info(time.ctime() + ': lupdater had %s updates available.\n' % (numupdates))
        else:
            subprocess.call(['/usr/bin/notify-send', 'Your system is already up to date! :)'], shell=False)
            logging.info(time.ctime() + ': No updates available, system is up to date.')
        # "Future-proofing"
        return numupdates, paclist

    def pac_check_list(self, paclist):
        '''Checks specifically for linux kernel packages so let the user know
        of whether they need to reboot for changes to take effect.'''
        # TODO: Check for other packages such as modules that require system
        # restart to take effect.
        critical = []
        if len(paclist) > 0:
            for i in paclist:
                if i.startswith('linux'):
                    critical.append(i)

        if len(critical) >= 1:
            for i in critical:
                subprocess.call(['/usr/bin/notify-send',
                                 '%s %s' % (i, 'is a critical update, it requires a system restart to take effect.')], shell=False)

                logging.info(time.ctime() + ': Critical update detected, user notified via notify-send.')
        return critical, paclist

def run_me(x):
    '''Runs all of the modules in the Pacman class as a standalone script for
    automatic update checking, returns a zero status when complete.'''
    logging.info(time.ctime() + ': lupdater now running with sleep enabled process.')
    # Meat and Potatoes
    p = Pacman()
    p.pac_update()
    p.pac_list()
    p.pac_check_list(paclist)
    logging.info(time.ctime() + ': lupdater exiting normally.')
    return 0

# Lobbeth thy holy hand grenade!
if __name__ == '__main__':
    x = 0
    run_me(x)