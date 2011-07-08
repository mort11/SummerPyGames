'''
renderthread.py
Provides the RenderThread class, which is responsible for all redering
'''
import threading,pygame
pygame.init()
from globalvalues import GlobalObjects,Options
frameratefont=pygame.font.SysFont("consolas",16)
class RenderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="RenderThread")
        self.renderobj=None
        self.running=True
        self.clock=pygame.time.Clock()
        self.screen=pygame.display.set_mode((800,600))
        GlobalObjects.lock.acquire()
        GlobalObjects.renderingThread=self
        GlobalObjects.lock.release()
    
    def run(self):
        while self.running:
            GlobalObjects.bigLock.acquire()
            self.clock.tick(Options.limitFramerate)
            GlobalObjects.bigLock.release()
            framerate=self.clock.get_fps()
            GlobalObjects.lock.acquire()
            GlobalObjects.event = pygame.event.poll()
            GlobalObjects.lock.release()
            Options.lock.acquire()
            print framerate
            Options.lock.release()
            if self.renderobj:
                self.renderobj.lock.acquire()
                GlobalObjects.lock.acquire()
                self.renderobj.draw(GlobalObjects.event)
                GlobalObjects.lock.release()
                self.renderobj.lock.release()
            Options.lock.acquire()
            if Options.showFramerate:
                self.screen.blit(frameratefont.render(str(framerate),False,(255,0,0)),(0,0))
            Options.lock.release()
            pygame.display.flip()
    
