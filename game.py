#!/usr/bin/env python3
import pygame
import mitosis
from random import randint

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 155,   0)
LGREEN    = (   0, 255,   0)
DREAD    = (   110, 0,   0)
RED      = ( 255,   0,   0)
GREY     = ( 50,   50,  50)

class LifeGame:
    def __init__(self):
        pygame.init()
        #sinitSize = [1920,1000]
        initSize = [1024,768]
        self.screen = pygame.display.set_mode(initSize)
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        
        self.state = 1
        self.cellLife = mitosis.CellLife(self.screen)
        self.font = pygame.font.Font(None, 42)
        self.instr = ['Press Enter to exit instructions','',
                             'Mouse B1 = Place Cell',
                             'Hold Mouse B1 to Paint',
                             'Mouse B2 = Erase Cell',
                             'Hold Mouse B2 to Paint Erase',
                             'Press P to Start/Pause',
                             'Press R to Reset Board',
                             'Press F to Speed up',
                             'Press S to Slow down']
        
        self.simSpeed = {'1 second':60, '0.5ms':30, '0.25ms':15,
                         '0.12ms':12, '0.06ms':6, '0.03ms':3,
                         '0.02ms':2,'Realtime':1}
        self.speed = 3
        
    def main(self):
        framecount = 0
        while True:
            self.getEvents()
            # Menu State
            if self.state == 1:
                self.screen.fill(BLACK)
                self.cellLife.drawBG()
                for i in range(len(self.instr)):
                    text = self.font.render(self.instr[i], 1, WHITE)
                    self.screen.blit(text,(100,100+i*30))
            # Paused State    
            elif self.state == 2:
                self.screen.fill(BLACK)
                self.cellLife.paused()
            # Running State
            elif self.state == 3:
                if framecount > self.speed:
                    self.screen.fill(BLACK)
                    self.cellLife.drawBG()
                    self.cellLife.update()
                    framecount = 0
            # Game Tick
            framecount += 1
            self.clock.tick(60)
            pygame.display.flip()
    
    def getEvents(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                quit()
                pygame.quit()
            # Mouse interaction in Running and Paused states.
            if event.type == pygame.MOUSEBUTTONDOWN and self.state != 1:
                while True:
                    event = pygame.event.poll()
                    pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.cellLife.clicked(pos,1)
                        pygame.display.flip()
                    elif pygame.mouse.get_pressed()[1] == 1 or pygame.mouse.get_pressed()[2] == 1:
                        self.cellLife.clicked(pos,0)
                        pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONUP and event.button in (1,2,3):
                        break
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_p] == 1:
                    if self.state == 2:
                        self.state = 3
                    elif self.state == 3:
                        self.state = 2
                if pygame.key.get_pressed()[pygame.K_RETURN] == self.state == 1:
                    self.state = 2
                if pygame.key.get_pressed()[pygame.K_r] == 1:
                    self.cellLife.resetGrid()
                    if self.state == 3: self.state = 2
                if pygame.key.get_pressed()[pygame.K_f] == 1:
                    if self.state == 3:
                        if   self.speed > 30: self.speed -= 10
                        elif self.speed > 15: self.speed -= 5
                        elif self.speed > 5: self.speed -= 2
                        elif self.speed > 0:  self.speed -=1
                elif pygame.key.get_pressed()[pygame.K_s] == 1:
                    if self.state == 3:
                        if   self.speed < 5: self.speed +=1
                        elif self.speed < 15: self.speed +=2
                        elif self.speed < 30: self.speed +=5
                        elif self.speed < 60: self.speed +=10
                        

if __name__=='__main__':
    game = LifeGame()
    game.main()