from typing import Dict, Optional, Union
from math import sqrt
import pygame as pg
from pg_extended.UI.helpers import fit, fill, squish, allIn
from pg_extended.Core import DynamicValue

backgroundType = Union[pg.Color, pg.Surface]

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

'''
Circle is a class that represents a circular area on the screen.
It is similar to Section just with a circular shape.

Parameters:
- [required] dimensions:            A dictionary containing the dimensions of the circle (x, y, radius).
-                                   The values in the dictionary must be instances of DynamicValue.
- [required] background:            The background color or surface of the circle (pg.Color or pg.Surface).
- [Optional] backgroundSizeType:    The type of background size adjustment (fit, fill, squish, none).
- [Optional] backgroundSizePercent: The percentage of the background size adjustment (default is 100).

Usable methods:
- update: Updates the circle's dimensions and background based on the provided DynamicValue objects.
- draw:   Draws the circle on the provided surface.
'''

class Circle:
  def __init__(self, dimensions: Dict[str, DynamicValue], background: backgroundType, backgroundSizeType: Optional[str] = 'fit', backgroundSizePercent: Optional[int] = 100):
    self.dimensions = dimensions
    self.background = background
    self.backgroundSizeType = backgroundSizeType
    self.backgroundSizePercent = backgroundSizePercent

    self.sqrt2 = sqrt(2)
    self.drawImage = None
    self.backgroundWidth = 0
    self.backgroundHeight = 0
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

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

    # # Same as before... not ideal but I don't know what else I can do
    # unstable = True
    # totalIterations = 0
    # maxIterations = len(self.dimensions)
    # while unstable:
    #   if totalIterations > maxIterations:
    #     raise ValueError('Provided dimensions are referencing each other in a cyclic pattern, please provide valid dimenisons')

    #   for dim in self.dimensions:
    #     self.dimensions[dim].resolveValue()

    #   if (
    #     self.x == self.dimensions['x'].value and
    #     self.y == self.dimensions['y'].value and
    #     self.radius == self.dimensions['radius'].value
    #     ): unstable = False
    #   else:
    #     totalIterations += 1

    #   self.x = self.dimensions['x'].value
    #   self.y = self.dimensions['y'].value
    #   self.radius = self.dimensions['radius'].value

    for dim in self.dimensions:
      self.dimensions[dim].resolveValue()

    self.x = self.dimensions['x'].value
    self.y = self.dimensions['y'].value
    self.radius = self.dimensions['radius'].value

    if isinstance(self.background, pg.Surface):
      if self.backgroundSizeType == 'fit':
        self.drawImage = fit(self.background, (self.radius * self.sqrt2, self.radius * self.sqrt2), self.backgroundSizePercent)
      elif self.backgroundSizeType == 'fill':
        self.drawImage = fill(self.background, (self.radius * 2, self.radius * 2), self.backgroundSizePercent)
      else:
        self.drawImage = squish(self.background, (self.radius * 2, self.radius * 2), self.backgroundSizePercent)

      self.backgroundWidth = self.drawImage.get_width()
      self.backgroundHeight = self.drawImage.get_height()
    elif isinstance(self.background, pg.Color) and self.background.a < 255:
      self.drawImage = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)

      pg.draw.aacircle(self.drawImage, self.background, (self.radius, self.radius), self.radius)

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.Surface):
      surface.blit(self.drawImage, (self.x - (self.backgroundWidth / 2), self.y - (self.backgroundHeight / 2)))
    elif isinstance(self.background, pg.Color):
      if self.background.a < 255:
        surface.blit(self.drawImage, (self.x - self.radius, self.y - self.radius))
      else:
        pg.draw.aacircle(surface, self.background, (self.x, self.y), self.radius)
