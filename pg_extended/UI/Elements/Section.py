import pygame as pg
from pg_extended.Types import Background
from pg_extended.Util import ImgManipulation
from pg_extended.Core import DynamicValue, AnimatedValue, RectArea

VALID_SIZE_TYPES = ('fit', 'fill', 'squish', 'none')

type NumValue = DynamicValue | AnimatedValue | int | float

class Section(RectArea):
  def __init__(self, dimensions: dict[str, NumValue], background: Background, borderRadius: float | None = 0, backgroundSizeType: str | None = 'fit', backgroundPosition: str | None = 'center', backgroundSizePercent: int | None = 100):
    self.background = background
    self.drawImage = None

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

  def resizeBackground(self):
    if not isinstance(self.background, pg.Surface):
      return None

    if self.backgroundSizeType == 'fit':
      self.drawImage = ImgManipulation.fit(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif self.backgroundSizeType == 'fill':
      self.drawImage = ImgManipulation.fill(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif self.backgroundSizeType == 'squish':
      self.drawImage = ImgManipulation.squish(self.background, (self.width, self.height), self.backgroundSmoothScale, self.backgroundSizePercent)
    elif not self.backgroundSizePercent == 100:
      self.drawImage = ImgManipulation.fit(self.background, (self.background.get_width(), self.background.get_height()), self.backgroundSmoothScale, self.backgroundSizePercent)
    else:
      self.drawImage = self.background

  def applyRadiusToBackground(self):
    if not isinstance(self.background, pg.Surface) or self.borderRadius is None or self.borderRadius <= 0:
      return None

    self.background = ImgManipulation.roundImage(self.background, self.borderRadius)

  def setBackgroundPos(self):
    if not isinstance(self.background, pg.Surface):
      return None

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

  def createTransparentSurface(self):
    if not isinstance(self.background, pg.Color) or self.background.a == 255:
      return None

    self.drawImage = pg.Surface(self.rect.size, pg.SRCALPHA)
    pg.draw.rect(self.drawImage, self.background, (0, 0, self.width, self.height), border_radius=self.borderRadius)

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    super().update()

    # resize the background image
    self.resizeBackground()

    # apply border radius to background image
    self.applyRadiusToBackground()

    # set the background image position
    self.setBackgroundPos()

    # create transparent surface if needed
    self.createTransparentSurface()

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if isinstance(self.background, pg.Surface):
      surface.blit(self.drawImage, (self.imageX, self.imageY))
    elif isinstance(self.background, pg.Color):
      if self.background.a < 255:
        surface.blit(self.drawImage, self.rect.topleft)
      else:
        pg.draw.rect(surface, self.background, self.rect, border_radius=self.borderRadius)
