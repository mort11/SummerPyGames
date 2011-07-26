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
        self.playerstart = (0,0)
        self.background = pygame.image.load("assets"+os.sep+"backgrounds"
        +os.sep+"world"+str(worldnum)+".png")
        if datafile:
            self.from_file(datafile)
        else:
            self.from_number(worldnum,stagenum)

    def pretty_name(self):
        return 'World '+ str(self.world)+' - Stage '+str(self.stage)
    
    def from_file(self,datafile):
        #stub implementation of level loading
        print "Loading: "+datafile
        self.objectdict=None
    
    def from_number(self,worldnum,stagenum):
        self.from_file("levels"+os.sep+"world"+str(worldnum)
        +os.sep+"stage"+str(stagenum))

    def start(self):
        # draw the level intro
        self.screen.fill((0,0,0))
        levelintro=pygame.font.SysFont('liberationsans',32)
        screencenter=(self.screen.get_width()/2,self.screen.get_height()/2)
        displaysize=levelintro.size(self.pretty_name())
        renderedtext=levelintro.render(self.pretty_name(),True,(255,255,255))
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
            self.start()
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

    def world_1():
        GlobalObjects.renderingThread.renderobj = Level(1,1)

    def world_2():
        GlobalObjects.renderingThread.renderobj = Level(2,1)

    def world_3():
        GlobalObjects.renderingThread.renderobj = Level(3,1)

    def world_4():
        GlobalObjects.renderingThread.renderobj = Level(4,1)

    def return_to_main(self=None):
        GlobalObjects.escInUse = False
        GlobalObjects.renderingThread.renderobj=Menus.main
    
    levelentries=(
    MenuEntry("Back",return_to_main),
    MenuEntry("World 1",world_1),
    MenuEntry("World 2",world_2),
    MenuEntry("World 3",world_3),
    MenuEntry("World 4",world_4)
    )

    def __init__(self):
        Menu.__init__(self,LevelMenu.levelentries[0:GlobalObjects.unlockedWorlds+1])

    def draw(self,events):
        Menu.draw(self,events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_main()

Menus.levels=LevelMenu()

