'''
levels.py
Provides the Level and LevelMenu classes
'''
import pygame,menus,os
pygame.init()

class Level:
    def __init__(self,worldnum,levelnum,datafile=None):
        if datafile == None:
            self.levelFromNumber(worldnum,levelnum)
        else:
            self.levelFromFile(datafile)
    
    def levelFromFile(self,datafile):
        #stub implementation of level loading
        print "Loading: "+datafile
    
    def levelFromNumber(self,worldnum,levelnum):
        self.levelFromFile("levels"+os.sep+"world"+str(worldnum)
        +os.sep+"level"+str(levelnum))

    def startLevel(self):
        # draw the level, let the player do their thing
        pass

class LevelMenu(menus.Menu):
    def __init__(self):
        menus.Menu.__init__(dict)
