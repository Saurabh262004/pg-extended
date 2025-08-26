from typing import Iterable, Union
from json import load
import traceback
import pygame as pg
from pg_extended.Game.Elements import TextureAtlas

tileIdentifierType = Union[tuple[int, int], str, tuple[int, int, int], tuple[int, int, int, int], pg.Color]

class Level:
  def __init__(self, numTilesX: int, numTilesY: int, atlas: TextureAtlas, tilesMatrixJsonURL: str):
    self.numTilesX = numTilesX
    self.numTilesY = numTilesY
    self.atlas = atlas
    self.tilesMatrixJsonURL = tilesMatrixJsonURL
    self.tilesMatrix = []

    self.generateTilesMatrix()

    self.locked = True
    self.activeDraw = True
    self.surface: pg.Surface = None

    self.width = atlas.tileWidth * numTilesX
    self.height = atlas.tileHeight * numTilesY

  def generateTilesMatrix(self):
    try:
      with open(self.tilesMatrixJsonURL, 'r') as f:
        self.tilesMatrix = load(f)['tiles']

    except Exception as e:
      print(e)
      traceback.print_exc()

  def recalcDim(self):
    self.width = self.atlas.tileWidth * self.numTilesX
    self.height = self.atlas.tileHeight * self.numTilesY

  def renderLevelSurface(self):
    self.recalcDim()

    self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)

    y = -1
    for row in self.tilesMatrix:
      y += 1
      x = -1
      for tileIdentifier in row:
        x += 1

        currentTile = self.atlas.getTile(tileIdentifier)

        if currentTile is None: continue

        tilePos = (self.atlas.tileWidth * x, self.atlas.tileHeight * y)

        self.surface.blit(currentTile, tilePos)

  def updateTile(self, poses: Iterable[tuple[int, int]], tileIdentifiers: Iterable[tileIdentifierType]):
    for i in range(len(poses)):
      x, y = poses[i]
      tileIdentifier = tileIdentifiers[i]

      tile = self.atlas.getTile(tileIdentifier)

      if tile is None: continue

      tilePos = (self.atlas.tileWidth * x, self.atlas.tileHeight * y)

      self.surface.blit(tile, tilePos)

  def initiate(self) -> bool:
    try:
      self.renderLevelSurface()
      self.locked = False
      return True
    except Exception as e:
      print(e)
      traceback.print_exc()
      return False
