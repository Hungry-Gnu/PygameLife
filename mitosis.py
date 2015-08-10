#!/usr/bin/env python3
import pygame
#import mitosis
from random import randint

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 155,   0)
LGREEN    = (   0, 255,   0)
DREAD    = (   110, 0,   0)
RED      = ( 255,   0,   0)
GREY     = ( 50,   50,  50)

class CellLife:
    def __init__(self,screen,cellSize):
        self.alive = []
        self.dead = []
        self.screen = screen
        self.width = self.height = cellSize
        self.margin = 1
        self.row = int(self.screen.get_size()[0] / (cellSize+self.margin))
        self.col = int(self.screen.get_size()[1] / (cellSize+self.margin))
        print("col=",self.col)
        print(self.margin)
        self.resetGrid()
                
        self.bg = pygame.Surface((self.screen.get_size()[0], self.screen.get_size()[1]))
        self.bg.fill(BLACK)
        for y in range(self.col):
            for x in range(self.row):
                pygame.draw.rect(self.bg,GREY,[ (self.margin+self.width)*x+self.margin,
                    (self.margin+self.height)*y+self.margin, self.width, self.height ])
        self.bg.convert()
                
    def resetGrid(self):
        self.grid = []
        for y in range(self.col):
            self.grid.append([])
            for x in range(self.row):
                self.grid[y].append(0) # Append a cell
        self.alive = []
        self.dead = []
                
    def paused(self):
        # change to a preset BG
        self.drawBG()
        for cell in self.alive:
            self.drawSquare(cell[0],cell[1],RED)
                    
    def drawBG(self):
        self.screen.blit(self.bg, (0,0))

    def drawSquare(self,x,y,colour):
        pygame.draw.rect(self.screen,colour,[ (self.margin+self.width)*x+self.margin,
            (self.margin+self.height)*y+self.margin, self.width, self.height ])

    def clicked(self,pos,make):
        x=pos[0] // (self.width+self.margin)
        y=pos[1] // (self.height+self.margin)
        # Set that location to one
        if x > self.row-1: x = self.row-1
        if y > self.col-1: y = self.col-1
        if y < self.col and x < self.row:
            if make == 1:
                self.grid[y][x]=1
                if (x,y) not in self.alive:
                    self.alive.append((x,y))
                self.drawSquare(x,y,RED)
            elif make == 0:
                self.grid[y][x]=0
                try:
                    cell = self.alive.index((x,y))
                    self.alive.pop(cell)
                except:
                    pass
                self.drawSquare(x,y,GREY)

    def checkPos(self,cell,x,y,grid):
        x,y = (cell[0]+x), (cell[1]+y)
        lenGridX, lenGridY = self.row-1, self.col-1
        if      (x < 0)        : x = lenGridX
        elif    (x > lenGridX) : x = 0
        if      (y < 0)        : y = lenGridY
        elif    (y > lenGridY) : y = 0
        return (x,y)

        for y in range(self.col):
            for x in range(self.row):
                if (x,y) in self.alive:
                    self.drawSquare(x,y,RED)
                else:
                    self.drawSquare(x,y,GREY)
        
    def update(self):
        for cell in self.alive:
            self.grid[cell[1]][cell[0]] = 1
            self.drawSquare(cell[0],cell[1],GREEN)
        for cell in self.dead:
            self.grid[cell[1]][cell[0]] = 0
            self.drawSquare(cell[0],cell[1],GREY)
        
        self.dead = []
        nextGen =[]
        deadDict = {}
        for cell in set(self.alive):
            nCount = 0
            for y in(-1,0,1):
                for x in(-1,0,1):
                    tempCell = self.checkPos(cell,x,y,self.grid)
                    if cell != tempCell:
                        cellAliveResult = self.grid[tempCell[1]][tempCell[0]]
                        # If it's a dead cell, check it.
                        if cellAliveResult == 1:
                            nCount += 1 
                        elif cellAliveResult == 0:
                            if deadDict.get(tempCell):
                                deadDict[tempCell][0]+=1
                            else:
                                deadDict[tempCell] = [1]
            if nCount in(2,3):
                nextGen.append(cell)
                self.drawSquare(cell[0],cell[1],GREEN)
            else:
                self.dead.append(cell)
                self.drawSquare(cell[0],cell[1],DREAD)
        for cell in deadDict:
            if deadDict[cell][0] == 3:
                nextGen.append(cell)
                self.drawSquare(cell[0],cell[1],LGREEN)
        self.alive = nextGen