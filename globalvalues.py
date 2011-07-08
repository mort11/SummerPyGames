'''
globalvalues.py
'''
import threading,pygame
pygame.init()
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

class GlobalObjects:
    bigLock=threading.RLock()
    lock=threading.RLock()
    event=pygame.event.poll()
    renderingThread=None
    escInUse=False

class Renderable:
    def __init__(self):
        self.lock=threading.RLock()
    
    def draw(self,event):
        print "Please implement a draw method"
