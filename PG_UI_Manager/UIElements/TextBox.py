from typing import Optional
import pygame as pg
from .Section import Section

'''
TextBox is a class that represents a text box UI element.

Parameters:
- [required] section:            A Section object that defines the text box's base model (position and size).
- [required] text:               The text to display in the text box.
- [required] fontPath:           The file path to the font to use for the text.
- [required] textColor:          The color of the text.
- [Optional] drawSectionDefault: Whether to draw the section background by default (default is False).
- [Optional] centerText:         Whether to center the text within the text box (default is True).

Usable methods:
- update: Updates the text box's dimensions and text based on the provided Section object.
- draw:   Draws the text box on the provided surface.
'''
class TextBox:
  def __init__(self, section: Section, text: str, fontPath: str, textColor: pg.Color, drawSectionDefault: Optional[bool] = False, centerText: Optional[bool] = True):
    self.section = section
    self.text = text
    self.fontPath = fontPath
    self.textColor = textColor
    self.drawSectionDefault = drawSectionDefault
    self.centerText = centerText
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    self.fontSize = max(10, int(self.section.height * .6))
    self.font = pg.font.SysFont(self.fontPath, self.fontSize)

    self.textSurface = self.font.render(self.text, True, self.textColor)
    if self.centerText:
      self.textRect = self.textSurface.get_rect(center=self.section.rect.center)
    else:
      self.textRect = self.textSurface.get_rect(midleft=self.section.rect.midleft)

  def draw(self, surface: pg.surface.Surface, drawSection: Optional[bool] = None):
    if not (self.active and self.activeDraw):
      return None

    if (drawSection is None and self.drawSectionDefault) or drawSection:
      self.section.draw(surface)

    surface.blit(self.textSurface, self.textRect)
