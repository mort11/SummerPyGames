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

"""
Provides the logic for loading levels, and draws their splash screen before 
giving control to the Game object
"""
class Level(Renderable):
    """
    Sets up the level and loads the objects from the disk
    """
    def __init__(self,worldnum,stagenum,datafile=None):
        Renderable.__init__(self)
        self.world=worldnum
        self.stage=stagenum
        self.time=-2000
        self.size = self.screen.get_size()
        self.playerstart = (0,500)
        self.background = pygame.image.load("assets"+os.sep+"world"
        +os.sep+str(worldnum)+os.sep+"background.jpg")
        if datafile:
            self.from_file(datafile)
        else:
            self.from_number(worldnum,stagenum)
    
    """
    Returns a beautifully formatted string for easy user Level identification
    The string is of the form "World X - Stage Y"
    """
    def pretty_name(self):
        return 'World '+ str(self.world) + ' - Stage '+str(self.stage)
    
    """
    Loads the level off the disk, parsing it as described in levelformat
    """
    def from_file(self,datafile):
        #stub implementation of level loading
        print "Loading: "+datafile
        
        self.objectdict=dict()
        
        levelfile = open(datafile, "r")
        levellines = levelfile.read().split("\n")
        if levellines[0] == "ALGEBRAADVENTURELEVELFILE":
            self.level_dimensions = levellines[1].split(" ")
            self.start_position = levellines[2].split(" ")
            i = 3
            while levellines[i] != "ENDOBJECTS":
                object_params = levellines[i].split(" ")
                self.objectdict.setdefault((int(object_params[1]), int(object_params[2])), Object(object_params[0]))
                i += 1
        else:
            print "Invalid level file"
    
    """
    Loads the level based on world and stage number
    """
    def from_number(self,worldnum,stagenum):
        self.from_file("levels"+os.sep+"world"+str(worldnum)
        +os.sep+"stage"+str(stagenum))
    
    """
    Draws the level splash
    """
    def start(self):
        self.screen.fill((0,0,0))
        levelintro=pygame.font.SysFont('liberationsans',32)
        screencenter=(self.screen.get_width()/2,self.screen.get_height()/2)
        displaysize=levelintro.size(self.pretty_name())
        renderedtext=levelintro.render(self.pretty_name(),True,(255,255,255))
        self.screen.blit(renderedtext,(screencenter[0]-displaysize[0]/2,
        screencenter[1]-displaysize[1]/2))
        self.time+=GlobalObjects.clock.get_time()
    
    """
    Checks to see if the level should abort during the splash
    """
    def processEvents(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GlobalObjects.renderingThread.renderobj = LevelMenu()
    
    """
    Draws the splash screen before passing control to Game
    """
    def draw(self, events):
        self.processEvents(events)
        if self.time < 0:
            self.start()
        else:
            GlobalObjects.renderingThread.renderobj=Game(self)

    """
    Completes the level, and begins loading the next one
    """
    def complete(self):
        if self.stage < 4:
            GlobalObjects.renderingThread.renderobj = Level(self.world,self.stage+1)
        else:
            with GlobalObjects.lock:
                GlobalObjects.unlockedWorlds+=1
            GlobalObjects.renderingThread.renderobj = Level(GlobalObjects.unlockedWorlds,1)

"""
Provides the menu from which the game is played
"""
class LevelMenu(Menu):

    """
    Sends the player to World 1
    """
    def world_1():
        GlobalObjects.renderingThread.renderobj = Level(1,1)

    """
    Sends the player to World 2
    """
    def world_2():
        GlobalObjects.renderingThread.renderobj = Level(2,1)

    """
    Sends the player to World 3
    """
    def world_3():
        GlobalObjects.renderingThread.renderobj = Level(3,1)

    """
    Sends the player to World 4
    """
    def world_4():
        GlobalObjects.renderingThread.renderobj = Level(4,1)
    """
    Returns to the Main menu
    """
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
    """
    Determines how many worlds are unlocked and only loads MenuEntries for those 
    that are
    """
    def __init__(self):
        Menu.__init__(self,LevelMenu.levelentries[0:GlobalObjects.unlockedWorlds+1])
    
    """
    Checks to see if returning to Main
    """
    def draw(self,events):
        Menu.draw(self,events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_main()
"""
Run on first import, builds LevelMenu object where it's needed
"""
Menus.levels=LevelMenu()

