'''
objects.py
Provides an abstraction layer over pygames Surfaces, and in addition to 
rectangles, provides other polygons with collision 
'''
import pygame,math,os
from globalvalues import GlobalObjects,Collison
pygame.init()

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
        self.mask = pygame.mask.from_surface(self.surface)
        #directions should probably be done opposite the way pygame does them,
        # just for the sake of our sanity
        # so x >0 = right ; y >0 = up
        self.moving=False
        self.rfootfoward=False
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
    
    def collide(self, otherobj):
        if self.collides and otherobj.collides:
            """
            Test if the sprites are colliding and
            resolve the collision in this case.
            """
            offset = [int(x) for x in vsub(otherobj.position,self.position)]
            overlap = self.mask.overlap_area(otherobj.mask,offset)
            if overlap == 0:
                return
            print "collision"
            """Calculate collision normal"""
            normx = (self.mask.overlap_area(otherobj.mask,(offset[0]+1,offset[1])) -
                  self.mask.overlap_area(otherobj.mask,(offset[0]-1,offset[1])))
            normy = (self.mask.overlap_area(otherobj.mask,(offset[0],offset[1]+1)) -
                  self.mask.overlap_area(otherobj.mask,(offset[0],offset[1]-1)))
            if normx == 0 and normy == 0:
                """One sprite is inside another"""
                return
            normv = [normx,normy]
            diffvel = vsub(otherobj.velocity,self.velocity)
            energy = vdot(diffvel,normv)/(2*vdot(normv,normv))
            if energy > 0:
                """Can scale up to 2*J here to get bouncy collisions"""
                energy *= 1.9
                self.velocity=vadd(self.velocity,[normx*energy,normy*energy])
            return
            """Separate the sprites"""
            c1 = -overlap/vdot(n,n)
            c2 = -c1/2
            self.position=vadd(self.position,[c2*normx,c2*normy])


#class Character(Object):
    
Glenda=Object('assets'+os.sep+'characters'+os.sep+'Glenda.png')
Konqi=Object('assets'+os.sep+'characters'+os.sep+'Konqi.png')
Beastie=Object('assets'+os.sep+'characters'+os.sep+'Beastie.png')
Schilli=Object('assets'+os.sep+'characters'+os.sep+'Schilli.png')
GlobalObjects.playercharacters = {1:Glenda,2:Konqi,3:Beastie,4:Schilli}


