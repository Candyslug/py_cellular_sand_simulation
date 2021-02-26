class Cell:
	def __init__(self, pos, isActive):
		self.pos = pos
		self.isActive = isActive
		self.nextMove = "" #options are: none, down, downL, downR

	def setActive(self, value):
		if self.isActive != value:
			self.isActive = value

	def getPos(self):
		return self.pos[0], self.pos[1]

	def getActive(self):
		return self.isActive