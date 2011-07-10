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
import pygame, objects, levels,menus,threads
from globalvalues import GlobalObjects,Events
pygame.init()
def main():
    options=menus.OptionsMenu()
    render=threads.RenderThread()
    render.renderobj=options
    render.start()
    eventthread=threads.EventThread()
    eventthread.start()
    def cleanup():
        render.killed.set()
        with Events.trigger,Events.done:
            Events.trigger.wait()
        render.join()
        eventthread.killed.set()
        eventthread.join()
    running = True
    while running:
        with Events.trigger:
            for event in Events.events:
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    with GlobalObjects.lock:
                        if GlobalObjects.escInUse:
                            GlobalObjects.lock.release()
                            break
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
        with Events.trigger,Events.done:
            Events.trigger.wait()
    cleanup()
    return 0

if __name__ == '__main__':
	main()

