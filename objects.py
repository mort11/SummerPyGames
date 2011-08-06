'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math,os
from globalvalues import GlobalObjects,Collison
pygame.init()

def maskFromSurface(surface, threshold = 127):

    mask = pygame.mask.Mask(surface.get_size())
    key = surface.get_colorkey()
    if key:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x+0.1,y+0.1)) != key:
                    mask.set_at((x,y),1)
    else:
        for y in range(surface.get_height()):
            for x in range (surface.get_width()):
                if surface.get_at((x,y))[3] > threshold:
                    mask.set_at((x,y),1)
    return mask

def vadd(x,y):
    return [x[0]+y[0],x[1]+y[1]]

def vsub(x,y):
    return [x[0]-y[0],x[1]-y[1]]

def vdot(x,y):
    return x[0]*y[0]+x[1]*y[1]
    
class Object:
    def __init__(self, texture, ifcollides=True):
        self.surface = pygame.image.load(texture)
        # using a mask texture lets artists use more of their alpha channels
        self.collides=ifcollides
        self.rect=self.surface.get_rect()
        self.size = [self.surface.get_width(),self.surface.get_height()]
        #directions should probably be done opposite the way pygame does them,
        # just for the sake of our sanity
        # so x >0 = right ; y >0 = up
        self.acceleration=[0,0]
        self.velocity=[0,0]
        self.position = [0, 0]
        self.lastdraw=pygame.time.get_ticks()
    
    def angle(self):
        return math.degrees(math.atan2(self.velocity[0],self.velocity[1]))
    
    def draw_on(self,surface,at=(0, 0)):
        self.lastdraw=pygame.time.get_ticks()
        surface.blit(self.surface,at)
        self.position = at
        self.rect.move_ip(self.position)
    
    def collide(self, otherobj):
        if self.collides and otherobj.collides:
            if self.rect.colliderect(otherobj.rect):
                pass


class Character(Object):
    def __init__(self,texture):
        Object.__init__(self,texture+".png")
        self.leftfootfoward=True
        self.leftstep=pygame.image.load(texture+"left.png")
        self.invertedleft=pygame.image.load(texture+"lefti.png")
        self.rightstep=pygame.image.load(texture+"right.png")
        self.invertedright=pygame.image.load(texture+"righti.png")
        self.is_jumping=False
        self.jump=pygame.image.load(texture+"jump.png")
        self.invertedjump=pygame.image.load(texture+"jumpi.png")

    def draw_on(self,surface,at=[0,0]):
        self.lastdraw=pygame.time.get_ticks()
        self.rect.move_ip(vsub(at,self.position))
        self.position=at
        if self.velocity[0]==0:
            Object.draw_on(self,surface,at)
            return
        else:
            self.leftfootfoward = not self.leftfootfoward
            if self.velocity[0]==1:
                if self.is_jumping:
                    surface.blit(self.jump,at)
                elif self.leftfootfoward:
                    surface.blit(self.leftstep,at)
                else:
                    surface.blit(self.rightstep,at)
            else:
                if self.is_jumping:
                    surface.blit(self.invertedjump,at)
                elif self.leftfootfoward:
                    surface.blit(self.invertedleft,at)
                else:
                    surface.blit(self.invertedright,at)

    
    
    
Glenda=Character('assets'+os.sep+'characters'+os.sep+'Glenda')
Konqi=Character('assets'+os.sep+'characters'+os.sep+'Konqui')
Beastie=Character('assets'+os.sep+'characters'+os.sep+'Beastie')
GlobalObjects.playercharacters = {1:Glenda,2:Konqi,3:Beastie}


