from typing import Dict, Optional, Union
from math import sqrt
import pygame as pg
from .DynamicValue import DynamicValue
from ..helpers import fit, fill, squish, allIn

backgroundType = Union[pg.Color, pg.surface.Surface]

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

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
