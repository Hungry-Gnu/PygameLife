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
###########################
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY     = ( 50,   50,  50)
###########################

class LifeGame:
    def __init__(self):
        self.firstStart = self.enteredMainMenu = 1
        pygame.init()
        initSize = [1920,1000]
        #initSize = [1024,768]
        self.screen = pygame.display.set_mode(initSize)
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.state = 'menu'
        self.enteredPattern = []
        self.cellLife = mitosis.CellLife(self.screen, 8)
        self.menuLife = mitosis.CellLife(self.screen, 5)

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
        self.frameCount = self.msgTime = 0
        self.message = []
        self.gameState = {'menu':self.stateMenu, 'paused':self.statePaused, 'running':self.stateRunning}
        self.resetMainMenuBG()

###############################
##     HELPER FUNCTIONS      ##
###############################
    def printHelp(self):
        self.menuSurf.fill(BLACK)
        for i in range(len(self.instr)):
            text = self.font.render(self.instr[i], 1, WHITE)
            x = self.menuSurf.get_rect().centerx - text.get_rect().centerx
            self.menuSurf.blit(text,(x,100+i*40))

    def resetMainMenuBG(self):
        self.menuLife.resetGrid()
        for pos in [(2, 0), (1, 0), (1, 1), (1, 2), (0, 1)]:
            x = int(self.menuLife.getGridWidth()*0.2) + pos[0]
            y = int(self.menuLife.getGridHeight()*0.4) + pos[1]
            self.menuLife.addAlive((x,y))
        # PULSAR!!!!
        for pos in [(1, 0), (1, 1), (1, 2), (2, 1), (0, 1)]:
            x = int(self.menuLife.getGridWidth()*0.5) + pos[0]
            y = int(self.menuLife.getGridHeight()*0.7) + pos[1]
            self.menuLife.addAlive((x-3,y))
            self.menuLife.addAlive((x+3,y))
        # Tetrinomo
        for pos in [(1, 0), (1, 1), (1, 2), (0, 2), (2, 1)]:
            x = int(self.menuLife.getGridWidth()*0.8) + pos[0]
            y = int(self.menuLife.getGridHeight()*0.2) + pos[1]
            self.menuLife.addAlive((x,y))

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

    def printGen(self):
        string = "Generation #"+str(self.cellLife.getGenCount())
        text = self.font.render(string, 1, WHITE)
        x = self.menuSurf.get_rect().centerx - text.get_rect().centerx
        self.menuSurf.blit(text,(x,10))

###############################
##        GAME STATES        ##
###############################
    def stateMenu(self):
        if self.state == 'menu':
            self.menuSurf.fill(BLACK)
            if self.firstStart == 1:
                ## Place holder. Will use for an intro
                self.printHelp()
            elif self.firstStart == 0:
                # Place holder, will use for a proper menu
                self.printHelp()
            if self.frameCount > 3:
                self.screen.fill(BLACK)
                self.menuLife.drawBG()
                self.menuLife.update()
                #self.cellLife.paused()
                self.frameCount = 0
            self.screen.blit(self.menuSurf,(0,0))
        
    def statePaused(self):
        if self.state == 'paused':
            self.screen.fill(BLACK)
            if self.firstStart == 0 and self.cellLife.getGenCount == 0:
                self.printPaused()
            else:
                self.menuSurf.fill(BLACK)
            self.cellLife.paused()
            self.screen.blit(self.menuSurf,(0,0))
        
    def stateRunning(self):
        if self.state == 'running':
            if self.frameCount > self.speed:
                self.screen.fill(BLACK)
                self.cellLife.drawBG()
                self.cellLife.update()
                self.frameCount = 0
            if self.msgTime > 60:
                self.menuSurf.fill(BLACK)
                self.message = []
                self.screen.blit(self.menuSurf,(0,0))
                self.msgTime = 0
            else:
                self.printMsg()
                self.printGen()
                self.screen.blit(self.menuSurf,(0,0))
                self.msgTime +=1
            
    def speedDown(self):
        if self.state == 'running':
            if   self.speed > 120: self.speed +=20
            elif self.speed > 30: self.speed -= 10
            elif self.speed > 15: self.speed -= 5
            elif self.speed > 5: self.speed -= 2
            elif self.speed > 0:  self.speed -=1
            self.message.append(self.speedString+str(120 - self.speed))
            
    def speedUp(self):
        if self.state == 'running':
            if   self.speed < 5: self.speed +=1
            elif self.speed < 15: self.speed +=2
            elif self.speed < 30: self.speed +=5
            elif self.speed < 60: self.speed +=10
            elif self.speed < 120: self.speed +=20
            self.message.append(self.speedString+str(120 - self.speed))

###############################
##         MAIN LOOP         ##
###############################
    def main(self):
        self.screen.fill(BLACK)
        self.menuLife.drawBG()
        while True:
            self.getEvents()
            # Menu State
            if self.state == 'menu':
                self.gameState['menu']()
            # Paused State
            elif self.state == 'paused':
                self.gameState['paused']()
            # Running State
            elif self.state == 'running':
                self.gameState['running']()
            # Game Tick
            self.frameCount += 1
            self.clock.tick(60)
            pygame.display.flip()

    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()
            # Mouse interaction in Running and Paused states.
            if event.type == pygame.MOUSEBUTTONDOWN and self.state != 'menu':
                while True:
                    event = pygame.event.poll()
                    pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.cellLife.clicked(pos,1)
                        pygame.display.flip()
                        #self.enteredPattern.append(pos)
                    elif pygame.mouse.get_pressed()[1] == 1 or pygame.mouse.get_pressed()[2] == 1:
                        self.cellLife.clicked(pos,0)
                        pygame.display.flip()
                    if event.type == pygame.MOUSEBUTTONUP and event.button in (1,2,3):
                        break
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RETURN] == 1 and self.state == 'menu':
                    self.state = 'paused'
                if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
                    if  self.state == 'running': self.state = 'menu'
                    elif self.state == 'menu': self.state = 'running'
                    self.stateMenu()
                    self.resetMainMenuBG()
                if pygame.key.get_pressed()[pygame.K_p] == 1:
                    if self.firstStart == 1: self.firstStart = 0
                    if   self.state == 'paused': self.state = 'running'
                    elif self.state == 'running': self.state = 'paused'
                    self.statePaused()
                if pygame.key.get_pressed()[pygame.K_r] == 1:
                    self.cellLife.resetGrid()
                    if self.state == 'running': self.state = 'paused'
                if pygame.key.get_pressed()[pygame.K_f] == 1:
                    self.speedDown()
                if pygame.key.get_pressed()[pygame.K_s] == 1:
                    self.speedUp()

if __name__=='__main__':
    game = LifeGame()
    game.main()
