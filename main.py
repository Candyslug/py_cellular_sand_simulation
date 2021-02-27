import pygame as pg 
from grid import Grid

class Window():
	def __init__(self):
		pg.init()
		self.windowSize = [1000,1000]
		self.isOpen = True
		self.screen = pg.display.set_mode(self.windowSize)
		self.myGrid = Grid(pg.display.get_surface().get_size())
		self.setWindowName("Sand Sim")

	def setWindowName(self, text):
		pg.display.set_caption(text)

	def mainLoop(self):
		while self.isOpen:
			self.handleEvents()
			self.update()
			self.render()
		else:
			self.quit()

	def handleEvents(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.isOpen = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
			if self.isOpen:
				self.myGrid.handleEvents(event)

	def update(self):
		self.myGrid.update()

	def render(self):
		pass
		pg.draw.rect(self.screen, (255, 0, 0), [80, 50, 100,70])
		self.screen.fill((30, 30, 30)) #background
		self.myGrid.render(self.screen)
		pg.display.update()

	def quit(self):
		self.isOpen = False
		pg.quit()

if __name__ == '__main__':
	myWindow = Window()
	myWindow.mainLoop()
