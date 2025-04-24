# a module that helps render stuff on screen with pygame
# reusing code is not something I know
from math import sqrt
import pygame as pg
from modules.misc.helpers import mapRange, allIn, squish, fit, fill
from typing import Union, Optional, Callable, Dict, Iterable, Any

numType = Union[int, float]
containerType = Union['Section', pg.Rect]
backgroundType = Union[pg.Color, pg.surface.Surface]
elementType = Union['Section', 'Circle', 'Button', 'Toggle', 'Slider']

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')
DIMENSION_REFERENCE_TYPES = ('number', 'percent', 'dictNum', 'classNum', 'dictPer', 'classPer', 'customCallable')
SLIDER_ONCHANGE_KEYS = ('callable', 'params', 'sendValue')

class DynamicValue:
  def __init__(self, referenceType: str, reference: Union[Callable, numType, Dict[str, numType], object], callableParameters: Optional[Any] = None, dictKey: Optional[str] = None, classAttr: Optional[str] = None, percent: Optional[numType] = None):
    self.referenceType = referenceType
    self.reference = reference
    self.callableParameters = callableParameters
    self.dictKey = dictKey
    self.classAttr = classAttr
    self.percent = percent
    self.value = None
    self.resolveValue: Callable

    if not self.referenceType in DIMENSION_REFERENCE_TYPES:
      raise ValueError(f'Invalid dimType value received, value must be one of the following: {DIMENSION_REFERENCE_TYPES}')

    if (self.referenceType == 'customCallable') and not callable(self.reference):
      raise ValueError('If referenceType is custumCallable then reference must be callable')

    if (self.referenceType == 'dictNum' or self.referenceType == 'dictPer') and not (isinstance(self.reference, dict)):
      raise ValueError('If referenceType is dictNum or dictPer then given reference must be a dict object')

    if (self.referenceType == 'dictNum' or self.referenceType == 'dictPer') and (self.dictKey is None):
      raise ValueError('If referenceType is dictNum or dictPer then dictKey must be defined')

    if (self.referenceType == 'classNum' or self.referenceType == 'classPer') and not (isinstance(self.reference, object)):
      raise ValueError('If referenceType is classNum or classPer then given reference must be an object')

    if (self.referenceType == 'classNum' or self.referenceType == 'classPer') and (self.classAttr is None):
      raise ValueError('If referenceType is classNum or classPer then classAttr must be defined')

    if (self.referenceType == 'percent' or self.referenceType == 'dictPer' or self.referenceType == 'classPer') and (self.percent is None):
      raise ValueError('If referenceType is percent, dictPer or classPer percent must be defined')

    if self.referenceType == 'number':
      self.resolveValue = self.__getByNumber
    elif self.referenceType == 'percent':
      self.resolveValue = self.__getByPercent
    elif self.referenceType == 'customCallable':
      self.resolveValue = self.__getByCustomCallable
    elif self.referenceType == 'dictNum':
      self.resolveValue = self.__getByDictNum
    elif self.referenceType == 'dictPer':
      self.resolveValue = self.__getByDictPer
    elif self.referenceType == 'classNum':
      self.resolveValue = self.__getByClassNum
    elif self.referenceType == 'classPer':
      self.resolveValue = self.__getByClassPer

    self.resolveValue()

  def __getByNumber(self):
    self.value = self.reference

  def __getByPercent(self):
    self.value = self.reference * (self.percent / 100)

  def __getByCustomCallable(self):
    if not self.callableParameters is None:
      self.value = self.reference(self.callableParameters)
    else:
      self.value = self.reference()

  def __getByDictNum(self):
    self.value = self.reference[self.dictKey]

  def __getByDictPer(self):
    self.value = self.reference[self.dictKey] * (self.percent / 100)

  def __getByClassNum(self):
    self.value = getattr(self.reference, self.classAttr, 0)

  def __getByClassPer(self):
    self.value = getattr(self.reference, self.classAttr, 0) * (self.percent / 100)

