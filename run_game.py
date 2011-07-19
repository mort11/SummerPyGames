'''
run_game.py

Implements the game logic, providing the Game class 
'''

from globalvalues import Renderable,Options,GlobalObjects
class Game(Renderable):
    def __init__(self,level):
        Renderable.__init__(self)
        self.world=level.world
        self.background=level.background
        self.objectdict=level.objectdict
        self.complete = level.complete
        self.size = level.size
        self.tile_bkd()
        if self.objectdict:
            for i in self.objectdict.iterkeys():
                self.objectdict[i].drawOn(self.screen,i)

    def select_player(self):
        self.player = GlobalObjects.playercharacters[self.world]

    def tile_bkd(self):
        levelbkgd = pygame.Surface(self.size)
        if Options.backgrounds:
            from math import ciel
            htiles=ciel(self.size[0]/self.background.get_width())
            vtiles=ciel(self.size[1]/self.background.get_height())
            for htile in range(htiles):
                levelbkgd.blit(self.background,(htile*self.background.get_width(),0)
                for vtile in range(vtiles):
                    levelbkgd.blit(self.background,(0,vtile*self.background.get_height())
        self.background = levelbkgd
    
    def draw(self, events):
        
