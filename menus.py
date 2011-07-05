'''
menus.py
Provides the Menu,MenuEntry, MainMenu and OptionsMenu classes
'''
import pygame
pygame.init()
screen=pygame.display.get_surface()
menufont = pygame.font.SysFont("droidsans",20)
# entries is a dict, with the string that will be the button text 
# used as the key for the bound method object
class Menu:
    
    def __init__(self,entries,initialentry=None):
        self.selectedentry=initialentry
        self.entrylist=list()
        for i in entries.iterkeys():
            self.addEntry(self.unpackEntry(i,entries))

    def selectEntry(self,entry):
        for i in self.entrylist:
            if i.compare(entry):
                self.selectedentry=i

    def unpackEntry(self,key,entries):
        return MenuEntry(key,entries.get(key))

    def addEntry(self, entry):
        self.entrylist.append(entry)

    def nextEntry(self):
        iterator=-1
        for i in self.entrylist:
            iterator+=1
            if i == self.selectedentry:
                break
        self.selectedentry=self.entrylist[iterator-1]

    def prevEntry(self):
        iterator=-1
        for i in self.entrylist:
            iterator+=1
            if i == self.selectedentry:
                break
        try:
            self.selectedentry=self.entrylist[iterator+1]
        except IndexError:
            self.selectedentry=self.entrylist[0]
    
    def activateEntry(self):
        self.selectedentry.activate()

    def draw(self):
        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        screencenter=(screen.get_width()/2,screen.get_height()/2)
        setlength=len(self.entrylist)
        if setlength > 0:
            #dynamic drawing of as many rectangles as needed
            height=64*(setlength/2) + screencenter[1]-16
            if setlength % 2 == 0:
                #even number of entries
                height-=16
            for i in self.entrylist:
                if i == self.selectedentry:
                    pygame.draw.rect(screen,(20,255,20),
                    (screencenter[0]-258,height-2,516,36))
                pygame.draw.rect(screen,(255,255,255),(screencenter[0]-256,
                height,512,32))
                displaysize=menufont.size(i.text)
                renderedfont=menufont.render(i.text,True,(0,0,0))
                screen.blit(renderedfont,(screencenter[0]-displaysize[0]/2,
                height+4))
                height-=64

class MenuEntry:
    def __init__(self, title, method):
        self.text=title
        self.boundmethod=method
    def compare(self,other):
        return self.text == other.text and self.boundmethod==other.boundmethod
    def activate(self):
        self.boundmethod()
