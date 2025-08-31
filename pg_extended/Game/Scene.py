from typing import Union, Dict
import pygame as pg
from pg_extended.Game.Elements import *

elementType = Union[TextureAtlas, SpriteAnimation, Level, Player]

class Scene:
  def __init__(self):
    self.locked = True
    self.surface: pg.Surface = None

    self.elements: Dict[str, elementType] = {}
    self.textureAtlases: Dict[str, TextureAtlas] = {}
    self.spriteAnimations: Dict[str, SpriteAnimation] = {}
    self.levels: Dict[str, Level] = {}
    self.activeLevel: Level = None
    self.players: Dict[str, Player] = {}

  def addElement(self, element: elementType, elementID: str):
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
