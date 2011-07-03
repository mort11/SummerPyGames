'''
menus.py
Provides the Menu,MenuEntry, MainMenu and OptionsMenu classes
'''
import pygame
pygame.init()
screen=pygame.display.get_surface()
# entries is a dict, with the string that will be the button text 
# used as the key for the bound method object
class Menu:
    def __init__(self,entries,initialentry=None):
        self.entryset=set()
        for i in entries.iterkeys():
            print i
            self.addEntry(self.unpackEntry(i,entries))
    def unpackEntry(self,key,entries):
        return MenuEntry(key,entries.get(key))
    def addEntry(self, entry):
        self.entryset.add(entry)
    def draw(self):
        
        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        screencenter=(screen.get_width()/2,screen.get_height()/2)
        setlength=len(self.entryset)
        if setlength > 0:
            #dynamic drawing of as many rectangles as needed
            if setlength % 2 == 0:
                #even number of entries
                height=64*(setlength/2) + screencenter[1]-32
                for i in self.entryset:
                    pygame.draw.rect(screen,(255,255,255),(screencenter[0]-256,
                    height,512,32))
                    height-=64
            else:
                #odd number of entries
                height=64*(setlength/2) + screencenter[1]-16
                for i in self.entryset:
                    pygame.draw.rect(screen,(255,255,255),(screencenter[0]-256,
                    height,512,32))
                    height-=64
                

class MenuEntry:
    def __init__(self, title, method):
        self.text=title
        self.boundmethod=method
        print self
    def activate(self):
        self.boundmethod()
