'''
menus.py
Provides the Menu,MenuEntry, MainMenu and OptionsMenu classes
'''
import pygame,threading
pygame.init()
from globalvalues import Options,Renderable,Menus,GlobalObjects
menufont = pygame.font.SysFont("droidsans",20)

"""
Draws a dynamic menu
"""
class Menu(Renderable):
    """
    Constructs the Menu, building the list of entries
    """
    def __init__(self,entries,initialentry=None):
        Renderable.__init__(self)
        self.selectedentry=initialentry
        self.entrylist=list()
        for i in entries:
            if not self.selectedentry:
                self.selectedentry=i
                self.entrylist.append(self.selectedentry)
                continue
            self.entrylist.append(i)
    """
    Selects the entry, highlighting it
    """
    def select_entry(self,entry):
        for i in self.entrylist:
            if i.compare(entry):
                self.selectedentry=i

    """
    Shifts the selected entry down
    """
    def next_entry(self):
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

    """
    Shifts the selected entry up
    """
    def prev_entry(self):
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
    
    """
    Calls the entry's activate method
    """
    def activate_entry(self):
        self.selectedentry.activate()

    """
    Processes key presses
    """
    def process_events(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.next_entry()
                elif event.key == pygame.K_UP:
                    self.prev_entry()
                elif event.key == pygame.K_RETURN:
                    self.activate_entry()

    """
    Draws the menu, highlighting the selected entry
    """
    def draw(self,events):
        self.process_events(events)
        self.screen.fill((0,0,0))
        screencenter=(self.screen.get_width()/2,self.screen.get_height()/2)
        setlength=len(self.entrylist)
        if setlength > 0:
            #dynamic drawing of as many rectangles as needed
            height=64*(setlength/2) + screencenter[1]-16
            if setlength % 2 == 0:
                #even number of entries
                height-=16
            for i in self.entrylist:
                if i == self.selectedentry:
                    pygame.draw.rect(self.screen,(20,255,20),
                    (screencenter[0]-258,height-2,516,36))
                pygame.draw.rect(self.screen,(255,255,255),(screencenter[0]-256,
                height,512,32))
                displaysize=menufont.size(i.get_text())
                renderedfont=menufont.render(i.get_text(),True,(0,0,0))
                self.screen.blit(renderedfont,(screencenter[0]-displaysize[0]/2,
                height+4))
                height-=64


'''
The title is the static text that will shown on the MenuEntry

The method is a method object that will be called with no arguments

The dynamic is a sliceable collection, consisting of (dynamicmethod,iftrue,iffalse)
that will be appended to the static text if present
'''

class MenuEntry:
    
    def __init__(self, title, method,dynamic=(None,None,None)):
        self.text=title
        self.boundmethod=method
        self.dynamicmethod = dynamic[0]
        self.iftrue = dynamic[1]
        self.iffalse = dynamic[2]

    def get_text(self):
        if not self.dynamicmethod:
            return self.text
        if self.dynamicmethod():
            return self.text+str(self.iftrue)
        else:
            return self.text+str(self.iffalse)

    def compare(self,other):
        return self.text == other.text and self.boundmethod==other.boundmethod \
         and self.expression == other.expression and self.iftrue == other.iftrue \
         and self.iffalse == other.iffalse

    def activate(self):
        self.boundmethod()

class OptionsMenu(Menu):
    
    def get_visible_fps():
        return Options.showFramerate
    
    def toggle_show_fps():
        with Options.lock:
            Options.showFramerate = not Options.showFramerate

    def get_fps_limit():
        return Options.limitFramerate
    
    def toggle_limit_framerate():
        with Options.lock:
            if Options.limitFramerate == 60:
                Options.limitFramerate = 0
            else:
                Options.limitFramerate = 60

    def get_backgrounds():
        return Options.backgrounds
    
    def toggle_backgrounds():
        with Options.lock:
            Options.backgrounds= not Options.backgrounds

    def get_menu_wrap():
        return Options.menuWrap
    
    def toggle_menu_wrap():
        with Options.lock:
            Options.menuWrap = not Options.menuWrap

    def return_to_main(self=None):
        with GlobalObjects.lock:
            GlobalObjects.escInUse = False
            GlobalObjects.renderingThread.renderobj = Menus.main


    optionsentries = (
    MenuEntry("Menu Wrapping: ",toggle_menu_wrap,(get_menu_wrap,"On","Off")),
    MenuEntry("Backgrounds: ",toggle_backgrounds,(get_backgrounds,"On","Off")),
    MenuEntry("Limit Framerate: ",toggle_limit_framerate,(get_fps_limit,"On",
    "Off")),
    MenuEntry("Show Framerate: ",toggle_show_fps,(get_visible_fps,"On","Off")),
    MenuEntry("Back",return_to_main)
    )
    
    def __init__(self):
        Menu.__init__(self,OptionsMenu.optionsentries)
    
    def draw(self,events):
        Menu.draw(self,events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_main()

class MainMenu(Menu):
    
    def switch_to_levels():
        GlobalObjects.escInUse = True
        GlobalObjects.renderingThread.renderobj=Menus.levels
    
    def switch_to_options():
        GlobalObjects.escInUse = True
        GlobalObjects.renderingThread.renderobj=Menus.options

    mainentries = (
    MenuEntry("Levels",switch_to_levels),
    MenuEntry("Options",switch_to_options)
    )

    def __init__(self):
        Menu.__init__(self,MainMenu.mainentries)


Menus.main = MainMenu()
Menus.options = OptionsMenu()
