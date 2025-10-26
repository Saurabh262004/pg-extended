from typing import Iterable
import pygame as pg
from pg_extended.Types import TileIdentifier

class SpriteAnimation:
  def __init__(self, animation: Iterable[tuple[str, TileIdentifier]]):
    self.animationRaw = animation

    self.scene: 'Scene' = None # type: ignore
    self.sprites: Iterable[pg.Surface] = []

  def initiate(self, scene: 'Scene'): # type: ignore
    self.scene = scene

    for tileDetails in self.animationRaw:
      atlasID, tileID = tileDetails

      sprite = self.scene.textureAtlases[atlasID].getTile(tileID)

      if sprite is None: continue

      self.sprites.append(sprite)
