'''
levels.py
Provides the Level and LevelMenu classes
'''
import pygame,os
from run_game import Game
from objects import Object
from menus import Menu, MenuEntry
from globalvalues import Renderable,Options,Menus,GlobalObjects
pygame.init()
class Level(Renderable):
    def __init__(self,worldnum,stagenum,datafile=None):
        Renderable.__init__(self)
        self.world=worldnum
        self.stage=stagenum
        self.time=-2000
        self.size = (0,0)
        self.background = pygame.image.load("assets"+os.sep+"backgrounds"
        +os.sep+"world"+str(worldnum)+".png")
        if datafile:
            self.levelFromFile(datafile)
        else:
            self.levelFromNumber(worldnum,stagenum)

    def prettyName(self):
        return 'World '+ str(self.world)+' - Stage '+str(self.stage)
    
    def levelFromFile(self,datafile):
        #stub implementation of level loading
        print "Loading: "+datafile
        self.objectdict=None
    
    def levelFromNumber(self,worldnum,stagenum):
        self.levelFromFile("levels"+os.sep+"world"+str(worldnum)
        +os.sep+"stage"+str(stagenum))

    def startLevel(self):
        # draw the level intro
        self.screen.fill((0,0,0))
        levelintro=pygame.font.SysFont('liberationsans',32)
        screencenter=(self.screen.get_width()/2,self.screen.get_height()/2)
        displaysize=levelintro.size(self.prettyName())
        renderedtext=levelintro.render(self.prettyName(),True,(255,255,255))
        self.screen.blit(renderedtext,(screencenter[0]-displaysize[0]/2,
        screencenter[1]-displaysize[1]/2))
        self.time+=GlobalObjects.clock.get_time()

    def processEvents(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GlobalObjects.renderingThread.renderobj = LevelMenu()
    
    def draw(self, events):
        self.processEvents(events)
        if self.time < 0:
            self.startLevel()
        else:
            GlobalObjects.renderingThread.renderobj=Game(self)
        

    def complete(self):
        if self.stage < 4:
            GlobalObjects.renderingThread.renderobj = Level(self.world,self.stage+1)
        else:
            with GlobalObjects.lock:
                GlobalObjects.unlockedWorlds+=1
            GlobalObjects.renderingThread.renderobj = Level(GlobalObjects.unlockedWorlds,1)

class LevelMenu(Menu):

    def goToWorld1():
        GlobalObjects.renderingThread.renderobj = Level(1,1)

    def goToWorld2():
        GlobalObjects.renderingThread.renderobj = Level(2,1)

    def goToWorld3():
        GlobalObjects.renderingThread.renderobj = Level(3,1)

    def goToWorld4():
        GlobalObjects.renderingThread.renderobj = Level(4,1)

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
        Menu.__init__(self,LevelMenu.levelentries[0:GlobalObjects.unlockedWorlds+1])

    def draw(self,events):
        Menu.draw(self,events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.returnToMain()

Menus.levels=LevelMenu()

