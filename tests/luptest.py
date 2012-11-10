# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 22:00:25 2012

@author: darthlukan
"""

from lupdaterapi import Pacman
import logging
import time

logging.basicConfig(filename='/tmp/lupdatertests.log', level=logging.DEBUG)
logging.info(time.ctime() + ': script running...')
p = Pacman()
logging.info(time.ctime() + ': instance of Pacman() created')
p.pac_search('linux')
logging.info(time.ctime() + ': search term passed to Pacman instance')
print('Package search for "linux": ')
print(p.pac_search.pkinfo)
print('Search terms used: ')
print(p.pac_search.terms)
logging.info(time.ctime() + ': test complete.')