class Section:
  def __init__(self, dimensions: Dict['str', DynamicValue], background: backgroundType, borderRadius: Optional[numType] = 0, backgroundSizeType: Optional[str] = 'fit', backgroundSizePercent: Optional[int] = 100):
    self.dimensions = dimensions
    self.background = background
    self.drawImage = None
    self.rect = pg.Rect(0, 0, 0, 0)
    self.borderRadius = borderRadius
    self.backgroundSizeType = backgroundSizeType
    self.backgroundSizePercent = backgroundSizePercent
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True

    if len(self.dimensions) != 4:
      raise ValueError(f'dimensions must contain 4 Dimension objects, received: {len(self.dimensions)}')

    if not allIn(('x', 'y', 'width', 'height'), self.dimensions):
      raise ValueError('dimensions must contain all of the following keys: \'x\', \'y\', \'width\' \'height\'')

    if not self.backgroundSizeType in VALID_SIZE_TYPES:
      raise ValueError(f'Invalid \"backgroundSizeType\" value, must be one of the following values: {VALID_SIZE_TYPES}')

    self.x = self.dimensions['x'].value
    self.y = self.dimensions['y'].value
    self.width = self.dimensions['width'].value
    self.height = self.dimensions['height'].value

    self.update()

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    # This is really not ideal but I don't know what else I can do
    unstable = True
    totalIterations = 0
    maxIterations = len(self.dimensions)
    while unstable:
      if totalIterations > maxIterations:
        raise ValueError('Provided dimensions are referencing each other in a cyclic pattern, please provide valid dimenisons')

      for dim in self.dimensions:
        self.dimensions[dim].resolveValue()

      if (
        self.x == self.dimensions['x'].value and
        self.y == self.dimensions['y'].value and
        self.width == self.dimensions['width'].value and
        self.height == self.dimensions['height'].value
        ): unstable = False
      else:
        totalIterations += 1

      self.x = self.dimensions['x'].value
      self.y = self.dimensions['y'].value
      self.width = self.dimensions['width'].value
      self.height = self.dimensions['height'].value

    self.rect.update(self.x, self.y, self.width, self.height)

    if isinstance(self.background, pg.surface.Surface):
      if self.backgroundSizeType == 'fit':
        self.drawImage = fit(self.background, (self.width, self.height), self.backgroundSizePercent)
      elif self.backgroundSizeType == 'fill':
        self.drawImage = fill(self.background, (self.width, self.height), self.backgroundSizePercent)
      elif self.backgroundSizeType == 'squish':
        self.drawImage = squish(self.background, (self.width, self.height), self.backgroundSizePercent)
      elif not self.backgroundSizePercent == 100:
        self.drawImage = fit(self.background, (self.background.get_width(), self.background.get_height()), self.backgroundSizePercent)
      else:
        self.drawImage = self.background

      self.imageX = self.x + ((self.width - self.drawImage.get_width()) / 2)
      self.imageY = self.y + ((self.height - self.drawImage.get_height()) / 2)

  def draw(self, surface: pg.surface.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.surface.Surface):
      surface.blit(self.drawImage, (self.imageX, self.imageY))
    elif isinstance(self.background, pg.Color):
      pg.draw.rect(surface, self.background, self.rect, border_radius = self.borderRadius)

class Circle:
  def __init__(self, dimensions: Dict[str, DynamicValue], background: backgroundType, backgroundSizeType: Optional[str] = 'fit'):
    self.dimensions = dimensions
    self.background = background
    self.drawImage = None
    self.backgroundSizeType = backgroundSizeType
    self.sqrt2 = sqrt(2)
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True

    if len(self.dimensions) != 3:
      raise ValueError(f'dimensions must contain 4 Dimension objects, received: {len(self.dimensions)}')

    if not allIn(('x', 'y', 'radius'), self.dimensions):
      raise ValueError('dimensions must contain all of the following keys: \'x\', \'y\', \'radius\'')

    if not self.backgroundSizeType in VALID_SIZE_TYPES:
      raise ValueError(f'Invalid \"backgroundSizeType\" value, must be one of the following values: {VALID_SIZE_TYPES}')

    self.x = self.dimensions['x'].value
    self.y = self.dimensions['y'].value
    self.radius = self.dimensions['radius'].value

    self.update()

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    # Same as before... not ideal but I don't know what else I can do
    unstable = True
    totalIterations = 0
    maxIterations = len(self.dimensions)
    while unstable:
      if totalIterations > maxIterations:
        raise ValueError('Provided dimensions are referencing each other in a cyclic pattern, please provide valid dimenisons')

      for dim in self.dimensions:
        self.dimensions[dim].resolveValue()

      if (
        self.x == self.dimensions['x'].value and
        self.y == self.dimensions['y'].value and
        self.radius == self.dimensions['radius'].value
        ): unstable = False
      else:
        totalIterations += 1

      self.x = self.dimensions['x'].value
      self.y = self.dimensions['y'].value
      self.radius = self.dimensions['radius'].value

    if isinstance(self.background, pg.surface.Surface):
      if self.backgroundSizeType == 'fit':
        self.drawImage = fit(self.background, (self.radius * self.sqrt2, self.radius * self.sqrt2))
      elif self.backgroundSizeType == 'fill':
        self.drawImage = fill(self.background, (self.radius * 2, self.radius * 2))
      else:
        self.drawImage = squish(self.background, (self.radius * 2, self.radius * 2))

  def draw(self, surface: pg.surface.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.surface.Surface):
      surface.blit(self.drawImage, (self.x - (self.drawImage.get_width() / 2), self.y - (self.drawImage.get_height() / 2)))
    elif isinstance(self.background, pg.Color):
      pg.draw.circle(surface, self.background, (self.x, self.y), self.radius)

