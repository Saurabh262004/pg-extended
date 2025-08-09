from typing import Optional, Union
import time
import pygame as pg
from .Section import Section
from .TextBox import TextBox

backgroundType = Union[pg.Color, pg.Surface]

IGNORE_KEYS = (9, 13, 27, 127, 1073741912)

LINE_SPLIT_UNICODES = ' \t\u00A0\u2000\u200A\u3000'+',.;:!?\'\"(){}[]/\\|-_\n\r\f\v'

class TextInput:
  def __init__(self, section: Section, fontPath: str, textColor: pg.Color, placeholder: Optional[str], placeholderTextColor: Optional[pg.Color], border: int = 1, borderColor: pg.Color = None, focusBorderColor: pg.Color = None, focusBackground: backgroundType = None, resizeable: bool = False, onChange: callable = None):
    self.section = section
    self.fontPath = fontPath
    self.textColor = textColor
    self.placeholder = placeholder
    self.placeholderTextColor = placeholderTextColor
    self.border = border
    self.borderColor = borderColor
    self.focusBorderColor = focusBorderColor
    self.background = self.section.background
    self.focusBackground = focusBackground
    self.resizeable = resizeable
    self.onChange = onChange

    self.inFocus = False
    self.typing = False
    self.typingStart = None
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True
    self.inputText = ''

    if self.placeholderTextColor is None:
      self.placeholderTextColor = self.textColor

    if self.border > 0:
      self.borderRect = pg.Rect(self.section.x - border, self.section.y - border, self.section.width + (border * 2), self.section.height + (border * 2))

    self.textBox = TextBox(self.section, self.placeholder, self.fontPath, self.placeholderTextColor, False)

    self.update()

  @staticmethod
  def getSplitText(text):
    splitArr = ['']

    for char in text:
      if char in LINE_SPLIT_UNICODES:
        if splitArr[-1][-1] == char:
          splitArr[-1] += char
        else:
          splitArr.append(char)
      else:
        splitArr[-1] += char

    return splitArr

  def checkEvent(self, event: pg.event.Event) -> Optional[bool]:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 1 and self.section.rect.collidepoint(event.pos):
        if not self.inFocus:
          self.inFocus = True

          if self.focusBackground:
            self.section.background = self.focusBackground
            self.section.update()
      else:
        self.inFocus = False

        self.section.background = self.background
        self.section.update()

    elif self.inFocus and event.type == pg.KEYDOWN:
      if not event.key in IGNORE_KEYS:
        if event.key == 8: # Backspace
          if event.mod == 4160: # CTRL + Backspace
            splitArr = self.getSplitText(self.inputText)

            self.inputText = ''.join(splitArr[0:-1])
          else:
            self.inputText = self.inputText[:-1]

            self.typing = True
            self.typingStart = time.perf_counter()
            self.lastKey = 'backspace'
            self.lazyUpdate = False
        else:
          self.inputText += event.unicode

          self.typing = True
          self.typingStart = time.perf_counter()
          self.lastKey = event.unicode
          self.lazyUpdate = False
        
        if self.inputText == '':
          self.textBox.textColor = self.placeholderTextColor
          self.textBox.text = self.placeholder
        else:
          self.textBox.textColor = self.textColor
          self.textBox.text = self.inputText

        self.textBox.update()

    elif event.type == pg.KEYUP:
      self.typing = False
      self.lazyUpdate = True

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    newX, newY = self.section.x - self.border, self.section.y - self.border
    newWidth, newHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    # auto rapid input on key hold
    if self.typing and (time.perf_counter() - self.typingStart > 0.5):
      if self.lastKey == 'backspace':
        self.inputText = self.inputText[:-1]
      else:
        self.inputText += self.lastKey

      if self.inputText == '':
        self.textBox.textColor = self.placeholderTextColor
        self.textBox.text = self.placeholder
      else:
        self.textBox.textColor = self.textColor
        self.textBox.text = self.inputText

    try:
      self.textBox.update()
    except Exception as e:
      print(e)

    if self.border > 0:
      self.borderRect.update(newX, newY, newWidth, newHeight)

  def draw(self, surface: pg.Surface):
    if not (self.active and self.activeDraw):
      return None

    if self.border > 0:
      if self.inFocus:
        pg.draw.rect(surface, self.focusBorderColor, self.borderRect, border_radius = self.section.borderRadius)
      else:
        pg.draw.rect(surface, self.borderColor, self.borderRect, border_radius = self.section.borderRadius)

    self.section.draw(surface)

    self.textBox.draw(surface)
