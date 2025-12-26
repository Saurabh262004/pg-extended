import pygame as pg
import pg_extended as pgx

class Utility:
  def changeTitle(self, title: str):
    self.title = title
    pg.display.set_caption(self.title)

  def screenResized(self) -> bool:
    if not self.running:
      return None

    tmpSW = self.screen.get_width()
    tmpSH = self.screen.get_height()

    if (self.screenWidth != tmpSW) or (self.screenHeight != tmpSH):
      self.screenWidth, self.screenHeight = self.screen.get_width(), self.screen.get_height()
      return True

    return False

  def setViewPort(self, viewPort: pgx.Game.ViewPort):
    self.viewPort = viewPort

    if self.running:
      self.viewPort.initiate(self.screen, self.activeScene)

  def resetUI(self):
    if not self.running:
      return None

    for dvKey in self.lazyDynamicValues:
      self.lazyDynamicValues[dvKey].resolveValue()

    for avKey in self.customAnimatedValues:
      self.customAnimatedValues[avKey].updateRestingPos()

    if self.customUpdateProcess is not None:
      self.customUpdateProcess()

    if self.activeScene is not None:
      self.activeScene.lazyUpdate()

    if self.viewPort is not None:
      self.viewPort.update()
      self.viewPort.renderScene()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].lazyUpdate()
