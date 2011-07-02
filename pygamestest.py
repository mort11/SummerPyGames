#!/usr/bin/env python2
import pygame, sys
from datetime import datetime
pygame.init()

size = width,height = 640,640
speed = [10,10]
BACKGROUND = 0,255,0
screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets/mortHead.png")
ballcollide = ball.get_rect()

loopstart=0
''''''
ballcollide = ballcollide.move(speed)
if ballcollide.left < 0 or ballcollide.right > width:
    speed[0] = -speed[0]
if ballcollide.top < 0 or ballcollide.bottom > height:
    speed[1]= -speed[1]

while True:
    loopstart=datetime.now()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    screen.fill(BACKGROUND)
    screen.blit(ball, ballcollide)
    pygame.display.flip()
    print (datetime.now() - loopstart)
    
