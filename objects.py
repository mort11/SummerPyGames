'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math
pygame.init()
defaultcolor=(0,0,0,0)
defaultthreshold=(1,1,1,1)
def autogenmask(texture,color=defaultcolor,threshold=defaultthreshold):    
    texturesurface=pygame.image.load(texture)
    return pygame.mask.from_threshold(texturesurface,color,threshold)

class Object:
    def __init__(self, texture,masktexture=None,pivotpixel=None, ifcollides=True):
        self.surface = pygame.image.load(texture)
        # using a mask texture lets artists use more of their alpha channels
        if masktexture:
            self.mask=autogenmask(masktexture)
        else:
            self.mask=autogenmask(texture)
        self.collides=ifcollides
        self.pivot=pivotpixel
        self.velocity=(0,0)
    
    def getVectorAngle(self):
        return math.degrees(math.atan2(self.velocity[0],self.velocity[1]))
    
    def drawOn(self,surface,at=(0,0)):
        surface.blit(self.surface,at)

class Block(Object):
    def __init__(self):
        Object.__init__(self,"assets"+os.sep+"block.png",(16,16))
