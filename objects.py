'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math
from globalvalues import GlobalObjects
pygame.init()
class Object:
    def __init__(self, texture, ifcollides=True):
        self.surface = pygame.image.load(texture)
        # using a mask texture lets artists use more of their alpha channels
        self.collides=ifcollides
        self.pivot=pivotpixel
        self.velocity=(0,0)
    
    def getVectorAngle(self):
        return math.degrees(math.atan2(self.velocity[0],self.velocity[1]))
    
    def drawOn(self,surface,at=(0,0)):
        surface.blit(self.surface,at)
    
    def collidesWith(self,otherobject):
        if self.collides:
            from pygame import mask
            mask.from_threshold(self.surface,(0,0,0,0),(1,1,1,1))

Glenda=Object('assets'+os.sep+'characters'+os.sep+'Glenda.png')
Konqi=Object('assets'+os.sep+'characters'+os.sep+'Konqi.png')
Beastie=Object('assets'+os.sep+'characters'+os.sep+'Beastie.png')
Schilli=Object('assets'+os.sep+'characters'+os.sep+'Schilli.png')
GlobalObjects.playercharacters = {Glenda:1,Konqi:2,Beastie:3,Schilli:4}


