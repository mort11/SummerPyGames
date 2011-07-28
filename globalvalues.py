'''
globalvalues.py
Stores values and locks that can be accessed from almost anywhere
Acquiring the lock of a class is recommended before writing to its attributes
'''
import threading,pygame
pygame.init()

class Renderable:
    def __init__(self):
        self.lock=threading.RLock()
        self.screen = pygame.display.get_surface()
        if not self.screen:
            self.screen = pygame.display.set_mode((800,600))
    
    def draw(self,events):
        print "Please implement a draw method"

class Options:
    lock=threading.RLock()
    menuWrap=False
    backgrounds=True
    limitFramerate=60
    showFramerate=False
    writeLog=False
    theme=None
    musicVolume=1
    sfxVolume=1

class Events:
    done = threading.Semaphore(2)
    events = pygame.event.get()
    trigger = threading.Condition()
    processing = threading.Semaphore(2)
    
class GlobalObjects:
    playercharacters = None
    unlockedWorlds=1
    lock = threading.RLock()
    clock = pygame.time.Clock()
    renderingThread = None
    eventsThread = None
    escInUse = False

class Menus:
    main = None
    options = None
    levels = None

class Input:
    left = 1
    right = 2
    up = 4
    down = 8

class Collison:
    #set this bit to 0 if no collision
    collides=1
    top=2
    bottom=4
    right=8
    left=16

