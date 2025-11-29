from typing import Literal
import pygame as pg
from pg_extended.Types import Background
from pg_extended.Util import ImgManipulation
from pg_extended.Core import DynamicValue, AnimatedValue, RectArea

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

type NumValue = DynamicValue | AnimatedValue | int | float

class Section(RectArea):
  def __init__(self, dimensions: dict[str, NumValue], background: Background, borderRadius: float | None = 0, backgroundSizeType: str | None = 'fit', backgroundPosition: str | None = 'center', backgroundSizePercent: int | None = 100):
    self.background = background
    self.midProcessBG = None
    self.drawReady = None

    self.backgroundSizeType = backgroundSizeType
    self.backgroundSizePercent = backgroundSizePercent
    self.backgroundPosition = backgroundPosition
    self.backgroundOffset = [0, 0]

    self.borderRadius = borderRadius

    self.backgroundSmoothScale = True

    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

    if not self.backgroundSizeType in VALID_SIZE_TYPES:
      raise ValueError(f'Invalid \"backgroundSizeType\" value, must be one of the following values: {VALID_SIZE_TYPES}')

    super().__init__(dimensions)

    self.update()

  def resizeBackground(self, getFrom: Literal['raw', 'mid', 'final'], setTo: Literal['raw', 'mid', 'final']):
    if not isinstance(self.background, pg.Surface):
      return None

    if getFrom == 'raw':
      sourceImage = self.background
    elif getFrom == 'mid':
      sourceImage = self.midProcessBG
    else:
      sourceImage = self.drawReady

    if self.backgroundSizeType == 'fit':
      result = ImgManipulation.fit(sourceImage, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif self.backgroundSizeType == 'fill':
      result = ImgManipulation.fill(sourceImage, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif self.backgroundSizeType == 'squish':
      result = ImgManipulation.squish(sourceImage, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif not self.backgroundSizePercent == 100:
      result = ImgManipulation.fit(sourceImage, (self.background.get_width(), self.background.get_height()), self.backgroundSmoothScale, self.backgroundSizePercent)
    else:
      result = sourceImage

    if setTo == 'raw':
      self.background = result
    elif setTo == 'mid':
      self.midProcessBG = result
    else:
      self.drawReady = result

  def applyRadiusToBackground(self, getFrom: Literal['raw', 'mid', 'final'], setTo: Literal['raw', 'mid', 'final']):
    if not isinstance(self.background, pg.Surface):
      return None

    if getFrom == 'raw':
      sourceImage = self.background
    elif getFrom == 'mid':
      sourceImage = self.midProcessBG
    else:
      sourceImage = self.drawReady

    if self.borderRadius is None or self.borderRadius <= 0:
      result = sourceImage
    else:
      result = ImgManipulation.roundImage(sourceImage, self.borderRadius)

    if setTo == 'raw':
      self.background = result
    elif setTo == 'mid':
      self.midProcessBG = result
    else:
      self.drawReady = result

  def setBackgroundPos(self, source: Literal['raw', 'mid', 'final']):
    if not isinstance(self.background, pg.Surface):
      return None

    if source == 'raw':
      sourceImage = self.background
    elif source == 'mid':
      sourceImage = self.midProcessBG
    else:
      sourceImage = self.drawReady

    # set x position
    if self.backgroundPosition.endswith('left'):
      self.imageX = self.x
    elif self.backgroundPosition.endswith('center'):
      self.imageX = self.x + ((self.width - sourceImage.get_width()) / 2)
    elif self.backgroundPosition.endswith('right'):
      self.imageX = self.x + (self.width - sourceImage.get_width())

    # set y position
    if self.backgroundPosition.startswith('top'):
      self.imageY = self.y
    elif self.backgroundPosition.startswith('center'):
      self.imageY = self.y + ((self.height - sourceImage.get_height()) / 2)
    elif self.backgroundPosition.startswith('bottom'):
      self.imageY = self.y + (self.height - sourceImage.get_height())

    # apply offset
    self.imageX += self.backgroundOffset[0]
    self.imageY += self.backgroundOffset[1]

  def createTransparentSurface(self, setTo: Literal['raw', 'mid', 'final']):
    if not isinstance(self.background, pg.Color) or self.background.a == 255:
      return None

    if setTo == 'raw':
      self.background = pg.Surface(self.rect.size, pg.SRCALPHA)
      pg.draw.rect(self.background, self.background, (0, 0, self.width, self.height), border_radius=self.borderRadius)
    elif setTo == 'mid':
      self.midProcessBG = pg.Surface(self.rect.size, pg.SRCALPHA)
      pg.draw.rect(self.midProcessBG, self.background, (0, 0, self.width, self.height), border_radius=self.borderRadius)
    else:
      self.drawReady = pg.Surface(self.rect.size, pg.SRCALPHA)
      pg.draw.rect(self.drawReady, self.background, (0, 0, self.width, self.height), border_radius=self.borderRadius)

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    super().update()

    if isinstance(self.background, pg.Surface):
      self.resizeBackground('raw', 'mid')
      self.applyRadiusToBackground('mid', 'final')
      self.setBackgroundPos('final')

    elif isinstance(self.background, pg.Color) and self.background.a < 255:
      self.createTransparentSurface('final')

    elif isinstance(self.background, pg.Color):
      self.drawReady = self.background

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.Surface):
      surface.blit(self.drawReady, (self.imageX, self.imageY))
    elif isinstance(self.background, pg.Color):
      if self.background.a < 255:
        surface.blit(self.drawReady, self.rect.topleft)
      else:
        pg.draw.rect(surface, self.background, self.rect, border_radius=self.borderRadius)
