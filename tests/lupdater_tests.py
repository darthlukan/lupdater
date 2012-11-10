#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Brian Tomlinson
# Contact: darthlukan@gmail.com
# Description: Simple update notifier for Liquid Lemur Linux,
# meant to be run via ~/.config/autostart/lupdater.desktop but
# can also be run from /usr/bin with '&' for manual setups.
# License: GPLv2

from nose.tools import *
import gtk
import time
import subprocess

# Timer variable. Changing this number will adjust the sleeper.
# The value is in seconds, the default is 4 hours.
# TODO: Settings like these should really be read from ~/.config/foo.py.
rest = 720

# Create the log
open('/tmp/lupdater.log', 'w+')

# We want to append the existing log, not overwrite lines.
# TODO: we should really clear the log once it reaches a certain size for disk
# space issues on systems that don't get rebooted often.
f = open('/tmp/lupdater.log', 'a+')

class SystrayApp():
    
    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file('/usr/share/icons/lupdater.png') 
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip('Lemur Updater')
		
    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

	  # show about dialog
        about = gtk.MenuItem('About')
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

	  # add run item for manual updates
        p = Pacman()
        run = gtk.MenuItem('Check Updates')
        run.show()
        menu.append(run)
        run.connect('activate', p.run_me)
        
        #add log checker, open in leafpad for now
        chklog = gtk.MenuItem('View Log')
        chklog.show()
        menu.append(chklog)
        chklog.connect('activate', self.show_log)
  
        # add quit item
        quit = gtk.MenuItem('Quit')
        quit.show()
        menu.append(quit)
        quit.connect('activate', gtk.main_quit)
        
        menu.popup(None, None, gtk.status_icon_position_menu,
	            event_button, event_time, self.tray)

    def  show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent (True)
        about_dialog.set_icon_name ('Lemur Updater')
        about_dialog.set_name('Lemur Updater')
        about_dialog.set_version('1.1')
        about_dialog.set_comments((u'System Tray interface to the Lemur Updater'))
        about_dialog.set_authors([u'Brian Tomlinson <darthlukan@gmail.com>'])
        about_dialog.run()
        about_dialog.destroy()
        
    def show_log(self, widget):
        subprocess.Popen('/usr/bin/leafpad /tmp/lupdater.log', shell=True)
  
class Sleeper():
    '''Sets the sleep time to 4 Hours by default.'''
    
    def slp_time(self):
        p = Pacman()
        counter = 0
        # Timer loop, TODO: FIX ME NAO!!!
        while rest >= 1:
            counter += 1
            if counter == rest:
                f.write(time.ctime() + ': lupdater woke up.\n')
                f.flush()
                p.run_me(1)
                f.write(time.ctime() + ': lupdater going to sleep.\n')
                f.flush()
                counter = 0

class Pacman():
    '''Provides functions to call pacman and update the repos, as well as return a list with number of updates. '''

    def pac_update(self):

        subprocess.call(['/usr/bin/notify-send', 'Updating repositories for update check...'], shell=False)        
        
        upd = subprocess.Popen('sudo pacman -Syy', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = upd.communicate()

    def pac_list(self):
        
        subprocess.call(['/usr/bin/notify-send', 'Checking for updates...'], shell=False)        
        
        paclist = []
    
        lst = subprocess.Popen('pacman -Qu', shell=True, stdout=subprocess.PIPE)

        for line in lst.stdout:
            line.rstrip('\r\n')
            paclist.append(line)

        numupdates = len(paclist)

        if numupdates >= 1:
            subprocess.call(['/usr/bin/notify-send', '%s %s %s' % ('You have', numupdates, 'updates available!')], shell=False)
            f.write(time.ctime() + ': lupdater had updates available.\n')
            f.flush()

        else:
            subprocess.call(['/usr/bin/notify-send', 'Your system is already up to date! :)'], shell=False)
            f.write(time.ctime() + ': System is up to date.\n')
            f.flush()
        # "Future-proofing"    
        return numupdates, paclist

    def run_me(self, widget):
    
        # Write to the log, f.flush() helps when using tail on lupdater.log.
        f.write(time.ctime() + ': lupdater running...\n')
        f.flush()
        # Meat and Potatoes
        self.pac_update()
        self.pac_list()
        
        # TODO, see Sleeper()
        #s = Sleeper()
        #s.slp_time()
    
# Let's roll!
if __name__ == '__main__':
    SystrayApp()
    gtk.main()
