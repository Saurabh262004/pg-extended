from typing import Union, Dict
import pygame as pg
from pg_extended.Game.Elements import *

elementType = Union[Level, Entity, Player]

class Scene:
  def __init__(self, surface: pg.Surface = None, preLoadState: bool = False):
    self.locked = preLoadState

    if not self.locked:
      if not surface:
        self.locked = True
        print('No surface provided, the scene is locked by default.\nIt can be initiated manually by providing a surface')
      else:
        self.surface = surface

    self.elements: Dict[str, elementType] = {}
    self.circles: Dict[str, Level] = {}
    self.textBoxes: Dict[str, Entity] = {}
    self.buttons: Dict[str, Player] = {}

  def lazyUpdate(self):
    pass

  def update(self):
    pass

  def handleEvents(self, event: pg.Event) -> str:
    pass

  def draw(self, surface: pg.Surface):
    pass

  def initiate(self, surface: pg.Surface):
    self.surface = surface
    
    for level in self.levels:
      level.initiate()

    self.locked = False
