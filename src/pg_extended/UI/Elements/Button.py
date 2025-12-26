from typing import Literal
from copy import copy
import pygame as pg
from pg_extended.Core import DynamicValue
from pg_extended.Core import CallbackSet
from pg_extended.Types import Background
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.TextBox import TextBox

class Button:
  def __init__(self, textBox: TextBox, callback: CallbackSet = None, border: int = 0, borderCol: Background = None, pressedBG: Background = None, pressedBorderBG: Background = None):
    self.textBox = textBox
    self.callback = callback
    self.border = border

    self.section = textBox.section

    self.pressedBG = pressedBG
    self.pressedBorderBG = pressedBorderBG

    self.defaultBG = copy(self.section.background)
    self.defaultBorderBG = borderCol

    self.borderSection = None

    if self.border > 0:
      self.borderSection = Section(
        {
          'x': DynamicValue(lambda: self.section.x - self.border),
          'y': DynamicValue(lambda: self.section.y - self.border),
          'width': DynamicValue(lambda: self.border * 2 + self.section.width),
          'height': DynamicValue(lambda: self.border * 2 + self.section.height)
        }, self.defaultBorderBG, self.section.borderRadius
      )

    self.active = True
    self.activeUpdate = True
    self.activeEvents = True
    self.activeDraw = True

    self.pressed = False

    self.lazyUpdate = True
    self.lazyUpdateOverride = False

  def switchBG(self):
    if self.pressed:
      if self.pressedBG:
        self.section.background = self.pressedBG

      if self.borderSection and self.pressedBorderBG:
        self.borderSection.background = self.pressedBorderBG

    else:
      self.section.background = self.defaultBG

      if self.borderSection:
        self.borderSection.background = self.defaultBorderBG

    self.section.update()

    if self.borderSection:
      self.borderSection.update()

  def handleCallback(self, event: pg.Event, eventType: Literal['mouseUp'] | Literal['mouseDown']):
    if self.callback is None:
      return None

    if eventType == 'mouseUp' and not self.section.rect.collidepoint(event.pos):
      return None

    self.callback.call(eventType)

  def checkEvent(self, event: pg.Event) -> bool | None:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.section.rect.collidepoint(event.pos):
      self.pressed = True

      self.switchBG()

      self.handleCallback(event, 'mouseDown')

      return True

    if event.type == pg.MOUSEBUTTONUP and self.pressed:
      self.pressed = False

      self.switchBG()

      self.handleCallback(event, 'mouseUp')

      return True

    return False

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    self.textBox.update()

    if self.border > 0:
      self.borderSection.update()

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if self.border > 0:
      self.borderSection.draw(surface)

    self.textBox.draw(surface, True)
