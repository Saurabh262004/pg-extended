import pygame as pg
from pg_extended.Types import Background
from pg_extended.Util import Misc
from pg_extended.Core import DynamicValue, CallbackSet
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.Circle import Circle

class Slider():
  def __init__(self, orientation: str, section: Section, dragElement: Section | Circle, valueRange: list[float] | tuple[float], scrollSpeed: float, filledSliderBackground: Background, callback: CallbackSet = None, hoverToScroll: bool | None = True):
    self.orientation = orientation
    self.section = section
    self.valueRange = valueRange
    self.scrollSpeed = scrollSpeed
    self.dragElement = dragElement
    self.filledSliderBackground = filledSliderBackground
    self.callback = callback
    self.hoverToScroll = hoverToScroll

    self.value = self.valueRange[0]
    self.pressed = False
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

    if not self.orientation in ('vertical', 'horizontal'):
      raise ValueError('Slider orientation must be \'vertical\' or \'horizontal\'')

    if isinstance(self.dragElement, Section):
      self.dragElementType = 'section'
    else:
      self.dragElementType = 'circle'

    def getDragElementPos(axis: str, elementType: str, slider: Slider):
      returnValue = None
      axis = axis
      elementType = elementType
      slider = slider
      section = slider.section
      sliderValue = slider.value
      sliderValueRange = slider.valueRange
      dragElement = slider.dragElement

      if axis == 'x':
        if elementType == 'section':
          valueMappingCoords = (section.x, section.x + section.width - dragElement.width)
        else:
          valueMappingCoords = (section.x + dragElement.radius, section.x + section.width - dragElement.radius)

        returnValue = Misc.mapRange(sliderValue, sliderValueRange[0], sliderValueRange[1], valueMappingCoords[0], valueMappingCoords[1])
      else:
        if elementType == 'section':
          valueMappingCoords = (section.y, section.y + section.height - dragElement.height)
        else:
          valueMappingCoords = (section.y + dragElement.radius, section.y + section.height - dragElement.radius)

        returnValue = Misc.mapRange(sliderValue, sliderValueRange[0], sliderValueRange[1], valueMappingCoords[0], valueMappingCoords[1])

      if returnValue < valueMappingCoords[0]: return valueMappingCoords[0]
      elif returnValue > valueMappingCoords[1]: return valueMappingCoords[1]
      else: return returnValue

    if self.dragElementType == 'circle':
      if self.orientation == 'horizontal':
        self.dragElement.dimensions['x'] = DynamicValue(
          getDragElementPos,
          args={'axis': 'x', 'elementType': 'circle', 'slider': self}
        )

        self.dragElement.dimensions['y'] = DynamicValue(
          lambda section: section.y + (section.height / 2),
          args={'section': self.section}
        )

      else:
        self.dragElement.dimensions['x'] = DynamicValue(
          lambda section: section.x + (section.width / 2),
          args={'section': self.section}
        )

        self.dragElement.dimensions['y'] = DynamicValue(
          getDragElementPos,
          args={'axis': 'y', 'elementType': 'circle', 'slider': self}
        )

    else:
      if self.orientation == 'horizontal':
        self.dragElement.dimensions['x'] = DynamicValue(
          getDragElementPos,
          args={'axis': 'x', 'elementType': 'section', 'slider': self}
        )

        self.dragElement.dimensions['y'] = DynamicValue(
          lambda section, dragElement: section.y + ((section.height - dragElement.height) / 2),
          args={'section': self.section, 'dragElement': self.dragElement}
        )

      else:
        self.dragElement.dimensions['x'] = DynamicValue(
          lambda section, dragElement: section.x + ((section.width - dragElement.width) / 2),
          args={'section': self.section, 'dragElement': self.dragElement}
        )

        self.dragElement.dimensions['y'] = DynamicValue(
          getDragElementPos,
          args={'axis': 'y', 'elementType': 'section', 'slider': self}
        )

    if self.dragElementType == 'section':
      if self.orientation == 'horizontal':
        self.mapPosition = DynamicValue(
          lambda element: element.x + (element.width / 2),
          args={'element': self.dragElement}
        )

      else:
        self.mapPosition = DynamicValue(
          lambda element: element.y + (element.height / 2),
          args={'element': self.dragElement}
        )

    else:
      if self.orientation == 'horizontal':
        self.mapPosition = self.dragElement.dimensions['x']
      else:
        self.mapPosition = self.dragElement.dimensions['y']

    filledSliderWidth = None
    filledSliderHeight = None

    if self.orientation == 'horizontal':
      filledSliderWidth = DynamicValue(
        lambda mapPosition, section: max(0, mapPosition.value - section.x),
        args={'mapPosition': self.mapPosition, 'section': self.section}
      )

      filledSliderHeight = self.section.dimensions['height']
    else:
      filledSliderWidth = self.section.dimensions['width']

      filledSliderHeight = DynamicValue(
        lambda mapPosition, section: max(0, mapPosition.value - section.y),
        args={'mapPosition': self.mapPosition, 'section': self.section}
      )

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

    self.value = Misc.mapRange(relativePos, start, end, self.valueRange[0], self.valueRange[1])

    self.dragElement.update()
    self.mapPosition.resolveValue()
    self.filledSlider.update()

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    self.section.draw(surface)
    self.filledSlider.draw(surface)
    self.dragElement.draw(surface)

  def handleCallback(self, trigger):
    if self.callback is not None:
      self.callback.call(trigger, {'value': self.value})

  def checkEvent(self, event: pg.Event) -> bool:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(pg.mouse.get_pos()):
      self.pressed = True

      self.updateValue()

      self.handleCallback('mouseDown')

    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
      if self.pressed:
        self.pressed = False

        self.handleCallback('mouseUp')

        return True

      return False

    if self.pressed and event.type == pg.MOUSEMOTION:
      self.updateValue()

      self.handleCallback('mouseDrag')

      return True

    if event.type == pg.MOUSEWHEEL:
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

          self.handleCallback('scroll')

          return True

        return False

      return False

    return False
