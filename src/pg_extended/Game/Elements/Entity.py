from math import floor
import pygame as pg
from pg_extended.Types import TileIdentifier
from pg_extended.Core import DynamicValue, AnimatedValue
from pg_extended.Game.Elements.SpriteAnimation import SpriteAnimation
from pg_extended.Game.Elements import Level

class Entity:
  def __init__(self, name: str, x: float, y: float, width: float, height: float, defaultSpriteDetails: tuple[str, TileIdentifier]):
    self.name = name
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.defaultSpriteAtlasID = defaultSpriteDetails[0]
    self.defaultSpriteID = defaultSpriteDetails[1]

    self.locked: bool = True
    self.animating: bool = False
    self.xPX: float = 0.0
    self.yPX: float = 0.0
    self.widthPX: float = 0.0
    self.heightPX: float = 0.0
    self.animationFrames: int = 1
    self.animations: list[dict[str, tuple[float, SpriteAnimation]]] = []
    self.currentAnimation: SpriteAnimation = None
    self.defaultSprite: pg.Surface = None
    self.sprite: pg.Surface = None

    self.animationInterpolator: AnimatedValue = AnimatedValue(
      [DynamicValue(0), DynamicValue(self, 'animationFrames')],
      1,
      'start',
      'linear',
      self.terminateAnimation
    )

  def initiate(self, level: Level, scene: 'Scene'): # type: ignore
    self.level = level
    self.xPX = self.x * level.tileWidth
    self.yPX = self.y * level.tileHeight
    self.widthPX = self.width * level.tileWidth
    self.heightPX = self.height * level.tileHeight
    self.defaultSprite = scene.textureAtlases[self.defaultSpriteAtlasID].getTile(self.defaultSpriteID)
    self.sprite = self.defaultSprite
    self.locked = False

  def update(self):
    if self.locked: return

    if self.animating:
      self.animationInterpolator.resolveValue()

      spriteIndex = floor(self.animationInterpolator.value)

      if spriteIndex >= self.animationFrames:
        spriteIndex = self.animationFrames - 1
      elif spriteIndex < 0:
        spriteIndex = 0

      self.sprite = self.currentAnimation.sprites[spriteIndex]
    else:
      self.sprite = self.defaultSprite

  def setAnimations(self, animations: dict[str, SpriteAnimation]):
    self.animations = animations

  def triggerAnimation(self, animationName: str, duration: float, reverse: bool = False, repeats: int = 0, alternate: bool = False):
    self.currentAnimation = self.animations[animationName]
    self.animationFrames = len(self.currentAnimation.sprites)
    self.animating = True
    self.animationInterpolator.duration = duration
    self.animationInterpolator.trigger(reverse, repeats, alternate)

  def terminateAnimation(self):
    self.animating = False
    self.animationInterpolator.terminate()
