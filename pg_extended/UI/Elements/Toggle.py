from typing import Optional, Callable
import pygame as pg
from pg_extended.UI.Elements.Section import Section

'''
Toggle is a class that represents a toggle switch UI element.

Parameters:
- [required] section:              A Section object that defines the toggle's base model (position and size).
- [required] indicatorColor:       The color of the toggle when it is toggled on.
- [required] borderColor:          The color of the toggle's border when it is toggled off.
- [required] borderColorToggled:   The color of the toggle's border when it is toggled on.
- [Optional] onClick:              A callable function to execute when the toggle is clicked.
- [Optional] onClickParams:        Parameters to pass to the onClick function.
- [Optional] sendStateInfoOnClick: Whether to send the toggled state to the onClick function (default is False).
- [Optional] border:               Width of the toggle's border (default is 0).

Usable methods:
- checkEvent: Checks for mouse button events and toggles the toggle state accordingly.
- update:     Updates the toggle's dimensions and background based on the provided Section object.
- draw:       Draws the toggle on the provided surface.
'''
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
    self.lazyUpdate = True

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

  def checkEvent(self, event: pg.Event) -> Optional[bool]:
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
      pg.draw.rect(surface, self.toggledBackground, self.innerBox, border_radius = self.section.borderRadius)
