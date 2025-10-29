import pygame as pg
from pg_extended.Core import DynamicValue
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
- [required] fontSize:           Size of the font in DynamicValue

Usable methods:
- update: Updates the text box's dimensions and text based on the provided Section object.
- draw:   Draws the text box on the provided surface.
'''
class TextBox:
  def __init__(self, section: Section, text: str, fontPath: str, textColor: pg.Color, fontSize: DynamicValue = None):
    self.section = section
    self.text = text
    self.fontPath = fontPath
    self.fontSize = fontSize
    self.textColor = textColor

    self.alignTextHorizontal = 'center'
    self.alignTextVertical = 'center'
    self.drawSectionDefault = False
    self.paddingLeft = 0
    self.paddingRight = 0
    self.paddingLeftStr = None
    self.paddingRightStr = None
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False
    self.textSurface: pg.Surface = None
    self.textRect: pg.Rect = None

    self.update()

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.section.update()

    if self.fontSize:
      self.fontSize.resolveValue()
      fontSize = self.fontSize.value
    else:
      fontSize = int(0.6 * self.section.height)

    self.font = pg.font.SysFont(self.fontPath, fontSize)

    self.paddingLeftStr = ' ' * self.paddingLeft
    self.paddingRightStr = ' ' * self.paddingRight
    self.textSurface = self.font.render(f'{self.paddingLeftStr}{self.text}{self.paddingRightStr}', True, self.textColor)

    key = (self.alignTextHorizontal, self.alignTextVertical)
    pos_attr = ALIGNMENT_MAP[key]

    self.textRect = self.textSurface.get_rect(**{pos_attr: getattr(self.section.rect, pos_attr)})

  def draw(self, surface: pg.Surface, drawSection: bool = None):
    if not (self.active and self.activeDraw):
      return None

    if (drawSection is None and self.drawSectionDefault) or drawSection:
      self.section.draw(surface)

    surface.blit(self.textSurface, self.textRect)
