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
    lock=threading.RLock()
    event=pygame.event.poll()
    renderingThread=None
    escInUse=False
