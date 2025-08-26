import pygame as pg
from pg_extended.Core import DynamicValue
from pg_extended.Game.Scene import Scene

class ViewPort:
  def __init__(self, x: DynamicValue, y: DynamicValue, scale: float):
    self.x = x
    self.y = y
    self.scale = scale

    self.scaledLevelSurface: pg.Surface = None
    self.preRendererdView: pg.Surface = None
    self.parentSurface: pg.Surface = None
    self.scalingMultiplier: float = 10.0
    self.scalingFactor: float = 0.0
    self.scaledTileWidth: float = 0.0
    self.scaledTileHeight: float = 0.0
    self.scenePosition: tuple[float, float] = (0.0, 0.0)
    self.locked: bool = True

  def initiate(self, surface: pg.Surface, scene: Scene):
    self.parentSurface = surface
    self.scene = scene

    self.locked = False
    self.update()

  def update(self):
    self.scalingFactor = self.parentSurface.get_height() / (self.scale * self.scalingMultiplier * self.scene.activeLevel.atlas.tileHeight)

    self.scaledTileWidth = self.scene.activeLevel.atlas.tileWidth * self.scalingFactor
    self.scaledTileHeight = self.scene.activeLevel.atlas.tileHeight * self.scalingFactor

    self.x.resolveValue()
    self.y.resolveValue()

    self.scenePosition = (-self.scaledTileWidth * self.x.value, -self.scaledTileHeight * self.y.value)

  def renderScene(self):
    if self.locked: return None

    self.update()

    self.scaledLevelSurface = pg.transform.scale_by(self.scene.activeLevel.surface, self.scalingFactor)

    self.preRenderedView = pg.Surface(self.parentSurface.get_size(), pg.SRCALPHA)

    self.preRenderedView.blit(self.scaledLevelSurface)

  def draw(self):
    if self.locked: return None

    self.parentSurface.blit(self.preRenderedView, self.scenePosition)
