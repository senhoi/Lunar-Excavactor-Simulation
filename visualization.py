import pygame
import math
import numpy as np
from pygame.locals import *
from excavation_arm import ExcArm
from excavation_force import ExcForce

class VisualArm(object):
    def __init__(self, ts, rads):
        self.proportion = 100       # pixels per meter
        self.length = 1
        self.ts = ts.flatten().tolist()
        self.rads = rads.flatten().tolist()

        self.prev_t = 0

    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        try:
            rad = self.rads.pop(0)
            t = self.ts.pop(0)
            delta_t = int((t - self.prev_t)*1000)
            self.prev_t = t
            x = self.length * self.proportion * math.sin(rad)
            y = self.length * self.proportion * math.cos(rad)
            return x, y, delta_t
        except IndexError:
            raise StopIteration


class App:
    def __init__(self, ts, rads):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 800, 600
        self._background = pygame.Surface((self.weight, self.height))
        self.vs_arm = iter(VisualArm(ts, rads))

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self._background, (0, 0))
        x, y, delta_t = next(self.vs_arm)
        print(f"x:{x} y:{y} t:{delta_t}")
        pygame.draw.line(self._display_surf, (255, 0, 0), (self.weight/2, self.height/2), (x+self.weight/2, y+self.height/2), 5)
        pygame.display.update()
        pygame.time.delay(delta_t)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    arm = ExcArm()
    sol = arm.integrate()
    t = np.linspace(0, 300, 3000)
    z = sol.sol(t)

    theApp = App(t, z.T[:,[0]])
    theApp.on_execute()




