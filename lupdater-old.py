#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Brian Tomlinson
# Contact: darthlukan@gmail.com
# Description: Simple update notifier for Liquid Lemur Linux,
# meant to be run via ~/.config/autostart/lupdater.desktop but
# can also be run from the applications menu.
# License: GPLv2

import gtk
import subprocess
import lupdaterapi

class SystrayApp():

    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file('/usr/share/icons/lupdater.png')
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip('Lemur Updater')
        self.lapi = lupdaterapi

    def blinker(self):
        if len(self.lapi.paclist) > 0:
            self.tray.set_from_file('/usr/share/icons/lupdater-alert.png')
            self.tray.set_blinking(True)

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)
        if self.tray.get_blinking() == True:
            self.tray.set_blinking(False)
            self.tray.set_from_file('/usr/share/icons/lupdater.png')

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

      # show about dialog
        about = gtk.MenuItem('About')
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

      # add run item for manual updates
        run = gtk.MenuItem('Check Updates')
        run.show()
        menu.append(run)
        run.connect('activate', self.lapi.run_me)

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
        about_dialog.set_version('1.2.1b')
        about_dialog.set_comments((u'System Tray interface to the Lemur Updater'))
        about_dialog.set_authors([u'Brian Tomlinson <darthlukan@gmail.com>'])
        about_dialog.run()
        about_dialog.destroy()

    def show_log(self, widget):
        subprocess.Popen('/usr/bin/leafpad /tmp/lupdater.log', shell=True)

# Let's roll!
if __name__ == '__main__':
    SystrayApp()
    gtk.main()
