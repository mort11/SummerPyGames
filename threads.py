'''
threads.py
Provides the RenderThread class, which is responsible for all rendering, and 
the EventThread class, which sends events to the other threads
'''
import threading,pygame
pygame.init()
from globalvalues import GlobalObjects,Options,Events, Menus
frameratefont=pygame.font.SysFont("consolas",16)

class EventThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="EventThread")
        self.killed = threading.Event()
        with GlobalObjects.lock:
            GlobalObjects.eventsThread=self
    
    def run(self):
        GlobalObjects.clock.tick(Options.limitFramerate)
        while not self.killed.isSet():
            if Events.done.acquire(False):
                Events.done.release()
                continue
            with Events.trigger:
                Events.events = pygame.event.get()
                Events.trigger.notifyAll()
            GlobalObjects.clock.tick(Options.limitFramerate)



class RenderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="RenderThread")
        self.renderobj=Menus.main
        self.killed=threading.Event()
        self.screen=pygame.display.get_surface()
        with GlobalObjects.lock:
            GlobalObjects.renderingThread=self
    
    def run(self):
        if self.renderobj:
            with self.renderobj.lock:
                self.renderobj.draw(Events.events)
        if Options.showFramerate:
            framerate = GlobalObjects.clock.get_fps()
            self.screen.blit(frameratefont.render(str(framerate),False,
            (255,0,0)),(0,0))
        pygame.display.flip()
        while not self.killed.isSet():
            with Events.done, Events.trigger:
                Events.trigger.wait()
            if self.renderobj:
                with self.renderobj.lock:
                    self.renderobj.draw(Events.events)
            if Options.showFramerate:
                framerate = GlobalObjects.clock.get_fps()
                self.screen.blit(frameratefont.render(str(framerate),False,
                (255,0,0)),(0,0))
            pygame.display.flip()



#class IOThread(threading.Thread):
    
    
