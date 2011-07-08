'''
renderthread.py
Provides the RenderThread class, which is responsible for all redering
'''
import threading,pygame
pygame.init()

class RenderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="RenderThread")
        self.renderobj=None
        self.running=True
        self.clock=pygame.time.Clock()
        pygame.display.set_mode((800,600))
    
    def run(self):
        from globalvalues import *
        while self.running:
            GlobalObjects.lock.acquire()
            GlobalObjects.event = pygame.event.poll()
            GlobalObjects.lock.release()
            Options.lock.acquire()
            framerate=1/self.clock.tick(Options.limitFramerate)*1000
            Options.lock.release()
            if self.renderobj:
                self.renderobj.lock.acquire()
                GlobalObjects.lock.acquire()
                self.renderobj.draw(GlobalObjects.event)
                GlobalObjects.lock.release()
                self.renderobj.lock.release()
            pygame.display.flip()
    
