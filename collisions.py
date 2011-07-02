'''
collisions.py
Provides the backend for collisions with objects of any number of verticies

Collision should be done(I think) on a per-pixel scale, as pygame doesn't have 
anything readily availible for it.
I'm considering using the alpha channel to determine wether or not to make a 
pixel collide.

In one implementation, #00000000 would be "no collisions", and any pixel 
that isn't #00000000 will have collision done ot it, allowing transparent 
object holes/borders

Alternately, a certain value in the alpha channel could trigger "no collisions",
say 65534 (16-bit color depth), allowing certain areas to collide for animated
groups of objects.

The second implementation seems better, though the first gives more collideable 
colors.

For now, I'll implement the second.
Image masks will be generated per Object and used to do collisions
'''
import pygame,objects
pygame.init()

class collisionDisplay(pygame.display):
    def initCollisions(self):
        self.colliders=set()    
    def addobject(self,object):
        self.colliders.add(object)
