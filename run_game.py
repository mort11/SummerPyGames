'''
run_game.py

Implements the game logic, providing the Game class 
'''
import pygame
from globalvalues import Renderable,Options,GlobalObjects,InputMasks
class Game(Renderable):

    def __init__(self,level):
        Renderable.__init__(self)
        self.world=level.world
        self.background=level.background
        self.objectdict=level.objectdict
        self.complete = level.complete
        self.size = level.size
        self.keyinput = 0 
        self.tile_bkd()
        self.select_player()
        if self.objectdict:
            for i in self.objectdict.iterkeys():
                self.objectdict[i].draw_on(self.screen,i)
        self.player.draw_on(self.screen,level.playerstart)

    def select_player(self):
        self.player = GlobalObjects.playercharacters[self.world]

    def tile_bkd(self):
        levelbkgd = pygame.Surface(self.size)
        if Options.backgrounds:
            from math import ciel
            htiles=ciel(self.size[0]/self.background.get_width())
            vtiles=ciel(self.size[1]/self.background.get_height())
            for htile in range(htiles):
                levelbkgd.blit(self.background,(htile*self.background.get_width(),0))
                for vtile in range(vtiles):
                    levelbkgd.blit(self.background,(0,vtile*self.background.get_height()))
        self.background = levelbkgd

    def process_events(self,events):
        keydowns=0
        #if KEYDOWN : KEYDOWN
        #if KEYUP : KEYUP
        #if KEYUP+KEYDOWN : KEYDOWN FOR 1 FRAME
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyinput |= InputMasks.up
                    keydowns |= InputMasks.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput |= InputMasks.down
                    keydowns |= InputMasks.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput |= InputMasks.left
                    keydowns |= InputMasks.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput |= InputMasks.right
                    keydowns |= InputMasks.right
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keyinput &= ~InputMasks.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput &= ~InputMasks.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput &= ~InputMasks.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput &= ~InputMasks.right
        # filtered input
        return self.keyinput | keydowns



    def draw(self, events):
        input=self.process_events(events)
        
        #Gotta deal with the 2-keys pressed scenario
        if input & InputMasks.up == InputMasks.up:
            #accelerate the character up? Check inventory?
            pass
        if input & InputMasks.left == InputMasks.left:
            #accelerate left
            pass
        if input & InputMasks.down == InputMasks.down:
            #crouch?
            pass
        if input & InputMasks.right == InputMasks.right:
            #accelerate right
            pass
