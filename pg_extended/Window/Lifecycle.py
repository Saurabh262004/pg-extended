import pygame as pg

class Lifecycle:
  def openWindow(self):
    self.time = pg.time
    self.clock = self.time.Clock()
    self.currentFPS: int = self.clock.get_fps()

    pg.display.set_caption(self.title)

    self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight), pg.RESIZABLE)

    receivedWidth, receivedHeight = self.screen.get_size()

    if ((not receivedWidth == self.screenWidth) or (not receivedHeight == self.screenHeight)):
      self.screenWidth, self.screenHeight = receivedWidth, receivedHeight

    self.running = True
    self.secondResize = False

    self.initiateActiveScene(self.screen)

    self.initiateActiveSystems(self.screen)

    if self.viewPort is not None:
      self.viewPort.initiate(self.screen, self.activeScene)

    self.resetUI()

    while self.running:
      self.updateLoop()

    self.closeWindow()

  def closeWindow(self):
    self.running = False
    self.deactivateSystems('all')
    self.deactivateScene()

    del self.screen
    del self.time
    del self.clock
