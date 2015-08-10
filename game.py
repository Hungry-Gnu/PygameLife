#!/usr/bin/env python3
########################################
#              PyGameLife              #
# Author  : Luke "Nukem" Jones         #
# Email   : luke.nukem.jones@gmail.com #
# License : GPLv3.0                    #
########################################

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
        self.firstStart = 1
        self.enteredMainMenu = 1
        pygame.init()
        #initSize = [1920,1000]
        initSize = [1024,768]
        self.screen = pygame.display.set_mode(initSize)
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.state = 1

        self.cellLife = mitosis.CellLife(self.screen, 8)
        self.menuLife = mitosis.CellLife(self.screen, 5)

        for pos in [(2, 0), (1, 0), (1, 1), (1, 2), (0, 1)]:
            x = int(len(self.menuLife.grid[0])*0.2) + pos[0]
            y = int(len(self.menuLife.grid)*0.4) + pos[1]
            self.menuLife.grid[y][x] = 1
            self.menuLife.alive.append((x,y))
        # Cross
        for pos in [(1, 0), (1, 1), (1, 2), (2, 1), (0, 1)]:
            x = int(len(self.menuLife.grid[0])*0.5) + pos[0]
            y = int(len(self.menuLife.grid)*0.8) + pos[1]
            self.menuLife.grid[y][x] = 1
            self.menuLife.alive.append((x,y))
            self.menuLife.grid[y][x+4] = 1
            self.menuLife.alive.append((x+4,y))
        # Tetrinomo
        for pos in [(1, 0), (1, 1), (1, 2), (0, 2), (2, 1)]:
            x = int(len(self.menuLife.grid[0])*0.8) + pos[0]
            y = int(len(self.menuLife.grid)*0.2) + pos[1]
            self.menuLife.grid[y][x] = 1
            self.menuLife.alive.append((x,y))
            
        self.font = pygame.font.Font(None, 42)
        self.instr = ['Press Enter to exit instructions','',
                             'Mouse B1 = Place Cell',
                             'Mouse B2 = Erase Cell',
                             'Press P to Start/Pause',
                             'Press R to Reset Board',
                             'Press F to Speed up',
                             'Press S to Slow down']
        self.menuSurf = pygame.Surface((self.screen.get_size()[0], self.screen.get_size()[1]))
        self.menuSurf.fill(BLACK)
        self.menuSurf.set_colorkey(BLACK)
        self.speedString = "Set speed to "
        self.strings = {'pause':'Game Paused',  'speed':'Speed = '}
        self.simSpeed = {'1 second':60, '0.5ms':30, '0.25ms':15,
                         '0.12ms':12, '0.06ms':6, '0.03ms':3,
                         '0.02ms':2,'Realtime':1}
        self.speed = 3
        self.message = []
    
    def printHelp(self):
        self.menuSurf.fill(BLACK)
        for i in range(len(self.instr)):
            text = self.font.render(self.instr[i], 1, WHITE)
            x = self.menuSurf.get_rect().centerx - text.get_rect().centerx
            self.menuSurf.blit(text,(x,100+i*40))
    
    def mainMenu(self):
        if self.enteredMainMenu == 1:
            self.menuLife.resetGrid()
            for pos in [(2, 0), (1, 0), (1, 1), (1, 2), (0, 1)]:
                x = int(len(self.menuLife.grid[0])*0.2) + pos[0]
                y = int(len(self.menuLife.grid)*0.4) + pos[1]
                self.menuLife.grid[y][x] = 1
                self.menuLife.alive.append((x,y))
            # Cross
            for pos in [(1, 0), (1, 1), (1, 2), (2, 1), (0, 1)]:
                x = int(len(self.menuLife.grid[0])*0.5) + pos[0]
                y = int(len(self.menuLife.grid)*0.8) + pos[1]
                self.menuLife.grid[y][x] = 1
                self.menuLife.alive.append((x,y))
                self.menuLife.grid[y][x+4] = 1
                self.menuLife.alive.append((x+4,y))
            # Tetrinomo
            for pos in [(1, 0), (1, 1), (1, 2), (0, 2), (2, 1)]:
                x = int(len(self.menuLife.grid[0])*0.8) + pos[0]
                y = int(len(self.menuLife.grid)*0.2) + pos[1]
                self.menuLife.grid[y][x] = 1
                self.menuLife.alive.append((x,y))
            self.enteredMainMenu = 0
            
    def printPaused(self):
        self.menuSurf.fill(BLACK)
        text = self.font.render( self.strings['pause'], 1, WHITE)
        x = self.menuSurf.get_rect().centerx - text.get_rect().centerx
        y = self.menuSurf.get_rect().centery - text.get_rect().centery
        self.menuSurf.blit(text,(x,y))
    
    def printMsg(self):
        self.menuSurf.fill(BLACK)
        if self.message:
            for i in range(len(self.message)):
                text = self.font.render(self.message[i], 1, WHITE)
                self.menuSurf.blit(text,(10,10+i*40))

    def main(self):
        framecount = 0
        msgTime = 0
        self.screen.fill(BLACK)
        self.menuLife.drawBG()
        while True:
            self.getEvents()
            # Menu State
            if self.state == 1:
                    self.menuSurf.fill(BLACK)
                    if self.firstStart == 1 and framecount > 3:
                        self.screen.fill(BLACK)
                        self.menuLife.drawBG()
                        self.menuLife.update()
                        self.printHelp()
                        framecount = 0
                    elif self.firstStart == 0:
                        self.mainMenu()
                        self.printHelp()
                        self.screen.fill(BLACK)
                        self.menuLife.drawBG()
                        self.menuLife.update()
                        #self.cellLife.paused()
                    self.screen.blit(self.menuSurf,(0,0))
            # Paused State    
            elif self.state == 2:
                    self.screen.fill(BLACK)
                    if self.firstStart == 0:
                        self.printPaused()
                    else:
                        self.menuSurf.fill(BLACK)
                    self.cellLife.paused()
                    self.screen.blit(self.menuSurf,(0,0))
            # Running State
            elif self.state == 3:
                    if framecount > self.speed:
                        self.screen.fill(BLACK)
                        self.cellLife.drawBG()
                        self.cellLife.update()
                        framecount = 0
                    if msgTime > 60:
                        self.menuSurf.fill(BLACK)
                        self.message = []
                        self.screen.blit(self.menuSurf,(0,0))
                        msgTime = 0
                    else:
                        self.printMsg()
                        self.screen.blit(self.menuSurf,(0,0))
                        msgTime +=1
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
                if pygame.key.get_pressed()[pygame.K_RETURN] == self.state == 1:
                    self.state = 2
                if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
                    if   self.state == 3:
                        self.state = 1
                        self.enteredMainMenu = 1
                    elif self.state == 1:
                        self.state = 3
                        self.enteredMainMenu = 0
                if pygame.key.get_pressed()[pygame.K_p] == 1:
                    self.firstStart = 0
                    if   self.state == 2: self.state = 3
                    elif self.state == 3: self.state = 2
                if pygame.key.get_pressed()[pygame.K_r] == 1:
                    self.cellLife.resetGrid()
                    if self.state == 3: self.state = 2
                if pygame.key.get_pressed()[pygame.K_f] == 1:
                    if self.state == 3:
                        if   self.speed > 120: self.speed +=20
                        elif self.speed > 30: self.speed -= 10
                        elif self.speed > 15: self.speed -= 5
                        elif self.speed > 5: self.speed -= 2
                        elif self.speed > 0:  self.speed -=1
                        self.message.append(self.speedString+str(120 - self.speed))
                if pygame.key.get_pressed()[pygame.K_s] == 1:
                    if self.state == 3:
                        if   self.speed < 5: self.speed +=1
                        elif self.speed < 15: self.speed +=2
                        elif self.speed < 30: self.speed +=5
                        elif self.speed < 60: self.speed +=10
                        elif self.speed < 120: self.speed +=20
                        self.message.append(self.speedString+str(120 - self.speed))

if __name__=='__main__':
    game = LifeGame()
    game.main()