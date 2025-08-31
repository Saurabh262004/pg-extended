from typing import Union, Iterable
import pygame as pg

tileIdentifierType = Union[tuple[int, int], str, tuple[int, int, int], tuple[int, int, int, int], pg.Color]

class SpriteAnimation:
  def __init__(self, animation: Iterable[tuple[str, tileIdentifierType]]):
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
