import pygame as pg
from pg_extended.Core import DynamicValue, AnimatedValue, Callback
from pg_extended.UI.Elements.Section import Section

class Toggle:
  def __init__(self, section: Section, indicatorColor: pg.Color, borderColor: pg.Color, borderColorToggled: pg.Color, border: int = 0, callback: Callback = None):
    self.section = section
    self.defaultBackground = section.background
    self.indicatorColor = indicatorColor
    self.borderColor = borderColor
    self.borderColorToggled = borderColorToggled
    self.border = border
    self.callback = callback

    self.borderRect = pg.Rect(self.section.x - border, self.section.y - border, self.section.width + (border * 2), self.section.height + (border * 2))

    self.toggled = False
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

    self.innerBoxPadding = .1
    self.innerBox = pg.Rect(0, 0, 0, 0)

    self.innerBoxAnim = AnimatedValue(
      [
        DynamicValue(lambda v: v.section.x + (v.section.width * v.innerBoxPadding), args={'v': self}),
        DynamicValue(lambda v: v.section.x + (v.section.width / 2), args={'v': self})
      ], 70, 'start', 'linear', self.animationCallback
    )

    self.update()

  def animationCallback(self):
    self.lazyUpdateOverride = False
    self.update()

  def updateInnerBox(self):
    self.innerBoxAnim.resolveValue()

    newX = self.innerBoxAnim.value
    newY = self.section.y  + (self.section.height * self.innerBoxPadding)
    newW = (self.section.width / 2) * (1 - (self.innerBoxPadding * 2))
    newH = self.section.height * (1 - (self.innerBoxPadding * 2))

    self.innerBox.update(newX, newY, newW, newH)

  def checkEvent(self, event: pg.Event) -> bool | None:
    if not (self.active and self.activeEvents) or (self.innerBoxAnim.animStart is not None):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(event.pos):
      self.innerBoxAnim.trigger(self.toggled)

      self.lazyUpdateOverride = True

      self.toggled = not self.toggled

      if self.toggled:
        self.section.background = self.indicatorColor
      else:
        self.section.background = self.defaultBackground

      self.updateInnerBox()

      if self.callback is not None:
        self.callback.call({'value': self.toggled})

      return True

    return False

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    if self.toggled:
      self.section.background = self.indicatorColor
    else:
      self.section.background = self.defaultBackground

    newBorderX, newBorderY = self.section.x - self.border, self.section.y - self.border
    newBorderWidth, newBorderHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    self.borderRect.update(newBorderX, newBorderY, newBorderWidth, newBorderHeight)

    self.updateInnerBox()

  def draw(self, surface: pg.Surface):
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
      pg.draw.rect(surface, self.indicatorColor, self.innerBox, border_radius = self.section.borderRadius)
