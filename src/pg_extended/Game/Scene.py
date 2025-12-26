import pygame as pg
from pg_extended.Game.Elements import *

class Scene:
  def __init__(self):
    self.locked = True
    self.surface: pg.Surface = None

    self.elements: dict[str, GameElement] = {}
    self.textureAtlases: dict[str, TextureAtlas] = {}
    self.spriteAnimations: dict[str, SpriteAnimation] = {}
    self.levels: dict[str, Level] = {}
    self.activeLevel: Level = None
    self.players: dict[str, Player] = {}

  def addElement(self, element: GameElement, elementID: str):
    if elementID in self.elements:
      raise ValueError(f'An element with ID: {elementID} already exists, please enter a unique ID.')

    self.elements[elementID] = element

    if isinstance(element, TextureAtlas):
      self.textureAtlases[elementID] = element
    elif isinstance(element, SpriteAnimation):
      self.spriteAnimations[elementID] = element
    elif isinstance(element, Level):
      self.levels[elementID] = element
    elif isinstance(element, Player):
      self.players[elementID] = element

  def lazyUpdate(self):
    pass

  def update(self):
    if self.locked:
      print('Scene is currently locked')
      return None

    for level in self.levels.values():
      for entity in level.entities:
        if entity.animating:
          entity.update()

  def handleEvents(self, event: pg.Event):
    pass

  def activateLevel(self, levelID: str):
    if not levelID in self.levels:
      print(f'Level with ID {levelID} does not exist, plase enter an existing level ID')
      return None

    self.activeLevel = self.levels[levelID]

  def deactivateLevel(self):
    self.activeLevel = None

  def initiate(self, surface: pg.Surface):
    self.surface = surface

    for atlas in self.textureAtlases.values():
      atlas.generateTiles()

    for spriteAnimation in self.spriteAnimations.values():
      spriteAnimation.initiate(self)

    levelInitializationSuccess = [level.initiate(self) for level in self.levels.values()]

    if all(levelInitializationSuccess):
      self.locked = False
