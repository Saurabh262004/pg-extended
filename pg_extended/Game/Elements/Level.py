from typing import Iterable, Union
import traceback
import pygame as pg
from pg_extended.Core import DynamicValue
from pg_extended.Game.Elements import TextureAtlas

numType = Union[int, float]

class Level:
  def __init__(self, tileWidth: DynamicValue, tileHeight: DynamicValue, numTilesX: int, numTilesY: int, atlas: TextureAtlas, tilesMatrix: Iterable[Iterable[Union[tuple[int, int], str]]]):
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.numTilesX = numTilesX
    self.numTilesY = numTilesY
    self.atlas = atlas
    self.tilesMatrix = tilesMatrix

    self.locked = True
    self.activeDraw = True
    self.baseSurface: pg.Surface = None
    self.surface: pg.Surface = None

    self.width = tileWidth.value * numTilesX
    self.height = tileHeight.value * numTilesY

    self.unchangedWidth = atlas.tileWidth * numTilesX
    self.unchangedHeight = atlas.tileHeight * numTilesY

  def update(self):
    pass

  def handleEvent(self, event: pg.Event):
    pass

  def draw(self, surface: pg.Surface, pos: tuple[numType, numType]):
    surface.blit(self.surface, pos)

  def recalcDim(self):
    self.tileWidth.resolveValue()
    self.tileHeight.resolveValue()

    self.width = self.tileWidth.value * self.numTilesX
    self.height = self.tileHeight.value * self.numTilesY

    self.unchangedWidth = self.atlas.tileWidth * self.numTilesX
    self.unchangedHeight = self.atlas.tileHeight * self.numTilesY

  def rescaleSurface(self, smoothscale: bool = False):
    if self.unchangedWidth == self.width:
      self.surface = self.baseSurface
    else:
      if smoothscale:
        self.surface = pg.transform.smoothscale(self.baseSurface, (self.width, self.height))
      else:
        self.surface = pg.transform.scale(self.baseSurface, (self.width, self.height))

  def renderLevelSurface(self, smoothscale: bool = False):
    self.recalcDim()

    self.baseSurface = pg.Surface((self.unchangedWidth, self.unchangedHeight), pg.SRCALPHA)

    y = -1
    for row in self.tilesMatrix:
      y += 1
      x = -1
      for tileIdentifier in row:
        x += 1
        if isinstance(tileIdentifier, str):
          currentTile = self.atlas.namedTiles[tileIdentifier]
        elif isinstance(tileIdentifier, tuple):
          currentTile = self.atlas.tiles[tileIdentifier[0]][tileIdentifier[1]]
        else: continue

        tilePos = (self.atlas.tileWidth * x, self.atlas.tileHeight * y)

        self.baseSurface.blit(currentTile, tilePos)

    self.rescaleSurface(smoothscale)

  def initiate(self) -> bool:
    try:
      self.renderLevelSurface()
      self.locked = False
      return True
    except Exception as e:
      print(e)
      traceback.print_exc()
      return False
