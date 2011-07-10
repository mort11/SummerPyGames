'''
threads.py
Provides the RenderThread class, which is responsible for all rendering, and 
the EventThread class, which sends events to the other threads
'''
import threading,pygame
pygame.init()
from globalvalues import GlobalObjects,Options,Events
frameratefont=pygame.font.SysFont("consolas",16)

class EventThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="EventThread")
        self.killed = threading.Event()
        print self.killed
        with GlobalObjects.lock:
            GlobalObjects.eventsThread=self
    
    def run(self):
        with GlobalObjects.lock,Options.lock:
            GlobalObjects.clock.tick(Options.limitFramerate)
        while not self.killed.isSet():
            if Events.done.acquire(False):
                Events.done.release()
                continue
            with Events.trigger:
                Events.events = pygame.event.get()
                Events.trigger.notifyAll()
            with Options.lock,GlobalObjects.lock:
                GlobalObjects.clock.tick(Options.limitFramerate)

class RenderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="RenderThread")
        self.renderobj=None
        self.killed=threading.Event()
        self.screen=pygame.display.set_mode((800,600))
        with GlobalObjects.lock:
            GlobalObjects.renderingThread=self
    
    def run(self):
        while not self.killed.isSet():
            if self.renderobj:
                with self.renderobj.lock, Events.trigger:
                    self.renderobj.draw(Events.events)
            with Options.lock:
                if Options.showFramerate:
                    with GlobalObjects.lock:
                        framerate=GlobalObjects.clock.get_fps()
                        self.screen.blit(frameratefont.render(str(framerate),False,
                        (255,0,0)),(0,0))
            pygame.display.flip()
            with Events.trigger,Events.done:
                Events.trigger.wait()
    
