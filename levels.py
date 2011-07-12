'''
levels.py
Provides the Level and LevelMenu classes
'''
import pygame,os
from menus import Menu, MenuEntry
from globalvalues import Renderable,Options,Menus,GlobalObjects
pygame.init()
def init():
    Menus.levels=LevelMenu()
class Level(Renderable):
    def __init__(self,worldnum,stagenum,datafile=None):
        Renderable.__init__(self)
        self.world=worldnum
        self.stage=stagenum
        if datafile:
            self.levelFromFile(datafile)
        else:
            self.levelFromNumber(worldnum,stagenum)
    
    def levelFromFile(self,datafile):
        #stub implementation of level loading
        print "Loading: "+datafile
    
    def levelFromNumber(self,worldnum,stagenum):
        self.levelFromFile("levels"+os.sep+"world"+str(worldnum)
        +os.sep+"stage"+str(stagenum))

    def startLevel(self):
        # draw the level, let the player do their thing
        pass

class LevelMenu(Menu):

    def updateMenu(self):
        Menus.levels=LevelMenu()
        GlobalObjects.renderingThread.renderobj=Menus.levels

    def goToWorld1():
        GlobalObjects.renderingThread.renderobj = Level(1,1)
        # just until I have an actual level to play
        GlobalObjects.unlockedWorlds = 2
        LevelMenu.updateMenu(Menus.levels)

    def goToWorld2():
        GlobalObjects.renderingThread.renderobj = Level(2,1)
        # just until I have an actual level to play
        GlobalObjects.unlockedWorlds = 3
        LevelMenu.updateMenu(Menus.levels)

    def goToWorld3():
        GlobalObjects.renderingThread.renderobj = Level(3,1)
        # just until I have an actual level to play
        GlobalObjects.unlockedWorlds = 4
        LevelMenu.updateMenu(Menus.levels)

    def goToWorld4():
        GlobalObjects.renderingThread.renderobj = Level(4,1)
        # just until I have an actual level to play
        GlobalObjects.unlockedWorlds = 1
        LevelMenu.updateMenu(Menus.levels)

    def returnToMain(self=None):
        GlobalObjects.escInUse = False
        GlobalObjects.renderingThread.renderobj=Menus.main
    
    levelentries=(
    MenuEntry("Back",returnToMain),
    MenuEntry("World 1",goToWorld1),
    MenuEntry("World 2",goToWorld2),
    MenuEntry("World 3",goToWorld3),
    MenuEntry("World 4",goToWorld4)
    )

    def __init__(self):
        Menu.__init__(self, LevelMenu.levelentries[0:GlobalObjects.unlockedWorlds+1])

    def draw(self,events):
        Menu.draw(self,events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.returnToMain()

