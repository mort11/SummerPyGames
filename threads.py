'''
threads.py
Provides the RenderThread class, which is responsible for all rendering, and 
the EventThread class, which sends events to the other threads
'''
import threading,pygame
pygame.init()
from globalvalues import GlobalObjects,Options,Events, Menus
frameratefont=pygame.font.SysFont("consolas",16)
"""
Provides Events to threads that need them and limits the framerate
"""
class EventThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="EventThread")
        self.killed = threading.Event()
        with GlobalObjects.lock:
            GlobalObjects.eventsThread=self
    """
    Updates the events and sleeps until killed
    """
    def run(self):
        GlobalObjects.clock.tick(Options.limitFramerate)
        while not self.killed.isSet():
            """
            Prevents the thread from updating events until both the other
            threads are ready. Live? Yes. Working? Yes
            """
            if Events.done.acquire(False):
                Events.done.release()
                continue
            with Events.trigger:
                Events.events = pygame.event.get()
                Events.trigger.notifyAll()
            if Options.limitFramerate: 
                GlobalObjects.clock.tick(Options.limitFramerate)
            else:
                GlobalObjects.clock.tick(1000)

"""
Renders the game, or whatever Renderable object it is told to, sending events to
that object.
"""
class RenderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="RenderThread")
        self.renderobj=Menus.main
        self.killed=threading.Event()
        self.screen=pygame.display.get_surface()
        with GlobalObjects.lock:
            GlobalObjects.renderingThread=self
    """
    Loops through sending events down to the renderobj and drawing the framerate
    for debug/ performance checking purposes, as well as updating the display
    """
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
            """
            Since None evaluates to False, use this check to make sure that the 
            renderobj exists
            """
            if self.renderobj:
                with self.renderobj.lock:
                    self.renderobj.draw(Events.events)
            if Options.showFramerate:
                framerate = GlobalObjects.clock.get_fps()
                self.screen.blit(frameratefont.render(str(framerate),False,
                (255,0,0)),(0,0))
            pygame.display.flip()



#class IOThread(threading.Thread):
    
    
