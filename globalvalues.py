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
    
class GlobalObjects:
    lock = threading.RLock()
    clock = pygame.time.Clock()
    renderingThread = None
    eventsThread = None
    escInUse = False

class Menus:
    main = None
    options = None