class TextBox:
  def __init__(self, section: Section, text: str, fontPath: str, textColor: pg.Color, drawSectionDefault: Optional[bool] = False, centerText: Optional[bool] = True):
    self.section = section
    self.text = text
    self.fontPath = fontPath
    self.textColor = textColor
    self.drawSectionDefault = drawSectionDefault
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.centerText = centerText

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    self.fontSize = max(10, int(self.section.height * .6))
    self.font = pg.font.SysFont(self.fontPath, self.fontSize)

    self.textSurface = self.font.render(self.text, True, self.textColor)
    if self.centerText:
      self.textRect = self.textSurface.get_rect(center=self.section.rect.center)
    else:
      self.textRect = self.textSurface.get_rect(midleft=self.section.rect.midleft)

  def draw(self, surface: pg.surface.Surface, drawSection: Optional[bool] = None):
    if not (self.active and self.activeDraw):
      return None

    if (drawSection is None and self.drawSectionDefault) or drawSection:
      self.section.draw(surface)

    surface.blit(self.textSurface, self.textRect)

class Button:
  def __init__(self, section: Section, pressedBackground: Optional[backgroundType] = None, borderColor: Optional[pg.Color] = None, borderColorPressed: Optional[pg.Color] = None, text: Optional[str] = None, fontPath: Optional[str] = None, textColor: Optional[pg.Color] = None, onClick: Optional[Callable] = None, onClickParams = None, border: Optional[int] = 0, onClickActuation: Optional[str] = 'buttonDown'):
    self.section = section
    self.onClick = onClick
    self.onClickParams = onClickParams
    self.onClickActuation = onClickActuation
    self.border = border
    self.pressed = False
    self.defaultBackground = section.background
    self.pressedBackground = pressedBackground
    self.borderColor = borderColor
    self.borderColorPressed = borderColorPressed
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True

    if self.border > 0:
      self.borderRect = pg.Rect(section.x - border, section.y - border, section.width + (border * 2), section.height + (border * 2))

    if text:
      self.textBox = TextBox(section, text, fontPath, textColor, False)
      self.hasText = True
    else:
      self.hasText = False

    if not onClickActuation in ('buttonDown', 'buttonUp'):
      raise ValueError('onClickActuation must be either \'buttonDown\' or \'buttonUp\'')

    self.update()

  def checkEvent(self, event: pg.event.Event) -> Optional[bool]:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(event.pos):
      self.pressed = True

      if self.pressedBackground:
        self.section.background = self.pressedBackground
        self.section.update()

      if self.onClick and self.onClickActuation == 'buttonDown':
        if self.onClickParams is None:
          self.onClick()
        else:
          self.onClick(self.onClickParams)

      return True
    elif event.type == pg.MOUSEBUTTONUP and self.pressed:
      self.pressed = False
      self.section.background = self.defaultBackground

      if self.onClick and self.onClickActuation == 'buttonUp':
        if self.onClickParams is None:
          self.onClick()
        else:
          self.onClick(self.onClickParams)
      
      self.section.update()

      return True
    return False

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    if not isinstance(self.section, pg.Rect):
      if self.hasText and self.activeDraw:
        try:
          self.textBox.update()
        except Exception as e:
          print(e)
      else:
        self.section.update()

    newX, newY = self.section.x - self.border, self.section.y - self.border
    newWidth, newHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    if self.border > 0:
      self.borderRect.update(newX, newY, newWidth, newHeight)

  def draw(self, surface: pg.surface.Surface):
    if not (self.active and self.activeDraw):
      return None

    if self.border > 0:
      if self.pressed:
        pg.draw.rect(surface, self.borderColorPressed, self.borderRect, border_radius = self.section.borderRadius)
      else:
        pg.draw.rect(surface, self.borderColor, self.borderRect, border_radius = self.section.borderRadius)

    self.section.draw(surface)

    if self.hasText:
      self.textBox.draw(surface)

