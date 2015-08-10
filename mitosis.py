#!/usr/bin/env python3
########################################
#              PyGameLife              #
# Author  : Luke "Nukem" Jones         #
# Email   : luke.nukem.jones@gmail.com #
# License : GPLv3.0                    #
########################################
import pygame
#import mitosis
from random import randint
###########################
BLACK    = (   0,   0,   0)
GREEN    = (   0, 155,   0)
LGREEN   = (   0, 255,   0)
DREAD    = ( 110,   0,   0)
RED      = ( 255,   0,   0)
GREY     = (  50,  50,  50)
###########################
class CellLife:
    def __init__(self,screen, cellSize):
        ''' Base "Game of Life" Class:
            Must pass in a surface to draw to and the
            cell size for the grid. Class will get the
            rez from the surface, then set up the grid
            and background image.'''
        self.__alive = [] # The *alive* generation
        self.__dead = [] # The cells to be killed off
        self.__grid = [] # Array that keeps track of alive cells
        self.__screen = screen
        self.__width = self.__height = cellSize
        self.__margin = 1
        self.__row = int(self.__screen.get_size()[0] / (cellSize+self.__margin))
        self.__col = int(self.__screen.get_size()[1] / (cellSize+self.__margin))
        self.__prevGen = []
        self.__genCount = 0
        # Initialize
        self.resetGrid()
        # Sets up the background as a stored surface to prevent continuous looping.
        self.__bg = pygame.Surface((self.__screen.get_size()[0], self.__screen.get_size()[1]))
        self.__bg.fill(BLACK)
        for y in range(self.__col):
            for x in range(self.__row):
                pygame.draw.rect(self.__bg,GREY,[ (self.__margin+self.__width)*x+self.__margin,
                    (self.__margin+self.__height)*y+self.__margin, self.__width, self.__height ])
        self.__bg.convert()
    ########################################
    def getGridWidth(self):
        ''' Returns the width of the grid'''
        return self.__row
    def getGridHeight(self):
        ''' Returns the height of the grid'''
        return self.__col
    def getGenCount(self):
        ''' Get the current number of generation'''
        return self.__genCount    
    ########################################
    def setGridpos(self,pos,var):
        self.__grid[pos[1]][pos[0]] = var
    def addAlive(self,pos):
        self.__alive.append(pos)
    ########################################            
    def resetGrid(self):
        self.__grid = []
        for y in range(self.__col):
            self.__grid.append([])
            for x in range(self.__row):
                self.__grid[y].append(0) # Append a cell
        self.__alive = []
        self.__dead = []
        self.__prevGen = []
        self.__genCount = 0
    ########################################
    def paused(self):
        # change to a preset BG
        self.drawBG()
        for cell in self.__alive:
            self.__drawSquare(cell[0],cell[1],RED)
    ########################################
    def drawBG(self):
        self.__screen.blit(self.__bg, (0,0))
    ########################################
    def __drawSquare(self,x,y,colour):
        pygame.draw.rect(self.__screen,colour,[ (self.__margin+self.__width)*x+self.__margin,
            (self.__margin+self.__height)*y+self.__margin, self.__width, self.__height ])
    ########################################
    def clicked(self,pos,make):
        x=pos[0] // (self.__width+self.__margin)
        y=pos[1] // (self.__height+self.__margin)
        # Set that location to one
        if x > self.__row-1: x = self.__row-1
        if y > self.__col-1: y = self.__col-1
        if y < self.__col and x < self.__row:
            if make == 1:
                self.__grid[y][x]=1
                if (x,y) not in self.__alive:
                    self.__alive.append((x,y))
                self.__drawSquare(x,y,RED)
            elif make == 0:
                self.__grid[y][x]=0
                try:
                    cell = self.__alive.index((x,y))
                    self.__alive.pop(cell)
                except:
                    pass
                self.__drawSquare(x,y,GREY)
    ########################################
    def __checkPos(self,cell,x,y,grid):
        x,y = (cell[0]+x), (cell[1]+y)
        lenGridX, lenGridY = self.__row-1, self.__col-1
        if      (x < 0)        : x = lenGridX
        elif    (x > lenGridX) : x = 0
        if      (y < 0)        : y = lenGridY
        elif    (y > lenGridY) : y = 0
        return (x,y)

        for y in range(self.__col):
            for x in range(self.__row):
                if (x,y) in self.__alive:
                    self.__drawSquare(x,y,RED)
                else:
                    self.__drawSquare(x,y,GREY)
    ########################################
    def update(self):
        if self.__prevGen != self.__alive:
            self.__genCount +=1
        for cell in self.__alive:
            self.__grid[cell[1]][cell[0]] = 1
            self.__drawSquare(cell[0],cell[1],GREEN)
        for cell in self.__dead:
            self.__grid[cell[1]][cell[0]] = 0
            self.__drawSquare(cell[0],cell[1],GREY)
        
        self.__dead = []
        nextGen =[]
        deadDict = {}
        for cell in set(self.__alive):
            nCount = 0
            for y in(-1,0,1):
                for x in(-1,0,1):
                    tempCell = self.__checkPos(cell,x,y,self.__grid)
                    if cell != tempCell:
                        cellAliveResult = self.__grid[tempCell[1]][tempCell[0]]
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
                self.__drawSquare(cell[0],cell[1],GREEN)
            else:
                self.__dead.append(cell)
                self.__drawSquare(cell[0],cell[1],DREAD)
        for cell in deadDict:
            if deadDict[cell][0] == 3:
                nextGen.append(cell)
                self.__drawSquare(cell[0],cell[1],LGREEN)
        self.__prevGen = self.__alive
        self.__alive = nextGen