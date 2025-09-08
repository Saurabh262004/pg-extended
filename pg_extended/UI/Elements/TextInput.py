from typing import Optional, Union
import time
import pygame as pg
from pg_extended.Core import DynamicValue, AnimatedValue
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.TextBox import TextBox

backgroundType = Union[pg.Color, pg.Surface]

LINE_SPLIT_UNICODES = ' \t\u00A0\u2000\u200A\u3000'+',.;:!?\'\"(){}[]/\\|-_\n\r\f\v'

ONCHANGE_KEYS = ('callable', 'params', 'sendValue')

'''
TextInput is a class that represents a text input UI element.

Parameters:
- [required] section:              A Section object that defines the position, size, and background of the text input.
- [required] fontPath:             Path to the font file to render the text.
- [required] textColor:            Color of the typed text (pg.Color).
- [optional] placeholder:          Placeholder text to display when no input is provided (default is None).
- [optional] placeholderTextColor: Color of the placeholder text (default is same as textColor).
- [optional] border:               Thickness of the border around the input box (default is 0).
- [optional] borderColor:          Color of the border when not focused (default is None).
- [optional] focusBorderColor:     Color of the border when focused (default is None).
- [optional] focusBackground:      Background (Color or Surface) when focused (default is None).
- [optional] onChangeInfo:         A dictionary describing a callback to be called when the text changes.
-                                  Structure:
-                                  {
-                                    'callable':  Callable function to call on text change,
-                                    'params':    Parameters to pass to the callable (default is None),
-                                    'sendValue': Whether to also send the current input text as a parameter.
-                                  }
- [optional] alignTextHorizontal:  Horizontal alignment of the text inside the box ('left', 'center', 'right'). (default is 'center').
- [optional] alignTextVertical:    Vertical alignment of the text inside the box ('top', 'center', 'bottom'). (default is 'center').

Usable methods:
- checkEvent: Processes pygame events (mouse clicks, key presses, key releases) and updates the text input accordingly.
- update:     Updates the textbox, handles held key input, and resizes the border rectangle if necessary.
- draw:       Renders the text input (border, background, and text) onto the given surface.
'''
class TextInput:
  def __init__(self, section: Section, fontPath: str, textColor: pg.Color, max: int = -1, placeholder: str = None, placeholderTextColor: pg.Color = None, border: int = 0, borderColor: pg.Color = None, focusBorderColor: pg.Color = None, focusBackground: backgroundType = None, onChangeInfo: dict = None, alignTextHorizontal: str = 'center', alignTextVertical: str = 'center'):
    self.section = section
    self.fontPath = fontPath
    self.textColor = textColor
    self.max = max
    self.placeholder = placeholder
    self.placeholderTextColor = placeholderTextColor
    self.border = border
    self.borderColor = borderColor
    self.focusBorderColor = focusBorderColor
    self.background = self.section.background
    self.focusBackground = focusBackground
    self.onChangeInfo = onChangeInfo
    self.alignTextHorizontal = alignTextHorizontal
    self.alignTextVertical = alignTextVertical

    self.inFocus = False
    self.typing = False
    self.active = True
    self.activeDraw = True
    self.activeUpdate = True
    self.activeEvents = True
    self.lazyUpdate = True
    self.lazyUpdateOverride = False
    self.inputText = ''
    self.lastKey = ''
    self.valueOnLastCallback = ''
    self.typingStart = 0
    self.lastAutoInputTime = 0
    self.autoInputDelay = 0.5
    self.autoInputInterval = 0.06
    self.dynamicAutoInputInterval = self.autoInputInterval
    self.autoInputSpeedIncrease = 0.8
    self.autoInputMinInterval = 0.01
    self.cursor: pg.Surface = None
    self.cursorX: float = 0

    self.cursorAlpha: AnimatedValue = AnimatedValue(
      [DynamicValue('number', 255), DynamicValue('number', 0)],
      500, 'start', 'easeIn'
    )

    if self.onChangeInfo is not None:
      for k in ONCHANGE_KEYS:
        if not k in self.onChangeInfo:
          raise ValueError(f'onChangeInfo must have these keys: {ONCHANGE_KEYS}')

    if self.placeholderTextColor is None:
      self.placeholderTextColor = self.textColor

    if self.border > 0:
      self.borderRect = pg.Rect(self.section.x - border, self.section.y - border, self.section.width + (border * 2), self.section.height + (border * 2))

    self.textBox = TextBox(self.section, self.placeholder, self.fontPath, self.placeholderTextColor, False, alignTextHorizontal=alignTextHorizontal, alignTextVertical=alignTextVertical)

    self.textBox.paddingLeft = 2
    self.textBox.paddingRight = 2

    self.update()

  @staticmethod
  def getSplitText(text):
    splitArr = ['']

    for char in text:
      if char in LINE_SPLIT_UNICODES:
        if splitArr[-1] == '' or splitArr[-1][-1] == char:
          splitArr[-1] += char
        else:
          splitArr.append(char)
      else:
        splitArr[-1] += char

    return splitArr

  def callback(self):
    if not self.active:
      return None

    if (not self.onChangeInfo is None) and (not self.valueOnLastCallback == self.inputText):
      self.valueOnLastCallback = self.inputText

      if not self.onChangeInfo['params'] is None:
        if self.onChangeInfo['sendValue']:
          self.onChangeInfo['callable'](self.inputText, self.onChangeInfo['params'])
        else:
          self.onChangeInfo['callable'](self.onChangeInfo['params'])
      else:
        if self.onChangeInfo['sendValue']:
          self.onChangeInfo['callable'](self.inputText)
        else:
          self.onChangeInfo['callable']()

  def checkEvent(self, event: pg.Event) -> Optional[bool]:
    if not (self.active and self.activeEvents):
      return None

    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 1 and self.section.rect.collidepoint(event.pos):
        if not self.inFocus:
          self.inFocus = True
          self.lazyUpdateOverride = True

          self.cursorAlpha.trigger(False, -1, True)

          if self.focusBackground:
            self.section.background = self.focusBackground
            self.section.update()
      else:
        self.inFocus = False
        self.lazyUpdateOverride = False

        self.cursorAlpha.terminate()

        self.section.background = self.background
        self.section.update()

    elif self.inFocus and event.type == pg.KEYDOWN:
      if event.mod & pg.KMOD_CTRL: # CTRL
        if event.key == pg.K_BACKSPACE: # CTRL + Backspace
          splitArr = self.getSplitText(self.inputText)

          self.inputText = ''.join(splitArr[:-1])
          self.typing = True
          self.typingStart = time.perf_counter()
          self.lastKey = 'ctrlbackspace'
      else:
        if event.key == pg.K_BACKSPACE: # Backspace
          self.inputText = self.inputText[:-1]

          self.typing = True
          self.typingStart = time.perf_counter()
          self.lastKey = 'backspace'
        else:
          self.inputText += event.unicode

          self.typing = True
          self.typingStart = time.perf_counter()
          self.lastKey = event.unicode

      if self.inputText == '':
        self.textBox.textColor = self.placeholderTextColor
        self.textBox.text = self.placeholder
      else:
        self.textBox.textColor = self.textColor
        self.textBox.text = self.inputText

      self.textBox.update()

    elif event.type == pg.KEYUP:
      if self.typing:
        self.typing = False
        self.dynamicAutoInputInterval = self.autoInputInterval

        self.callback()

  def update(self):
    if not (self.active and self.activeUpdate):
      return None

    newX, newY = self.section.x - self.border, self.section.y - self.border
    newWidth, newHeight = self.section.width + (self.border * 2), self.section.height + (self.border * 2)

    if self.inFocus:
      self.cursorAlpha.resolveValue()

      self.cursor = pg.Surface((2, self.textBox.textRect.height), pg.SRCALPHA)

      self.cursor.fill((self.textColor.r, self.textColor.g, self.textColor.b, self.cursorAlpha.value))

      spaceWidth, _ = self.textBox.font.size(' ')
      leftPaddingWidth = spaceWidth * self.textBox.paddingLeft
      rightPaddingWidth = spaceWidth * self.textBox.paddingRight
      textWidth, _ = self.textBox.font.size(self.inputText)

      if self.textBox.alignTextHorizontal == 'left':
        self.cursorX = self.section.x + leftPaddingWidth + textWidth
      elif self.textBox.alignTextHorizontal == 'center':
        self.cursorX = self.section.x + (self.section.width / 2) + ((textWidth + (leftPaddingWidth - rightPaddingWidth)) / 2)
      elif self.textBox.alignTextHorizontal == 'right':
        self.cursorX = self.section.x + (self.section.width - rightPaddingWidth)

    # auto rapid input on key hold
    if self.typing and (time.perf_counter() - self.typingStart > self.autoInputDelay):
      if time.perf_counter() - self.lastAutoInputTime > self.dynamicAutoInputInterval:
        if self.dynamicAutoInputInterval > self.autoInputMinInterval:
          self.dynamicAutoInputInterval *= self.autoInputSpeedIncrease

        self.lastAutoInputTime = time.perf_counter()

        if self.lastKey == 'ctrlbackspace':
          splitArr = self.getSplitText(self.inputText)
          self.inputText = ''.join(splitArr[:-1])
        elif self.lastKey == 'backspace':
          self.inputText = self.inputText[:-1]
        elif len(self.inputText) < self.max or self.max < 0:
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

    if self.inFocus:
      surface.blit(self.cursor, (self.cursorX, self.textBox.textRect.y))
