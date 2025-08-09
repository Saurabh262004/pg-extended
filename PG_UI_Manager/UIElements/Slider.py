from typing import Optional, Union, Iterable, Dict
import pygame as pg
from ..helpers import mapRange
from .Core import DynamicValue
from .Section import Section
from .Circle import Circle

numType = Union[int, float]
backgroundType = Union[pg.Color, pg.Surface]

SLIDER_ONCHANGE_KEYS = ('callable', 'params', 'sendValue')

'''
Slider is a class that represents a slider UI element.

Parameters:
- [required] orientation:             The orientation of the slider ('vertical' or 'horizontal').
- [required] section:                 A Section object that defines the slider's base model (position and size).
- [required] dragElement:             A Section or Circle object that represents the draggable element of the slider.
- [required] valueRange:              A tuple or list containing the minimum and maximum values of the slider.
- [required] scrollSpeed:             The speed at which the slider value changes when scrolling (pass a negative value for reverse scrolling).
- [required] filledSliderBackground:  The background color or surface of the filled part of the slider.
- [Optional] onChangeInfo:            A dictionary containing information for the onChange callback function.
-                                     structure of the dictionary:
-                                     {
-                                       'callable':  Callable function to be called when the slider value changes.
-                                       'params':    Parameters to pass to the callable function (default is None).
-                                       'sendValue': Whether to send the slider value as a parameter to the callable function.
-                                     }
- [Optional] hoverToScroll:           Whether the slider should only scroll when the mouse is hovered over it (default is True).

Usable methods:
- update:      Updates the slider's dimensions and background based on the provided Section object.
- draw:        Draws the slider on the provided surface.
- checkEvent:  Checks for mouse button events and updates the slider value accordingly.
- updateValue: Updates the slider value based on the current mouse position.
- callback:    Calls the onChangeInfo callable with the current slider value and parameters.
'''
class Slider():
  def __init__(self, orientation: str, section: Section, dragElement: Union[Section, Circle], valueRange: Iterable[numType], scrollSpeed: numType, filledSliderBackground: backgroundType, onChangeInfo: Optional[Dict] = None, hoverToScroll: Optional[bool] = True):
    self.orientation = orientation
    self.section = section
    self.valueRange = valueRange
    self.scrollSpeed = scrollSpeed
    self.dragElement = dragElement
    self.filledSliderBackground = filledSliderBackground
    self.onChangeInfo = onChangeInfo
    self.hoverToScroll = hoverToScroll
    self.pressed = False
    self.value = self.valueRange[0]
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True

    if not self.orientation in ('vertical', 'horizontal'):
      raise ValueError('Slider orientation must be \'vertical\' or \'horizontal\'')

    if not self.onChangeInfo is None:
      for k in SLIDER_ONCHANGE_KEYS:
        if not k in self.onChangeInfo:
          raise ValueError(f'onChangeInfo must have these keys: {SLIDER_ONCHANGE_KEYS}')

    if isinstance(self.dragElement, Section):
      self.dragElementType = 'section'
    else:
      self.dragElementType = 'circle'

    def getDragElementPos(params):
      returnValue = None
      axis: str = params[0]
      elementType: str = params[1]
      slider: Slider = params[2]
      section = slider.section
      sliderValue = slider.value
      sliderValueRange = slider.valueRange
      dragElement = slider.dragElement

      if axis == 'x':
        if elementType == 'section':
          valueMappingCoords = (section.x, section.x + section.width - dragElement.width)
        else:
          valueMappingCoords = (section.x + dragElement.radius, section.x + section.width - dragElement.radius)

        returnValue = mapRange(sliderValue, sliderValueRange[0], sliderValueRange[1], valueMappingCoords[0], valueMappingCoords[1])
      else:
        if elementType == 'section':
          valueMappingCoords = (section.y, section.y + section.height - dragElement.height)
        else:
          valueMappingCoords = (section.y + dragElement.radius, section.y + section.height - dragElement.radius)

        returnValue = mapRange(sliderValue, sliderValueRange[0], sliderValueRange[1], valueMappingCoords[0], valueMappingCoords[1])

      if returnValue < valueMappingCoords[0]: return valueMappingCoords[0]
      elif returnValue > valueMappingCoords[1]: return valueMappingCoords[1]
      else: return returnValue

    if self.dragElementType == 'circle':
      if self.orientation == 'horizontal':
        self.dragElement.dimensions['x'] = DynamicValue('callable', getDragElementPos, ('x', 'circle', self))
        self.dragElement.dimensions['y'] = DynamicValue('callable', lambda section: section.y + (section.height / 2), self.section)
      else:
        self.dragElement.dimensions['x'] = DynamicValue('callable', lambda section: section.x + (section.width / 2), self.section)
        self.dragElement.dimensions['y'] = DynamicValue('callable', getDragElementPos, ('y', 'circle', self))
    else:
      if self.orientation == 'horizontal':
        self.dragElement.dimensions['x'] = DynamicValue('callable', getDragElementPos, ('x', 'section', self))
        self.dragElement.dimensions['y'] = DynamicValue('callable', lambda params: params[0].y + ((params[0].height - params[1].height) / 2), (self.section, self.dragElement))
      else:
        self.dragElement.dimensions['x'] = DynamicValue('callable', lambda params: params[0].x + ((params[0].width - params[1].width) / 2), (self.section, self.dragElement))
        self.dragElement.dimensions['y'] = DynamicValue('callable', getDragElementPos, ('y', 'section', self))

    if self.dragElementType == 'section':
      if self.orientation == 'horizontal':
        self.mapPosition = DynamicValue('callable', lambda element: element.x + (element.width / 2), self.dragElement)
      else:
        self.mapPosition = DynamicValue('callable', lambda element: element.y + (element.height / 2), self.dragElement)
    else:
      if self.orientation == 'horizontal':
        self.mapPosition = self.dragElement.dimensions['x']
      else:
        self.mapPosition = self.dragElement.dimensions['y']

    filledSliderWidth = None
    filledSliderHeight = None
    if self.orientation == 'horizontal':
      filledSliderWidth = DynamicValue('callable', lambda params: params[0].value - params[1].x, (self.mapPosition, self.section))
      filledSliderHeight = self.section.dimensions['height']
    else:
      filledSliderWidth = self.section.dimensions['width']
      filledSliderHeight = DynamicValue('callable', lambda params: params[0].value - params[1].y, (self.mapPosition, self.section))

    self.filledSlider = Section(
      {
        'x': self.section.dimensions['x'],
        'y': self.section.dimensions['y'],
        'width': filledSliderWidth,
        'height': filledSliderHeight
      }, self.filledSliderBackground, self.section.borderRadius
    )

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()
    self.dragElement.update()
    self.mapPosition.resolveValue()
    self.filledSlider.update()

  def updateValue(self):
    if not self.active:
      return None

    mousePos = pg.mouse.get_pos()

    if self.orientation == 'horizontal':
      relativePos = mousePos[0]
      start = self.section.x
      end = self.section.x + self.section.width
    else:
      relativePos = mousePos[1]
      start = self.section.y
      end = self.section.y + self.section.height

    if relativePos < start:
      relativePos = start
    elif relativePos > end:
      relativePos = end

    self.value = mapRange(relativePos, start, end, self.valueRange[0], self.valueRange[1])

    self.dragElement.update()
    self.mapPosition.resolveValue()
    self.filledSlider.update()

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    self.section.draw(surface)
    self.filledSlider.draw(surface)
    self.dragElement.draw(surface)

  def callback(self):
    if not self.active:
      return None

    if not self.onChangeInfo is None:
      if not self.onChangeInfo['params'] is None:
        if self.onChangeInfo['sendValue']:
          self.onChangeInfo['callable'](self.value, self.onChangeInfo['params'])
        else:
          self.onChangeInfo['callable'](self.onChangeInfo['params'])
      else:
        if self.onChangeInfo['sendValue']:
          self.onChangeInfo['callable'](self.value)
        else:
          self.onChangeInfo['callable']()

  def checkEvent(self, event: pg.event.Event) -> bool:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(pg.mouse.get_pos()):
      self.pressed = True
    elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
      if self.pressed:
        self.pressed = False
        self.callback()
      else:
        return False
    elif event.type == pg.MOUSEWHEEL:
      self.pressed = False
      scroll = False
      updatedValue = self.value

      if self.hoverToScroll:
        if self.section.rect.collidepoint(pg.mouse.get_pos()):
          scroll = True
      else:
        scroll = True

      if scroll:
        if event.x > 0 or event.y > 0:
          updatedValue += self.scrollSpeed
        elif event.x < 0 or event.y < 0:
          updatedValue -= self.scrollSpeed

        if updatedValue < min(self.valueRange[0], self.valueRange[1]):
          updatedValue = min(self.valueRange[0], self.valueRange[1])
        elif updatedValue > max(self.valueRange[0], self.valueRange[1]):
          updatedValue = max(self.valueRange[0], self.valueRange[1])

        if self.value != updatedValue:
          self.value = updatedValue

          self.update()
          self.callback()
          return True
        return False
      return False

    if self.pressed:
      self.updateValue()
      return True

    return False
