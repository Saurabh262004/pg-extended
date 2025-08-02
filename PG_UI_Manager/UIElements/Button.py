from typing import Optional, Callable, Union
import pygame as pg
from .Section import Section
from .TextBox import TextBox

backgroundType = Union[pg.Color, pg.surface.Surface]

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
