'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math,os
from globalvalues import GlobalObjects
pygame.init()
class Collison:
    #set this bit to 0 if no collision
    collides=1
    top=2
    bottom=4
    right=8
    left=16
    
class Object:
    def __init__(self, texture, ifcollides=True):
        self.surface = pygame.image.load(texture)
        # using a mask texture lets artists use more of their alpha channels
        self.collides=ifcollides
        self.pivot=pivotpixel
        self.velocity=(0,0)
    
    def angle(self):
        return math.degrees(math.atan2(self.velocity[0],self.velocity[1]))
    
    def draw_on(self,surface,at=(0,0)):
        surface.blit(self.surface,at)
    
    def collides_with(self,otherobject):
        if self.collides:
            from pygame import mask
            selfmask=mask.from_threshold(self.surface,(0,0,0,0),(1,1,1,1))
            othermask=mask.from_threshold(otherobject.surface,(0,0,0,0),(1,1,1,1))
            return selfmask.collides(othermask)
        return False

    def collides_dir(self,otherobject):
        output=0
        collision=self.collides_with(otherobject)
        if collision:
            center=self.mask.from_threshold(self.surface,(0,0,0,0),(1,1,1,1)).centroid()
            output |= Collison.collides
            if center[0] <=collision[0]:
                output |= Collison.right
            else:
                output |= Collison.left
            if center[1] <= collision[1]:
                output |= = Collison.bottom
            else:
                output |= Collison.top
        return output


Glenda=Object('assets'+os.sep+'characters'+os.sep+'Glenda.png')
Konqi=Object('assets'+os.sep+'characters'+os.sep+'Konqi.png')
Beastie=Object('assets'+os.sep+'characters'+os.sep+'Beastie.png')
Schilli=Object('assets'+os.sep+'characters'+os.sep+'Schilli.png')
GlobalObjects.playercharacters = {Glenda:1,Konqi:2,Beastie:3,Schilli:4}


