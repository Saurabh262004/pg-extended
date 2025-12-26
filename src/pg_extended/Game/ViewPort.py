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
    self.lazyRender: bool = False

  def initiate(self, surface: pg.Surface, scene: Scene):
    self.parentSurface = surface
    self.scene = scene

    self.locked = False
    self.update()

  def update(self):
    self.scalingFactor = self.parentSurface.get_height() / (self.scale * self.scalingMultiplier * self.scene.activeLevel.tileHeight)

    self.scaledTileWidth = self.scene.activeLevel.tileWidth * self.scalingFactor
    self.scaledTileHeight = self.scene.activeLevel.tileHeight * self.scalingFactor

    self.x.resolveValue()
    self.y.resolveValue()

    self.scenePosition = (-self.scaledTileWidth * self.x.value, -self.scaledTileHeight * self.y.value)

  def renderScene(self):
    if self.locked: return None

    self.scaledLevelSurface = pg.transform.scale_by(self.scene.activeLevel.surface, self.scalingFactor)

    self.preRenderedView = pg.Surface(self.parentSurface.get_size(), pg.SRCALPHA)

    self.preRenderedView.blit(self.scaledLevelSurface)

    for entity in self.scene.activeLevel.entities:
      if entity.sprite is None: continue

      entitySprite = pg.transform.scale(entity.sprite, (int(entity.widthPX * self.scalingFactor), int(entity.heightPX * self.scalingFactor)))

      entityPos = (self.scaledTileWidth * entity.x, self.scaledTileHeight * entity.y)

      self.preRenderedView.blit(entitySprite, entityPos)

  def draw(self):
    if self.locked: return None

    self.parentSurface.blit(self.preRenderedView, self.scenePosition)
