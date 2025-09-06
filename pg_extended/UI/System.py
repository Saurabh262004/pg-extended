from typing import Dict, Iterable, Union
import pygame as pg
from pg_extended.UI.helpers import allIn
from pg_extended.UI.Elements import *

elementType = Union[Section, Circle, TextBox, Button, Toggle, Slider, TextInput]

'''
System is a class that represents a collection of UI elements and manages their processes, such as drawing, updating and event handling.

Parameters:
- [Optional] surface:       A pygame surface to draw the elements on. If not provided, the system will be locked by default.
- [Optional] preLoadState:  Whether the system should be locked in a pre-loaded state (default is False).
-                           If True, the system will not be able to draw or update until it is initiated with a surface.

Usable methods:
- addElement:    Adds a new UI element to the system.
- removeElement: Removes an existing UI element from the system.
- draw:          Draws the specified UI elements on the surface.
- update:        Updates the specified UI elements.
- handleEvents:  Handles mouse events and updates the state of buttons and toggles.
- initiate:      Initiates the system with a surface, unlocking it for drawing and updating.
'''
class System:
  def __init__(self, surface: pg.Surface = None, preLoadState: bool = False):
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
    self.textInputs: Dict[str, TextInput] = {}

    self.firstDraw = True

  def addElement(self, element: elementType, elementID: str):
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
    elif isinstance(element, TextInput):
      self.textInputs[elementID] = element

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
    elif isinstance(element, TextInput):
      del self.textInputs[elementID]

    del self.elements[elementID]

    return True

  def __validateIDs(self, elementIDs: Iterable = None) -> Union[Iterable, None, dict]:
    if elementIDs == None:
      return self.elements

    if not allIn(elementIDs, self.elements):
      print('The given iterable contains id(s) that do not exist in this system, please enter a valid iterable')
      return None

    return elementIDs

  def draw(self, elementIDs: Iterable = None):
    if self.locked:
      print('System is currently locked')
      return None

    idList = self.__validateIDs(elementIDs)

    if not idList == None:
      for elementID in idList:
        if self.elements[elementID].active and self.elements[elementID].activeDraw:
          self.elements[elementID].draw(self.surface)

    self.firstDraw = False

  def update(self, elementIDs: Iterable[str] = None):
    if self.locked:
      print('System is currently locked')
      return None

    idList = self.__validateIDs(elementIDs)

    if not idList == None:
      for elementID in idList:
        element = self.elements[elementID]

        if element.lazyUpdateOverride or (not element.lazyUpdate and element.active):
          element.update()

  def lazyUpdate(self, elementIDs: Iterable[str] = None):
    if self.locked:
      print('System is currently locked')
      return None

    idList = self.__validateIDs(elementIDs)

    if not idList == None:
      for elementID in idList:
        if self.elements[elementID].active:
          self.elements[elementID].update()

  def handleEvents(self, event: pg.Event) -> Union[str, None]:
    if self.locked:
      print('System is currently locked')
      return None

    mousePos = pg.mouse.get_pos()

    changeCursor = None
    for buttonID in self.buttons:
      if self.buttons[buttonID].active:
        self.buttons[buttonID].checkEvent(event)

        if not changeCursor and self.buttons[buttonID].activeEvents:
          if self.buttons[buttonID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

    for toggleID in self.toggles:
      if self.toggles[toggleID].active:
        self.toggles[toggleID].checkEvent(event)

        if not changeCursor and self.toggles[toggleID].activeEvents:
          if self.toggles[toggleID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

    for sliderID in self.sliders:
      if self.sliders[sliderID].active:
        self.sliders[sliderID].checkEvent(event)

        if not changeCursor and self.sliders[sliderID].activeEvents:
          if self.sliders[sliderID].section.rect.collidepoint(mousePos):
            changeCursor = 'hand'

    for textInputID in self.textInputs:
      if self.textInputs[textInputID].active:
        self.textInputs[textInputID].checkEvent(event)

        if not changeCursor and self.textInputs[textInputID].activeEvents:
          if self.textInputs[textInputID].section.rect.collidepoint(mousePos):
            changeCursor = 'ibeam'

    return 'arrow' if changeCursor is None else changeCursor

  def initiate(self, surface: pg.Surface):
    self.surface = surface

    self.locked = False