class Toggle:
  def __init__(self, section: Section, indicatorColor: pg.Color, borderColor: pg.Color, borderColorToggled: pg.Color, onClick: Optional[Callable] = None, onClickParams = None, sendStateInfoOnClick: Optional[bool] = False, border: int = 0):
    self.section = section
    self.onClick = onClick
    self.sendStateInfoOnClick = sendStateInfoOnClick
    self.onClickParams = onClickParams
    self.border = border
    self.toggled = False
    self.defaultBackground = section.background
    self.toggledBackground = indicatorColor
    self.borderColor = borderColor
    self.borderColorToggled = borderColorToggled
    self.borderRect = pg.Rect(self.section.x - border, self.section.y - border, self.section.width + (border * 2), self.section.height + (border * 2))
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True

    self.innerBoxPadding = .1
    self.innerBox = pg.Rect(0, 0, 0, 0)
    self.update()

  def updateInnerBox(self):
    newX = self.section.x + (self.section.width * self.innerBoxPadding)
    newY = self.section.y  + (self.section.height * self.innerBoxPadding)
    newW = (self.section.width / 2) * (1 - (self.innerBoxPadding * 2))
    newH = self.section.height * (1 - (self.innerBoxPadding * 2))

    if self.toggled:
      newX = self.section.x + (self.section.width / 2)

    self.innerBox.update(newX, newY, newW, newH)

  def checkEvent(self, event: pg.event.Event) -> Optional[bool]:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(event.pos):
      self.toggled = not self.toggled

      if self.toggled:
        self.section.background = self.toggledBackground
      else:
        self.section.background = self.defaultBackground

      self.updateInnerBox()

      if self.onClick:
        if self.onClickParams is not None:
          if self.sendStateInfoOnClick:
            self.onClick(self.onClickParams, self.toggled)
          else:
            self.onClick(self.onClickParams)
        else:
          if self.sendStateInfoOnClick:
            self.onClick(self.toggled)
          else:
            self.onClick()

      return True
    return False

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    if self.toggled:
      self.section.background = self.toggledBackground
    else:
      self.section.background = self.defaultBackground

    newBorderX, newBorderY = self.section.x - self.border, self.section.y - self.border
    newBorderWidth, newBorderHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    self.borderRect.update(newBorderX, newBorderY, newBorderWidth, newBorderHeight)

    self.updateInnerBox()

  def draw(self, surface: pg.surface.Surface):
    if not (self.active and self.activeDraw):
      return None

    if self.border > 0:
      if self.toggled:
        pg.draw.rect(surface, self.borderColorToggled, self.borderRect, border_radius = self.section.borderRadius)
      else:
        pg.draw.rect(surface, self.borderColor, self.borderRect, border_radius = self.section.borderRadius)

    self.section.draw(surface)

    if self.toggled:
      pg.draw.rect(surface, self.defaultBackground, self.innerBox, border_radius = self.section.borderRadius)
    else:
      pg.draw.rect(surface, self.toggledBackground, self.innerBox, border_radius = self.section.borderRadius)

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
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.pressed = False
    self.value = self.valueRange[0]

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
        self.dragElement.dimensions['x'] = DynamicValue('customCallable', getDragElementPos, ('x', 'circle', self))
        self.dragElement.dimensions['y'] = DynamicValue('customCallable', lambda section: section.y + (section.height / 2), self.section)
      else:
        self.dragElement.dimensions['x'] = DynamicValue('customCallable', lambda section: section.x + (section.width / 2), self.section)
        self.dragElement.dimensions['y'] = DynamicValue('customCallable', getDragElementPos, ('y', 'circle', self))
    else:
      if self.orientation == 'horizontal':
        self.dragElement.dimensions['x'] = DynamicValue('customCallable', getDragElementPos, ('x', 'section', self))
        self.dragElement.dimensions['y'] = DynamicValue('customCallable', lambda params: params[0].y + ((params[0].height - params[1].height) / 2), (self.section, self.dragElement))
      else:
        self.dragElement.dimensions['x'] = DynamicValue('customCallable', lambda params: params[0].x + ((params[0].width - params[1].width) / 2), (self.section, self.dragElement))
        self.dragElement.dimensions['y'] = DynamicValue('customCallable', getDragElementPos, ('y', 'section', self))

    if self.dragElementType == 'section':
      if self.orientation == 'horizontal':
        self.mapPosition = DynamicValue('customCallable', lambda element: element.x + (element.width / 2), self.dragElement)
      else:
        self.mapPosition = DynamicValue('customCallable', lambda element: element.y + (element.height / 2), self.dragElement)
    else:
      if self.orientation == 'horizontal':
        self.mapPosition = self.dragElement.dimensions['x']
      else:
        self.mapPosition = self.dragElement.dimensions['y']

    filledSliderWidth = None
    filledSliderHeight = None
    if self.orientation == 'horizontal':
      filledSliderWidth = DynamicValue('customCallable', lambda params: params[0].value - params[1].x, (self.mapPosition, self.section))
      filledSliderHeight = self.section.dimensions['height']
    else:
      filledSliderWidth = self.section.dimensions['width']
      filledSliderHeight = DynamicValue('customCallable', lambda params: params[0].value - params[1].y, (self.mapPosition, self.section))

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

  def draw(self, surface: pg.surface.Surface):
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
