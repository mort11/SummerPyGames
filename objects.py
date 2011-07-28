'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math,os
from globalvalues import GlobalObjects,Collison
pygame.init()

    
class Object:
    def __init__(self, texture, ifcollides=True):
        self.surface = pygame.image.load(texture)
        # using a mask texture lets artists use more of their alpha channels
        self.collides=ifcollides
        #directions should probably be done opposite the way pygame does them,
        # just for the sake of our sanity
        # so x >0 = right ; y >0 = up
        self.acceleration=(0,0)
        self.velocity=(0,0)
        self.lastdraw=pygame.time.get_ticks()
    
    def angle(self):
        return math.degrees(math.atan2(self.velocity[0],self.velocity[1]))
    
    def draw_on(self,surface,at=(0,0)):
        self.lastdraw=pygame.time.get_ticks()
        surface.blit(self.surface,at)
    
    def collides_with(self,otherobject):
        if self.collides:
            from pygame import mask
            selfmask=mask.from_threshold(self.surface,(0,0,0,0),(1,1,1,1))
            othermask=mask.from_threshold(otherobject.surface,(0,0,0,0),(1,1,1,1))
            return selfmask.overlap(othermask)
        return False

    def collides_dir(self,otherobject):
        output=0
        collision=self.collides_with(otherobject)
        if collision:
            center=pygame.mask.from_threshold(self.surface,(0,0,0,0),(1,1,1,1)).centroid()
            output |= Collison.collides
            if center[0]+0.25*self.surface.get_width() <=collision[0]:
                output |= Collison.right
            elif center[0]-0.25*self.surface.get_width() >=collision[0]:
                output |= Collison.left
            if center[1]+0.25*self.surface.get_height()<= collision[1]:
                output |= Collison.bottom
            elif center[1]+0.25*self.surface.get_height()<= collision[1]:
                output |= Collison.top
        return output


Glenda=Object('assets'+os.sep+'characters'+os.sep+'Glenda.png')
Konqi=Object('assets'+os.sep+'characters'+os.sep+'Konqi.png')
Beastie=Object('assets'+os.sep+'characters'+os.sep+'Beastie.png')
Schilli=Object('assets'+os.sep+'characters'+os.sep+'Schilli.png')
GlobalObjects.playercharacters = {1:Glenda,2:Konqi,3:Beastie,4:Schilli}


