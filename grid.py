from random import randint
import pygame as pg
from cell import Cell

class Grid:
	def __init__(self, screenSize):
		self.screenSize = screenSize
		self.gridSize = [50, 50]
		self.cellCount = self.gridSize[0] * self.gridSize[1]
		self.cellSize = [screenSize[0] / self.gridSize[0], screenSize[1] / self.gridSize[1]]
		self.cells = []
		self.initCellList()
#		self.listCells() #debug purposes, lists all cells, their position, and active status
		self.currentTick = 0
		self.maxTick = 40
		self.curState = 0 #states: 0-preparing each cell's next move, 1-moving cells.

	def initCellList(self):
		self.cells = []
		for y in range(self.gridSize[1]): #start with y coord first
			for x in range(self.gridSize[0]):
				self.cells.append(Cell((x, y), 0))

	def handleEvents(self, event):
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_c:
				self.initCellList()
			if event.key == pg.K_r:
				self.randomizeCells()
		if pg.mouse.get_pressed()[0]:
			for x in range(0, self.screenSize[0], int(self.cellSize[0])):
				for y in range(0, self.screenSize[1], int(self.cellSize[1])):
					if pg.mouse.get_pos()[0] > x and pg.mouse.get_pos()[0] < x + self.cellSize[0]:
						if pg.mouse.get_pos()[1] > y and pg.mouse.get_pos()[1] < y + self.cellSize[1]:
							if self.cells[self.getIndexbyCellPos((int(x / self.cellSize[0]), int(y / self.cellSize[1])))].getActive() == False:
							  self.cells[self.getIndexbyCellPos((int(x / self.cellSize[0]), int(y / self.cellSize[1])))].setActive(1)

	def randomizeCells(self):
		self.cells = []
		for y in range(self.gridSize[1]): #start with y coord first
			for x in range(self.gridSize[0]):
				if randint(0,4) == 0: #25% chance for cell to start active
					self.cells.append(Cell((x, y), 1))	
				else:
					self.cells.append(Cell((x, y), 0))	

	def getCellbyPos(self, pos):
		return self.cells[(self.gridSize[0] * pos[1]) + pos[0]]

	def getIndexbyCellPos(self, pos):
		return (self.gridSize[0] * pos[1]) + pos[0]

	def listCells(self):
		print("--- Cells ---")
		for i in range(self.cellCount):
			print("   [" + str(i) + "] (" + str(self.cells[i].getPos()) + ") -> " + str(self.cells[i].getActive()))
		print("--- Done ---")

	def render(self, screen):
		self.renderGrid(screen)
		self.renderCells(screen)

	def renderGrid(self, screen):
		for x in range(0, self.gridSize[0]):
			pg.draw.rect(screen, (150, 150, 150), [self.cellSize[0] * x, 0, 1, self.screenSize[1]]) #vertical lines
		for y in range(0, self.gridSize[1]):
			pg.draw.rect(screen, (150, 150, 150), [0, self.cellSize[1] * y, self.screenSize[0], 1]) #horizontal lines				

	def renderCells(self, screen):
		for cell in self.cells:
			if cell.getActive():
				pg.draw.rect(screen, (220, 35, 35), [cell.getPos()[0] * self.cellSize[0], cell.getPos()[1] * self.cellSize[1], self.cellSize[0], self.cellSize[1]])

	def updateCells(self):
		if self.curState == 0: #preparing the cells' next moves
			for cell in self.cells:
				if cell.getActive() == False:
					continue

				curCellPos = cell.getPos()
				cellUnder = -1
				cellUnderLeft = -1
				cellUnderRight = -1

				if curCellPos[1] < self.gridSize[1] - 1:
					cellUnder = self.getCellbyPos([curCellPos[0], curCellPos[1] + 1])
					if curCellPos[0] > 0:	
						cellUnderLeft = self.getCellbyPos([curCellPos[0] - 1, curCellPos[1] + 1])
					if curCellPos[0] < self.gridSize[1] - 1:
						cellUnderRight = self.getCellbyPos([curCellPos[0] + 1, curCellPos[1] + 1])
				else:
					self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "none"

				if cellUnder != -1 and cellUnder.getActive() == False:
					self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "down"
					continue
				else:
					if cellUnderRight != -1 and cellUnderRight.getActive() == False and cellUnderLeft != -1 and cellUnderLeft.getActive() == False:
						self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "downRand"
					elif cellUnderRight != -1 and cellUnderRight.getActive() == False:
						self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "downR"
					elif cellUnderLeft != -1 and cellUnderLeft.getActive() == False:
						self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "downL"
					else:
						self.cells[self.getIndexbyCellPos(curCellPos)].nextMove = "none"

			self.curState = 1
		elif self.curState == 1: #updating cells by current move
			for cell in self.cells:
				curCellPos = cell.getPos()

				if cell.nextMove == "none":
					continue
				if cell.nextMove == "down":
					self.cells[self.getIndexbyCellPos((curCellPos[0], curCellPos[1] + 1))].setActive(1)
					self.cells[self.getIndexbyCellPos(curCellPos)].setActive(0)
				if cell.nextMove == "downRand":
					lr = randint(0,1)
					if lr == 0:
						lr = -1
					self.cells[self.getIndexbyCellPos((curCellPos[0] + lr, curCellPos[1] + 1))].setActive(1)
					self.cells[self.getIndexbyCellPos(curCellPos)].setActive(0)
				if cell.nextMove == "downR":
					self.cells[self.getIndexbyCellPos((curCellPos[0] + 1, curCellPos[1] + 1))].setActive(1)
					self.cells[self.getIndexbyCellPos(curCellPos)].setActive(0)
				if cell.nextMove == "downL":
					self.cells[self.getIndexbyCellPos((curCellPos[0] - 1, curCellPos[1] + 1))].setActive(1)
					self.cells[self.getIndexbyCellPos(curCellPos)].setActive(0)

				cell.nextMove = ""
			self.curState = 0

	def updateTick(self):
		if self.currentTick < self.maxTick:
			self.currentTick = self.currentTick + 1
		elif self.currentTick >= self.maxTick:
			self.updateCells()
			self.currentTick = 0

	def update(self):
		self.updateTick()