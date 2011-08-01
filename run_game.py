'''
run_game.py

Implements the game logic, providing the Game class 
'''
import pygame
from globalvalues import Renderable,Options,GlobalObjects,Input,Collison
from levelparser import LevelFile

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
        self.bkd_pos = 0
        self.objectdict=level.objectdict
        self.complete = level.complete
        self.size = level.size
        self.keyinput = 0 
        self.tile_bkd()
        if self.objectdict:
            for i in self.objectdict.iterkeys():
                self.objectdict[i].draw_on(self.background,i)
        self.player = GlobalObjects.playercharacters[self.world]
        self.player.draw_on(self.screen,level.playerstart)
        
        self.is_jumping = False
    
    """
    Tiles the background so that it encompasses the entire level, or just paints
    black if the backgrounds option is false 
    """
    def tile_bkd(self):
        levelbkgd = self.screen
        levelbkgd.blit(self.background, (self.bkd_pos, 0))
        
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
                #print "collide"
                is_jumping = False
                if self.player.velocity[1] < 0: self.player.velocity[1] = 0
                if self.player.acceleration[1] < 0: self.player.velocity[1] = 0
            if collisions & Collison.top == Collison.top:
                if self.player.velocity[1] > 0: self.player.velocity[1] = 0
                if self.player.acceleration[1] > 0: self.player.velocity[1] = 0
        #Gotta deal with the 2-keys pressed scenario somehow.
        
        self.tile_bkd()
        if self.player.position[0] < self.size[0]/2 or self.player.velocity[0] < 0:
            self.player.draw_on(self.screen, (self.player.position[0] + (self.player.acceleration[0]*self.player.velocity[0]), 
                                                self.player.position[1] + (self.player.acceleration[1]*self.player.velocity[1])))
        else:
            #scrolls background if player is moving past the midpoint on the screen
            self.player.draw_on(self.screen, (self.player.position[0], self.player.position[1] + (self.player.acceleration[1]*self.player.velocity[1])))
            self.bkd_pos = self.bkd_pos - (self.player.acceleration[0]*self.player.velocity[0])
        
        if self.is_jumping:
            time = pygame.time.get_ticks() - self.start_jump
            if time < 500:
                self.player.draw_on(self.screen, (self.player.position[0], self.start_jump_pos - ((-10*(2*(time/500.0) - 1)*(2*(time/500.0) - 1) + 10)*20)))
            else:
                self.player.draw_on(self.screen, (self.player.position[0], self.start_jump_pos))
                self.is_jumping = False
        
        if input & Input.up == Input.up:
            if not self.is_jumping:
                self.is_jumping = True
                self.start_jump = pygame.time.get_ticks()
                self.start_jump_pos = self.player.position[1]
            pass
        if input & Input.left == Input.left:
            self.player.velocity[0] = -1
            self.player.acceleration[0] = 10
            pass
        if input & Input.down == Input.down:
            #crouch?
            pass
        if input & Input.right == Input.right:
            self.player.velocity[0] = 1
            self.player.acceleration[0] = 10
            pass
        if input & Input.left != Input.left and input & Input.right != Input.right:
            self.player.velocity[0] = 0
