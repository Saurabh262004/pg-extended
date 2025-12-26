from json import load
import pygame as pg
from pg_extended.Types import TileIdentifier

class TextureAtlas:
  def __init__(self, tilesetURL: str, tileWidth: int, tileHeight: int, paddingX: int = 0, paddingY: int = 0, tilestOffsetX: int = 0, tilestOffsetY: int = 0, namesJsonURL: str = None, sequences: dict[str, list[TileIdentifier] | tuple[TileIdentifier]] = None):
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight
    self.paddingX = paddingX
    self.paddingY = paddingY
    self.tilestOffsetX = tilestOffsetX
    self.tilestOffsetY = tilestOffsetY
    self.namesJsonURL = namesJsonURL

    if namesJsonURL is not None:
      try:
        with open(namesJsonURL, 'r') as f:
          self.names = load(f)['names']
      except:
        self.names = None
    else:
      self.names = None

    self.sequences = sequences

    self.tileset = pg.image.load(tilesetURL)

    self.tilesX = (self.tileset.get_width() - tilestOffsetX) // (tileWidth + paddingX)
    self.tilesY = (self.tileset.get_height() - tilestOffsetY) // (tileHeight + paddingY)

    self.tiles = []
    self.namedTiles = {}
    self.sequencedTiles = {}

  def generateTiles(self):
    self.tileset.convert_alpha()

    for x in range(self.tilesX):
      self.tiles.append([])
      for y in range(self.tilesY):
        tileX = self.tilestOffsetX + (x * (self.tileWidth + self.paddingX))
        tileY = self.tilestOffsetY + (y * (self.tileHeight + self.paddingY))

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
    if self.sequences is None: return None

    for sequence in self.sequences:
      self.sequencedTiles[sequence] = []
      for tileIdentifier in self.sequences[sequence]:
        if isinstance(tileIdentifier, str):
          self.sequencedTiles[sequence].append(self.namedTiles[tileIdentifier])
        elif isinstance(tileIdentifier, tuple):
          if len(tileIdentifier) == 2:
            self.sequencedTiles[sequence].append(self.tiles[tileIdentifier[0]][tileIdentifier[1]])
          elif len(tileIdentifier) == 3 or len(tileIdentifier) == 4:
            surface = pg.Surface((self.tileWidth, self.tileHeight), pg.SRCALPHA)
            surface.fill(tileIdentifier)
            self.sequencedTiles[sequence].append(surface)
        elif isinstance(tileIdentifier, pg.Color):
          surface = pg.Surface((self.tileWidth, self.tileHeight), pg.SRCALPHA)
          surface.fill(tileIdentifier)
          self.sequencedTiles[sequence].append(surface)

  def getTile(self, identifier: TileIdentifier) -> pg.Surface | None:
    if isinstance(identifier, str):
      return self.namedTiles.get(identifier)
    elif isinstance(identifier, tuple):
      if len(identifier) == 2:
        return self.tiles[identifier[0]][identifier[1]]
      elif len(identifier) == 3 or len(identifier) == 4:
        surface = pg.Surface((self.tileWidth, self.tileHeight), pg.SRCALPHA)
        surface.fill(identifier)
        return surface
    elif isinstance(identifier, pg.Color):
      surface = pg.Surface((self.tileWidth, self.tileHeight), pg.SRCALPHA)
      surface.fill(identifier)
      return surface

    return None
