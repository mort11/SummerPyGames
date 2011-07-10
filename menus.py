'''
menus.py
Provides the Menu,MenuEntry, MainMenu and OptionsMenu classes
'''
import pygame,threading
pygame.init()
from globalvalues import Options,Renderable
menufont = pygame.font.SysFont("droidsans",20)

class Menu(Renderable):
    
    def __init__(self,entries,initialentry=None):
        Renderable.__init__(self)
        self.selectedentry=initialentry
        self.entrylist=list()
        for i in entries:
            if not self.selectedentry:
                self.selectedentry=i
                self.addEntry(self.selectedentry)
                continue
            self.addEntry(i)

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
        Options.lock.acquire()
        if not Options.menuWrap and iterator == 0:
            Options.lock.release()
            return
        Options.lock.release()
        self.selectedentry=self.entrylist[iterator-1]

    def prevEntry(self):
        iterator=-1
        for i in self.entrylist:
            iterator+=1
            if i == self.selectedentry:
                break
        Options.lock.acquire()
        if not Options.menuWrap and iterator == len(self.entrylist)-1:
            Options.lock.release()
            return
        Options.lock.release()
        try:
            self.selectedentry=self.entrylist[iterator+1]
        except IndexError:
            self.selectedentry=self.entrylist[0]
    
    def activateEntry(self):
        self.selectedentry.activate()

    def update(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.nextEntry()
                elif event.key == pygame.K_UP:
                    self.prevEntry()
                elif event.key == pygame.K_RETURN:
                    self.activateEntry()

    def draw(self,events):
        self.update(events)
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
                text=i.getText()
                displaysize=menufont.size(text)
                renderedfont=menufont.render(text,True,(0,0,0))
                screen.blit(renderedfont,(screencenter[0]-displaysize[0]/2,
                height+4))
                height-=64


'''
The title is the static text that will shown on the MenuEntry

The method is a method object that will be called with no arguments

The dynamic is a sliceable collection, consisting of (dynamicmethod,iftrue,iffalse)
that will be appended to the static text if present
'''

class MenuEntry:
    def __init__(self, title, method,dynamic=(None,None,None),lock=None):
        self.text=title
        self.boundmethod=method
        self.dynamicmethod = dynamic[0]
        self.iftrue = dynamic[1]
        self.iffalse = dynamic[2]
        if lock:
            self.lock = threading.Lock()
        else:
            self.lock=lock

    def getText(self):
        with self.lock:
            if self.dynamicmethod():
                return self.text+str(self.iftrue)
            else:
                return self.text+str(self.iffalse)

    def compare(self,other):
        return self.text == other.text and self.boundmethod==other.boundmethod \
         and self.expression == other.expression and self.iftrue == other.iftrue \
         and self.iffalse == other.iffalse

    def activate(self):
        with self.lock:
            self.boundmethod()

class OptionsMenu(Menu):
    
    def getVisibleFPS():
        Options.lock.acquire()
        fps=Options.showFramerate
        Options.lock.release()
        return fps
    
    def toggleShowFPS():
        Options.lock.acquire()
        if Options.showFramerate:
            Options.showFramerate=False
        else:
            Options.showFramerate=True
        Options.lock.release()

    def getFramerateLimit():
        Options.lock.acquire()
        limit=Options.limitFramerate
        Options.lock.release()
        return limit
    
    def toggleLimitFramerate():
        Options.lock.acquire()
        if Options.limitFramerate == 60:
            Options.limitFramerate = 0
        else:
            Options.limitFramerate = 60
        Options.lock.release()

    def getBackgrounds():
        Options.lock.acquire()
        backgrounds=Options.backgrounds
        Options.lock.release()
        return backgrounds
    
    def toggleBackgrounds():
        Options.lock.acquire()
        if Options.backgrounds:
            Options.backgrounds=False
        else:
            Options.backgrounds=True
        Options.lock.release()

    def getMenuWrap():
        Options.lock.acquire()
        wrap=Options.menuWrap
        Options.lock.release()
        return wrap
    
    def toggleMenuWrap():
        Options.lock.acquire()
        if Options.menuWrap:
            Options.menuWrap=False
        else:
            Options.menuWrap=True
        Options.lock.release()

    optionsentries = (
    MenuEntry("Menu Wrapping: ",toggleMenuWrap,(getMenuWrap,"On","Off"),
    Options.lock),
    MenuEntry("Backgrounds: ",toggleBackgrounds,(getBackgrounds,"On","Off"),
    Options.lock),
    MenuEntry("Limit Framerate: ",toggleLimitFramerate,(getFramerateLimit,"On",
    "Off"),Options.lock),
    MenuEntry("Show Framerate: ",toggleShowFPS,(getVisibleFPS,"On","Off"),
    Options.lock)
    )
    
    def __init__(self):
        Menu.__init__(self,OptionsMenu.optionsentries)

