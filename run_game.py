'''
run_game.py

Implements the game logic, providing the Game class 
'''

from globalvalues import Renderable,Options,GlobalObjects,InputMasks
class Game(Renderable):

    def __init__(self,level):
        Renderable.__init__(self)
        self.world=level.world
        self.background=level.background
        self.objectdict=level.objectdict
        self.complete = level.complete
        self.size = level.size
        self.keyinput=0
        self.keystocheck=15
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

    def process_events(self,events):
        #if KEYDOWN : KEYDOWN
        #if KEYUP : KEYUP
        #if KEYUP+KEYDOWN : KEYDOWN + CHECK NEXT FRAME
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyinput |= InputMasks.up
                    self.keystocheck ^= InputMasks.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput |= InputMasks.down
                    self.keystocheck ^= InputMasks.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput |= InputMasks.left
                    self.keystocheck ^= InputMasks.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput |= InputMasks.right
                    self.keystocheck ^= InputMasks.right
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyinput &= ~InputMasks.up
                    self.keystocheck ^= InputMasks.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput &= ~InputMasks.down
                    self.keystocheck ^= InputMasks.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput &= ~InputMasks.left
                    self.keystocheck ^= InputMasks.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput &= ~InputMasks.right
                    self.keystocheck ^= InputMasks.right
        self.inputmasks ^= self.keystocheck
    def draw(self, events):
        
