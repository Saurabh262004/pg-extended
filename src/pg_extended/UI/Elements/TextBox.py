import os
import pygame as pg
from pg_extended.Core import DynamicValue
from pg_extended.UI.Elements.Section import Section

ALIGNMENT_MAP = {
  'left-top': 'topleft',
  'left-center': 'midleft',
  'left-bottom': 'bottomleft',
  'center-top': 'midtop',
  'center-center': 'center',
  'center-bottom': 'midbottom',
  'right-top': 'topright',
  'right-center': 'midright',
  'right-bottom': 'bottomright',
}

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

    if self.text == '':
      return None

    if self.fontSize:
      self.fontSize.resolveValue()
      fontSize = self.fontSize.value
    else:
      fontSize = .6 * self.section.height

    if os.path.exists(self.fontPath):
      self.font = pg.font.Font(self.fontPath, int(fontSize))
    else:
      matched = pg.font.match_font(self.fontPath)
      if matched:
        self.font = pg.font.Font(matched, int(fontSize))
      else:
        self.font = pg.font.Font(None, int(fontSize))

    self.paddingLeftStr = ' ' * self.paddingLeft
    self.paddingRightStr = ' ' * self.paddingRight
    self.textSurface = self.font.render(f'{self.paddingLeftStr}{self.text}{self.paddingRightStr}', True, self.textColor)

    if self.textColor.a < 255:
      self.textSurface.set_alpha(self.textColor.a)

    key = f'{self.alignTextHorizontal}-{self.alignTextVertical}'
    pos_attr = ALIGNMENT_MAP[key]

    self.textRect = self.textSurface.get_rect(**{pos_attr: getattr(self.section.rect, pos_attr)})

  def draw(self, surface: pg.Surface, drawSection: bool = None):
    if not (self.active and self.activeDraw):
      return None

    if (drawSection is None and self.drawSectionDefault) or drawSection:
      self.section.draw(surface)

    if self.text == '':
      return None

    surface.blit(self.textSurface, self.textRect)
