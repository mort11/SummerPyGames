'''
run_game.py

Implements the game logic, providing the Game class 
'''
import pygame
from globalvalues import Renderable,Options,GlobalObjects,Input,Collison

"""
Takes apart a level object and renders the necessary components for 
playing the game
"""
class Game(Renderable):
    """
    Sets up the object
    """
    def __init__(self,level):
        Renderable.__init__(self)
        self.world=level.world
        self.background=level.background
        self.objectdict=level.objectdict
        self.complete = level.complete
        self.size = level.size
        self.keyinput = 0 
        self.tile_bkd()
        if self.objectdict:
            for i in self.objectdict.iterkeys():
                self.objectdict[i].draw_on(self.screen,i)
        self.player = GlobalObjects.playercharacters[self.world]
        self.player.draw_on(self.screen,level.playerstart)
    
    """
    Tiles the background so that it encompasses the entire level, or just paints
    black if the backgrounds option is false
    """
    def tile_bkd(self):
        levelbkgd = pygame.Surface(self.size)
        if Options.backgrounds:
            import math
            htiles=int(math.ceil(self.size[0]/self.background.get_width()))
            vtiles=int(math.ceil(self.size[1]/self.background.get_height()))
            for htile in range(htiles):
                levelbkgd.blit(self.background,(htile*self.background.get_width(),0))
                for vtile in range(vtiles):
                    levelbkgd.blit(self.background,(0,vtile*self.background.get_height()))
        self.background = levelbkgd
        
    """
    Processes and filters keyboard input.
    The filter assumes that the events will be processed in order, and 
    behaves according to these rules:
    if KEYDOWN : KEYDOWN
    if KEYUP : KEYUP
    if KEYDOWN+KEYUP : KEYDOWN FOR 1 FRAME
    """
    def process_events(self,events):
        keydowns=0
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyinput |= Input.up
                    keydowns |= Input.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput |= Input.down
                    keydowns |= Input.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput |= Input.left
                    keydowns |= Input.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput |= Input.right
                    keydowns |= Input.right
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keyinput &= ~Input.up
                elif event.key == pygame.K_DOWN:
                    self.keyinput &= ~Input.down
                elif event.key == pygame.K_LEFT:
                    self.keyinput &= ~Input.left
                elif event.key == pygame.K_RIGHT:
                    self.keyinput &= ~Input.right
        return self.keyinput | keydowns

    """
    Draws the level, processing input and checking collisions
    """
    def draw(self, events):
        input=self.process_events(events)
        collisions =0
        for i in self.objectdict.iterkeys():
            collisions |= self.player.collides_dir(self.objectdict[i])
        if collisions & Collison.collides == Collison.collides:
            if collisions & Collison.bottom == Collison.bottom:
                if self.player.velocity[1] < 0: self.player.velocity[1] = 0
                if self.player.acceleration[1] < 0: self.player.velocity[1] = 0
            if collisions & Collison.top == Collison.top:
                if self.player.velocity[1] > 0: self.player.velocity[1] = 0
                if self.player.acceleration[1] > 0: self.player.velocity[1] = 0
        #Gotta deal with the 2-keys pressed scenario somehow.
        
        if input & Input.up == Input.up:
            #accelerate the character up? Check inventory?
            pass
        if input & Input.left == Input.left:
            #accelerate left
            pass
        if input & Input.down == Input.down:
            #crouch?
            pass
        if input & Input.right == Input.right:
            #accelerate right
            pass
