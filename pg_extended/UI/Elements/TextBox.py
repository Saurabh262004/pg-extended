from typing import Optional
import pygame as pg
from pg_extended.UI.Elements.Section import Section

TEXT_ALIGN_HORIZONTAL = ('left', 'right', 'center')
TEXT_ALIGN_VERTICAL = ('top', 'bottom', 'center')

ALIGNMENT_MAP = {
  ('left', 'top'): 'topleft',
  ('left', 'center'): 'midleft',
  ('left', 'bottom'): 'bottomleft',
  ('center', 'top'): 'midtop',
  ('center', 'center'): 'center',
  ('center', 'bottom'): 'midbottom',
  ('right', 'top'): 'topright',
  ('right', 'center'): 'midright',
  ('right', 'bottom'): 'bottomright',
}

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
  def __init__(self, section: Section, text: str, fontPath: str, textColor: pg.Color, drawSectionDefault: Optional[bool] = False, alignTextHorizontal: str = 'center', alignTextVertical: str = 'center'):
    if alignTextHorizontal not in TEXT_ALIGN_HORIZONTAL:
      raise ValueError(f'alignTexrHorizontal must be one of these values: {TEXT_ALIGN_HORIZONTAL}, received: {alignTextHorizontal}')

    if alignTextVertical not in TEXT_ALIGN_VERTICAL:
      raise ValueError(f'alignTexrHorizontal must be one of these values: {TEXT_ALIGN_VERTICAL}, received: {alignTextVertical}')

    self.section = section
    self.text = text
    self.fontPath = fontPath
    self.textColor = textColor
    self.drawSectionDefault = drawSectionDefault
    self.alignTextHorizontal = alignTextHorizontal
    self.alignTextVertical = alignTextVertical
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    self.fontSize = max(10, int(self.section.height * .6))
    self.font = pg.font.SysFont(self.fontPath, self.fontSize)

    self.textSurface = self.font.render(self.text, True, self.textColor)

    key = (self.alignTextHorizontal, self.alignTextVertical)
    pos_attr = ALIGNMENT_MAP[key]
    self.textRect = self.textSurface.get_rect(**{pos_attr: getattr(self.section.rect, pos_attr)})

  def draw(self, surface: pg.Surface, drawSection: Optional[bool] = None):
    if not (self.active and self.activeDraw):
      return None

    if (drawSection is None and self.drawSectionDefault) or drawSection:
      self.section.draw(surface)

    surface.blit(self.textSurface, self.textRect)
