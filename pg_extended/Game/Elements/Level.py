from typing import Iterable, Union
from json import load
import traceback
import pygame as pg


tileIdentifierType = Union[tuple[int, int], str, tuple[int, int, int], tuple[int, int, int, int], pg.Color]

class Level:
  def __init__(self, numTilesX: int, numTilesY: int, tileWidth: float, tileHeight: float, tilesMatrixJsonURL: str):
    self.numTilesX = numTilesX
    self.numTilesY = numTilesY
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.tilesMatrixJsonURL = tilesMatrixJsonURL

    self.tilesMatrix = []
    self.generateTilesMatrix()

    self.locked = True
    self.activeDraw = True
    self.surface: pg.Surface = None
    self.scene: 'Scene' = None # type: ignore

    self.width = tileWidth * numTilesX
    self.height = tileHeight * numTilesY

  def generateTilesMatrix(self):
    try:
      with open(self.tilesMatrixJsonURL, 'r') as f:
        rawJson = load(f)
        tilesMatrixRaw = rawJson['tiles']

        for row in tilesMatrixRaw:
          self.tilesMatrix.append([])
          for tile in row:
            if isinstance(tile[1], str):
              self.tilesMatrix[-1].append((rawJson['atlases'][tile[0]], tile[1]))
            else:
              self.tilesMatrix[-1].append((rawJson['atlases'][tile[0]], (*tile[1],)))

    except Exception as e:
      print(e)
      traceback.print_exc()

  def recalcDim(self):
    self.width = self.tileWidth * self.numTilesX
    self.height = self.tileHeight * self.numTilesY

  def renderLevelSurface(self):
    self.recalcDim()

    self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)

    y = -1
    for row in self.tilesMatrix:
      y += 1
      x = -1
      for tile in row:
        atlasID, tileID = tile[0], tile[1]

        x += 1

        currentTile = pg.transform.scale(self.scene.elements[atlasID].getTile(tileID), (self.tileWidth, self.tileHeight))

        if currentTile is None: continue

        tilePos = (self.tileWidth * x, self.tileHeight * y)

        self.surface.blit(currentTile, tilePos)

  def updateTile(self, poses: Iterable[tuple[int, int]], tiles: tuple[tuple[int, tileIdentifierType]]):
    for i in range(len(poses)):
      x, y = poses[i]
      atlasID = tiles[i][0]
      tileID = tiles[i][1]

      tile = self.scene.elements[atlasID].getTile(tileID)

      if tile is None: continue

      tile = pg.transform.scale(tile, (self.tileWidth, self.tileHeight))

      tilePos = (self.tileWidth * x, self.tileHeight * y)

      self.surface.blit(tile, tilePos)

  def initiate(self, scene: 'Scene') -> bool: # type: ignore
    try:
      self.scene = scene
      self.renderLevelSurface()
      self.locked = False
      return True
    except Exception as e:
      print(e)
      traceback.print_exc()
      return False
