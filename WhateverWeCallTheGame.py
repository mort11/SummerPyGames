#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       WhateverWeCallTheGame.py
#       
#       Copyright Contributors
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       
import pygame, objects, levels,menus,renderthread
from globalvalues import GlobalObjects
pygame.init()
def main():
    options=menus.OptionsMenu()
    testthread=renderthread.RenderThread()
    testthread.renderobj=options
    testthread.start()
    while True:
        GlobalObjects.lock.acquire()
        event = GlobalObjects.event
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            GlobalObjects.lock.release()
            break
        GlobalObjects.lock.release()
    testthread.running=False
    return 0

if __name__ == '__main__':
	main()

