from typing import Optional, Callable, Union
import pygame as pg
from pg_extended.Types import Background
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.TextBox import TextBox

'''
Button is a class that represents a button UI element.

Parameters:
- [required] section:            A Section object that defines the button's base model. (areas, position, size, border radius, etc.)
- [Optional] pressedBackground:  Background color or surface when the button is pressed.
- [Optional] borderColor: Color  for the button's border.
- [Optional] borderColorPressed: Color for the button's border when pressed.
- [Optional] text:               Text to display on the button.
- [Optional] fontPath:           Path to the font file for the button's text.
- [Optional] textColor:          Color of the button's text.
- [Optional] onClick:            A callable function to execute when the button is clicked.
- [Optional] onClickParams:      Parameters to pass to the onClick function.
- [Optional] border:             Width of the button's border.
- [Optional] onClickActuation:   Defines when the onClick function is called, either 'buttonDown' or 'buttonUp'.

Usable methods:
- checkEvent: Checks for mouse button events and toggles the button state accordingly.
- update:     Updates the button's dimensions and text based on the provided Section object.
- draw:       Draws the button on the provided surface.
'''
class Button:
  def __init__(self, section: Section, pressedBackground: Optional[Background] = None, borderColor: Optional[pg.Color] = None, borderColorPressed: Optional[pg.Color] = None, text: Optional[str] = None, fontPath: Optional[str] = None, textColor: Optional[pg.Color] = None, onClick: Optional[Callable] = None, onClickParams = None, border: Optional[int] = 0, onClickActuation: Optional[str] = 'buttonDown'):
    self.section = section
    self.onClick = onClick
    self.onClickParams = onClickParams
    self.onClickActuation = onClickActuation
    self.border = border
    self.defaultBackground = section.background
    self.pressedBackground = pressedBackground
    self.borderColor = borderColor
    self.borderColorPressed = borderColorPressed

    self.pressed = False
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

    if self.border > 0:
      self.borderRect = pg.Rect(section.x - border, section.y - border, section.width + (border * 2), section.height + (border * 2))

    if text:
      self.textBox = TextBox(section, text, fontPath, textColor)
      self.hasText = True
    else:
      self.hasText = False

    if not onClickActuation in ('buttonDown', 'buttonUp'):
      raise ValueError('onClickActuation must be either \'buttonDown\' or \'buttonUp\'')

    self.update()

  def checkEvent(self, event: pg.Event) -> Optional[bool]:
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

      if self.onClickActuation == 'buttonUp' and self.onClick and self.section.rect.collidepoint(event.pos):
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

    if self.hasText:
      self.textBox.update()
    else:
      self.section.update()

    newX, newY = self.section.x - self.border, self.section.y - self.border
    newWidth, newHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    if self.border > 0:
      self.borderRect.update(newX, newY, newWidth, newHeight)

  def draw(self, surface: pg.Surface):
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
