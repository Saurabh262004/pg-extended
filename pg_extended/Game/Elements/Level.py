from typing import Iterable, Union
import pygame as pg
from pg_extended.Core import DynamicValue
from pg_extended.Game.Elements import TextureAtlas

class Level:
  def __init__(self, tileWidth: DynamicValue, tileHeight: DynamicValue, numTilesX: int, numTilesY: int, cameraX: float, cameraY: float, atlas: TextureAtlas, tilesMatrix: Iterable[Iterable[Union[tuple[int, int], str]]]):
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.numTilesX = numTilesX
    self.numTilesY = numTilesY
    self.cameraX = cameraX
    self.cameraY = cameraY
    self.atlas = atlas
    self.tilesMatrix = tilesMatrix

  def update(self):
    pass

  def handleEvent(self, event: pg.Event):
    pass

  def draw(self):
    pass

  def initiate(self):
    pass
