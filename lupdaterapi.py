#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Brian Tomlinson
# Contact: darthlukan@gmail.com
# Description: Simple update notifier for Liquid Lemur Linux, API.
# License: GPLv2

import sys
import pyalpm
import logging
import subprocess

# Global log config
logging.basicConfig(filename='/tmp/lupdater.log',  level=logging.DEBUG)

class Pacman():
    '''Provides methods for interacting with packages as Pacman would using pyalpm.'''
    # For now: Use subprocess to call Pacman until code map is complete.

    def __init__(self):
        '''Setup handler and other alpm objects.'''

        handler = pyalpm.Handle('/', '/var/lib/pacman')
        localdb = handler.get_localdb()
        syncdb = handler.get_syncdbs()
        lemurdb = handler.register_syncdb('lemur',  pyalpm.SIG_DATABASE_OPTIONAL)
        coredb = handler.register_syncdb('core',  pyalpm.SIG_DATABASE_OPTIONAL)
        extradb = handler.register_syncdb('extra',  pyalpm.SIG_DATABASE_OPTIONAL)
        commdb = handler.register_syncdb('community',  pyalpm.SIG_DATABASE_OPTIONAL)
        multidb = handler.register_syncdb('multilib',  pyalpm.SIG_DATABASE_OPTIONAL)

        repos = {
        'lemur': lemurdb,
        'core': coredb,
        'extra': extradb,
        'community': commdb,
        'multilib': multidb,
        }

    def pac_alpm_version(self):
        '''Returns the installed version of libalpm.'''

        pyalpm.alpmversion()

    def pac_syncdb(self):
        '''Syncs the repos as with Pacman -Syy so that we are always current.'''
        upd = subprocess.Popen('sudo pacman -Syy', shell=False,
                               stdout=subprocess.PIPE)
        stdout, stderr = upd.communicate()

    def pac_search(self, *args):
        '''Searches for packages based on args as with Pacman -Ss'''

        terms = []
        pkinfo = {}

        for each in args:
            terms.append(each)

        ss = subprocess.Popen(['pacman', '-Ss '] + terms, shell=False,
                             stdout=subprocess.PIPE)
        stdout, stderr = ss.communicate()

        for line in ss.stdout:
            line.rstrip('\r\n')
            pkinfo.append(line)

        return pkinfo, terms

    def pac_pkginfo(self,  *args):
        '''Gets package info based on args as with Pacman -Si.'''

    def pac_sys_upgrade(self):
        '''Runs system upgrade as Pacman -Syyuu.'''

    def pac_pkgrm(self,  *args):
        '''Removes named package from system as with Pacman -R.'''

    def pac_pkrmdd(self,  *args):
        '''Removes named package from system as with Pacman -Rdd'''

    def pac_pkginst(self, *args):
        '''Installs named package as with Pacman -S.'''