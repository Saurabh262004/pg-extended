from typing import Optional, Dict, Iterable, Union
import pygame as pg
from ..helpers import allIn
from .Section import Section
from .Circle import Circle
from .TextBox import TextBox
from .Button import Button
from .Toggle import Toggle
from .Slider import Slider

elementType = Union[Section, Circle, Button, Toggle, Slider]

class System:
  def __init__(self, surface: Optional[pg.surface.Surface] = None, preLoadState: Optional[bool] = False):
    self.locked = preLoadState

    if not self.locked:
      if not surface:
        self.locked = True
        print('No surface provided, the system is locked by default.\nIt can be initiated manually by providing a surface')
      else:
        self.surface = surface

    self.elements: Dict[str, elementType] = {}
    self.sections: Dict[str, Section] = {}
    self.circles: Dict[str, Circle] = {}
    self.textBoxes: Dict[str, TextBox] = {}
    self.buttons: Dict[str, Button] = {}
    self.toggles: Dict[str, Toggle] = {}
    self.sliders: Dict[str, Slider] = {}

    self.firstDraw = True

  def addElement(self, element: elementType, elementID: str) -> bool:
    if elementID in self.elements:
      raise ValueError(f'An element with id: {elementID} already exists, please enter a unique id.')

    self.elements[elementID] = element

    if isinstance(element, Section):
      self.sections[elementID] = element
    elif isinstance(element, Circle):
      self.circles[elementID] = element
    elif isinstance(element, TextBox):
      self.textBoxes[elementID] = element
    elif isinstance(element, Button):
      self.buttons[elementID] = element
    elif isinstance(element, Toggle):
      self.toggles[elementID] = element
    elif isinstance(element, Slider):
      self.sliders[elementID] = element

    return True

  def removeElement(self, elementID: str) -> bool:
    if not elementID in self.elements:
      raise ValueError(f'An element with id: {elementID} does not exist, please enter a valid id.')

    element = self.elements[elementID]

    if isinstance(element, Section):
      del self.sections[elementID]
    elif isinstance(element, Circle):
      del self.circles[elementID]
    elif isinstance(element, TextBox):
      del self.textBoxes[elementID]
    elif isinstance(element, Button):
      del self.buttons[elementID]
    elif isinstance(element, Toggle):
      del self.toggles[elementID]
    elif isinstance(element, Slider):
      del self.sliders[elementID]

    del self.elements[elementID]

    return True

  def __validateIDs(self, elementIDs: Optional[Iterable] = None) -> Union[Iterable, None, dict]:
    if elementIDs == None:
      return self.elements

    if not allIn(elementIDs, self.elements):
      print('The given iterable contains id(s) that do not exist in this system, please enter a valid iterable')
      return None

    return elementIDs

  def draw(self, elementIDs: Optional[Iterable] = None):
    if self.locked:
      print('System is currently locked')
      return None

    idList = self.__validateIDs(elementIDs)

    if not idList == None:
      for elementID in idList:
        if self.elements[elementID].active and self.elements[elementID].activeDraw:
          self.elements[elementID].draw(self.surface)

    self.firstDraw = False

  def update(self, elementIDs: Optional[Iterable] = None):
    if self.locked:
      print('System is currently locked')
      return None

    idList = self.__validateIDs(elementIDs)

    if not idList == None:
      for elementID in idList:
        if self.elements[elementID].active:
          self.elements[elementID].update()

  def handleEvents(self, event: pg.event.Event) -> Union[str, None]:
    if self.locked:
      print('System is currently locked')
      return None

    mousePos = pg.mouse.get_pos()

    changeCursor = None
    for buttonID in self.buttons:
      if self.buttons[buttonID].active:
        if not changeCursor and self.buttons[buttonID].activeEvents:
          if self.buttons[buttonID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

        self.buttons[buttonID].checkEvent(event)

    for toggleID in self.toggles:
      if self.toggles[toggleID].active:
        if not changeCursor and self.toggles[toggleID].activeEvents:
          if self.toggles[toggleID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

        self.toggles[toggleID].checkEvent(event)

    for sliderID in self.sliders:
      if self.sliders[sliderID].active:
        if not changeCursor and self.sliders[sliderID].activeEvents:
          if self.sliders[sliderID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

        self.sliders[sliderID].checkEvent(event)

    return changeCursor

  def initiate(self, surface: pg.surface.Surface):
    self.surface = surface

    self.locked = False
