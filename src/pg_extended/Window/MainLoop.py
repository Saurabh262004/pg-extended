import pygame as pg

class MainLoop:
	def updateLoop(self):
		self.handleEvents()

		if self.secondResize or self.screenResized():
			self.secondResize = not self.secondResize
			self.resetUI()

		self.currentFPS = self.clock.get_fps()

		self.screen.fill((0, 0, 0))

		for dvKey in self.customDynamicValues:
			self.customDynamicValues[dvKey].resolveValue()

		for avKey in self.customAnimatedValues:
			self.customAnimatedValues[avKey].resolveValue()

		for systemID in self.systemZ:
			if systemID in self.activeSystems:
				self.activeSystems[systemID].update()

		if self.customLoopProcess is not None:
			self.customLoopProcess()

		for systemID in self.systemZ:
			if systemID in self.activeSystems:
				self.activeSystems[systemID].draw()

		if self.customDrawProcess is not None:
			self.customDrawProcess()

		self.firstUpdate = False
		pg.display.flip()
		self.clock.tick(self.fps)
