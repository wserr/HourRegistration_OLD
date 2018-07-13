import pygame
from pygame import locals
from BusinessLogic import Globals
import queue

class DAController:
    def __init__(self,queue,killEvent):
        self.Queue = queue
        self.KillEvent = killEvent
        pygame.init()
        pygame.joystick.init() # main joystick device system
        try:
            self.Joystick = pygame.joystick.Joystick(0) # create a joystick instance
            self.Joystick.init() # init instance
            print('Enabled joystick: ' + self.Joystick.get_name())
        except pygame.error:
            print('no joystick found.')

    def Listen(self):
        while not self.KillEvent.wait(1):
            for e in pygame.event.get(): # iterate over event stack
                if e.type == pygame.locals.JOYBUTTONDOWN: # 10
                    if self.Joystick.get_button(0):
                        self.Queue.put(0)
                    elif self.Joystick.get_button(1):
                        self.Queue.put(1)
                    elif self.Joystick.get_button(2):
                        self.Queue.put(2)
                    elif self.Joystick.get_button(3):
                        self.Queue.put(3)
 



