from typing import Union, Dict, Optional, Iterable
import pygame as pg
from pg_extended.Game.Elements import *

elementType = Union[Level, Entity, Player]

class Scene:
  def __init__(self, cameraX: Union[int, float], cameraY: Union[int, float]):
    self.cameraX = cameraX
    self.cameraY = cameraY

    self.locked = True
    self.surface: pg.Surface = None

    self.elements: Dict[str, elementType] = {}
    self.textureAtlases: Dict[str, TextureAtlas] = {}
    self.levels: Dict[str, Level] = {}
    self.activeLevels: Dict[str, Level] = {}
    self.entities: Dict[str, Entity] = {}
    self.players: Dict[str, Player] = {}

  def addElement(self, element: elementType, elementID: str):
    if elementID in self.elements:
      raise ValueError(f'An element with ID: {elementID} already exists, please enter a unique ID.')

    self.elements[elementID] = element

    if isinstance(element, TextureAtlas):
      self.textureAtlases[elementID] = element
    elif isinstance(element, Level):
      self.levels[elementID] = element
    elif isinstance(element, Entity):
      self.entities[elementID] = element
    elif isinstance(element, Player):
      self.players[elementID] = element

  def lazyUpdate(self):
    pass

  def update(self):
    pass

  def handleEvents(self, event: pg.Event):
    pass

  def draw(self):
    if self.locked: return None

    for level in self.activeLevels.values():
      level.draw(self.surface, (self.cameraX, self.cameraY))

  def activateLevels(self, levelNames: Iterable[str]):
    for levelName in levelNames:
      if levelName in self.levels:
        self.activeLevels[levelName] = self.levels[levelName]

  def deactivateLevels(self, levelNames: Iterable[str]):
    for levelName in levelNames:
      if levelName in self.activeLevels:
        del self.activeLevels[levelName]

  def initiate(self, surface: pg.Surface):
    self.surface = surface

    for atlas in self.textureAtlases.values():
      atlas.generateTiles()

    levelInitializationSuccess = [level.initiate() for level in self.levels.values()]

    if all(levelInitializationSuccess):
      self.locked = False
