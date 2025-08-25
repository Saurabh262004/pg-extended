from typing import Union, Iterable, Dict, Optional
import pygame as pg

tileIdentifierType = Union[tuple[int, int], str, pg.Color]

class TextureAtlas:
  def __init__(self, tilesetURL: str, tileWidth: int, tileHeight: int, paddingX: int = 0, paddingY: int = 0, marginLeft: int = 0, marginTop: int = 0, names: Iterable[Iterable[str]] = None, sequences: Dict[str, Iterable[str]] = None):
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.paddingX = paddingX
    self.paddingY = paddingY
    self.marginLeft = marginLeft
    self.marginTop = marginTop
    self.names = names
    self.sequences = sequences

    self.tileset = pg.image.load(tilesetURL)

    self.tilesX = (self.tileset.get_width() - marginLeft) // (tileWidth + paddingX)
    self.tilesY = (self.tileset.get_height() - marginTop) // (tileHeight + paddingY)

    self.tiles = []
    self.namedTiles = {}
    self.sequencedTiles = {}

  def generateTiles(self):
    self.tileset.convert_alpha()

    for x in range(self.tilesX):
      self.tiles.append([])
      for y in range(self.tilesY):
        tileX = self.marginLeft + (x * (self.tileWidth + self.paddingX))
        tileY = self.marginTop + (y * (self.tileHeight + self.paddingY))

        tileRect = pg.Rect(tileX, tileY, self.tileWidth, self.tileHeight)

        currentTile = pg.Surface(tileRect.size, pg.SRCALPHA)

        currentTile.blit(self.tileset, (0, 0), tileRect)

        self.tiles[x].append(currentTile)

    self.setNamedTiles()
    self.setSequencedTiles()

  def setNamedTiles(self):
    if self.names is None: return None

    y = -1
    for row in self.names:
      y += 1
      x = -1
      for name in row:
        x += 1
        self.namedTiles[name] = self.tiles[x][y]

  def setSequencedTiles(self):
    if (self.names is None) or (self.sequences is None):
      return None

    for sequence in self.sequences:
      self.sequencedTiles[sequence] = []
      for tileName in self.sequences[sequence]:
        self.sequencedTiles[sequence].append(self.namedTiles[tileName])

  def getTile(self, identifier: tileIdentifierType) -> Optional[pg.Surface]:
    if isinstance(identifier, str):
      return self.namedTiles.get(identifier)
    elif isinstance(identifier, tuple):
      return self.tiles[identifier[0]][identifier[1]]
    elif isinstance(identifier, pg.Color):
      surface = pg.Surface((self.tileWidth, self.tileHeight))
      surface.fill(identifier)
      return surface

    return None
