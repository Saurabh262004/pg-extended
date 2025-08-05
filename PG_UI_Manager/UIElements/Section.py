from typing import Optional, Union, Dict
import pygame as pg
from ..helpers import allIn, squish, fit, fill
from .Core import DynamicValue

numType = Union[int, float]
backgroundType = Union[pg.Color, pg.surface.Surface]

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

'''
Section is a class that represents a rectangular area on the screen.
It is used as a base / container for other UI elements.

Parameters:
- [required] dimensions:            A dictionary containing the dimensions of the section (x, y, width, height).
-                                   The values in the dictionary must be instances of DynamicValue.
- [required] background:            The background color or surface of the section (pg.Color or pg.surface.Surface).
- [Optional] borderRadius:          The border radius of the section (default is 0).
- [Optional] backgroundSizeType:    The type of background size adjustment (fit, fill, squish, none).
- [Optional] backgroundSizePercent: The percentage of the background size adjustment (default is 100).

Usable methods:
- update: Updates the section's dimensions and background based on the provided DynamicValue objects.
- draw:   Draws the section on the provided surface.
'''
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
