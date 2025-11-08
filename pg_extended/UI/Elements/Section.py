from typing import Optional, Union, Dict
import pygame as pg
from pg_extended.Types import Background
from pg_extended.Util import ImgManipulatoin
from pg_extended.Util import Misc
from pg_extended.Core import DynamicValue

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

'''
Section is a class that represents a rectangular area on the screen.
It is used as a base / container for other UI elements.

Parameters:
- [required] dimensions:            A dictionary containing the dimensions of the section (x, y, width, height).
-                                   The values in the dictionary must be instances of DynamicValue.
- [required] background:            The background color or surface of the section (pg.Color or pg.Surface).
- [Optional] borderRadius:          The border radius of the section (default is 0).
- [Optional] backgroundSizeType:    The type of background size adjustment (fit, fill, squish, none).
- [Optional] backgroundSizePercent: The percentage of the background size adjustment (default is 100).

Usable methods:
- update: Updates the section's dimensions and background based on the provided DynamicValue objects.
- draw:   Draws the section on the provided surface.
'''
class Section:
  def __init__(self, dimensions: Dict['str', DynamicValue], background: Background, borderRadius: Optional[float] = 0, backgroundSizeType: Optional[str] = 'fit', backgroundPosition: Optional[str] = 'center', backgroundSizePercent: Optional[int] = 100):
    self.dimensions = dimensions
    self.background = background
    self.drawImage = None
    self.rect = pg.Rect(0, 0, 0, 0)
    self.borderRadius = borderRadius
    self.backgroundSizeType = backgroundSizeType
    self.backgroundSizePercent = backgroundSizePercent
    self.backgroundPosition = backgroundPosition
    self.backgroundOffset = [0, 0]
    self.backgroundSmoothScale = True
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

    if len(self.dimensions) != 4:
      raise ValueError(f'dimensions must contain 4 Dimension objects, received: {len(self.dimensions)}')

    if not Misc.allIn(('x', 'y', 'width', 'height'), self.dimensions):
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

    # # This is really not ideal but I don't know what else I can do
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
    #     self.width == self.dimensions['width'].value and
    #     self.height == self.dimensions['height'].value
    #     ): unstable = False
    #   else:
    #     totalIterations += 1

    #   self.x = self.dimensions['x'].value
    #   self.y = self.dimensions['y'].value
    #   self.width = self.dimensions['width'].value
    #   self.height = self.dimensions['height'].value

    for dim in self.dimensions:
      self.dimensions[dim].resolveValue()

    self.x = self.dimensions['x'].value
    self.y = self.dimensions['y'].value
    self.width = self.dimensions['width'].value
    self.height = self.dimensions['height'].value

    self.rect.update(self.x, self.y, self.width, self.height)

    if isinstance(self.background, pg.Surface):
      # resize the background image
      if self.backgroundSizeType == 'fit':
        self.drawImage = ImgManipulatoin.fit(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
      elif self.backgroundSizeType == 'fill':
        self.drawImage = ImgManipulatoin.fill(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
      elif self.backgroundSizeType == 'squish':
        self.drawImage = ImgManipulatoin.squish(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
      elif not self.backgroundSizePercent == 100:
        self.drawImage = ImgManipulatoin.fit(self.background, (self.background.get_width(), self.background.get_height()), self.backgroundSmoothScale, self.backgroundSizePercent)
      else:
        self.drawImage = self.background

      if self.borderRadius > 0:
        self.drawImage = ImgManipulatoin.roundImage(self.drawImage, self.borderRadius)

      # set x position
      if self.backgroundPosition.endswith('left'):
        self.imageX = self.x
      elif self.backgroundPosition.endswith('center'):
        self.imageX = self.x + ((self.width - self.drawImage.get_width()) / 2)
      elif self.backgroundPosition.endswith('right'):
        self.imageX = self.x + (self.width - self.drawImage.get_width())

      # set y position
      if self.backgroundPosition.startswith('top'):
        self.imageY = self.y
      elif self.backgroundPosition.startswith('center'):
        self.imageY = self.y + ((self.height - self.drawImage.get_height()) / 2)
      elif self.backgroundPosition.startswith('bottom'):
        self.imageY = self.y + (self.height - self.drawImage.get_height())

      # apply offset
      self.imageX += self.backgroundOffset[0]
      self.imageY += self.backgroundOffset[1]
    elif isinstance(self.background, pg.Color) and self.background.a < 255:
      self.drawImage = pg.Surface(self.rect.size, pg.SRCALPHA)
      pg.draw.rect(self.drawImage, self.background, (0, 0, self.width, self.height), border_radius=self.borderRadius)

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.Surface):
      surface.blit(self.drawImage, (self.imageX, self.imageY))
    elif isinstance(self.background, pg.Color):
      if self.background.a < 255:
        surface.blit(self.drawImage, (self.x, self.y))
      else:
        pg.draw.rect(surface, self.background, self.rect, border_radius=self.borderRadius)
