from json import load
import traceback
import pygame as pg
from pg_extended.Types import TileIdentifier
from pg_extended.Game.Elements import Entity

class Level:
  def __init__(self, numTilesX: int, numTilesY: int, tileWidth: float, tileHeight: float, tilesMatrixJsonURL: str):
    self.numTilesX = numTilesX
    self.numTilesY = numTilesY
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.tilesMatrixJsonURL = tilesMatrixJsonURL

    self.tileLayers = []
    self.generateTilesMatrix()

    self.locked = True
    self.activeDraw = True
    self.surface: pg.Surface = None
    self.scene: 'Scene' = None # type: ignore
    self.entities: list[Entity] = []

    self.width = tileWidth * numTilesX
    self.height = tileHeight * numTilesY

  def generateTilesMatrix(self):
    try:
      with open(self.tilesMatrixJsonURL, 'r') as f:
        rawJson = load(f)
        layersRaw = rawJson['layers']

        for layer in layersRaw:
          self.tileLayers.append([])
          for row in layer:
            self.tileLayers[-1].append([])
            for tile in row:
              if tile is None:
                self.tileLayers[-1][-1].append(None)
              elif isinstance(tile[1], str):
                self.tileLayers[-1][-1].append((rawJson['atlases'][tile[0]], tile[1]))
              else:
                self.tileLayers[-1][-1].append((rawJson['atlases'][tile[0]], (*tile[1],)))

    except Exception as e:
      print(e)
      traceback.print_exc()

  def recalcDim(self):
    self.width = self.tileWidth * self.numTilesX
    self.height = self.tileHeight * self.numTilesY

  def renderLevelSurface(self):
    self.recalcDim()

    self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)

    for layer in self.tileLayers:
      y = -1
      for row in layer:
        y += 1
        x = -1
        for tile in row:
          x += 1

          if tile is None: continue

          atlasID, tileID = tile[0], tile[1]

          currentTile = pg.transform.scale(self.scene.textureAtlases[atlasID].getTile(tileID), (self.tileWidth, self.tileHeight))

          if currentTile is None: continue

          tilePos = (self.tileWidth * x, self.tileHeight * y)

          self.surface.blit(currentTile, tilePos)

  def updateTile(self, poses: list[tuple[int, int]] | tuple[tuple[int, int]], tiles: list[tuple[int, TileIdentifier]] | tuple[tuple[int, TileIdentifier]]):
    for i in range(len(poses)):
      x, y = poses[i]
      atlasID = tiles[i][0]
      tileID = tiles[i][1]

      tile = self.scene.textureAtlases[atlasID].getTile(tileID)

      if tile is None: continue

      tile = pg.transform.scale(tile, (self.tileWidth, self.tileHeight))

      tilePos = (self.tileWidth * x, self.tileHeight * y)

      self.surface.blit(tile, tilePos)

  def addEntity(self, entity: Entity):
    self.entities.append(entity)

  def initiate(self, scene: 'Scene') -> bool: # type: ignore
    try:
      self.scene = scene
      self.renderLevelSurface()

      for entity in self.entities:
        entity.initiate(self, scene)

      self.locked = False
      return True
    except Exception as e:
      print(e)
      traceback.print_exc()
      return False
