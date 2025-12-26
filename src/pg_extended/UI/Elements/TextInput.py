import time
import pyperclip
import pygame as pg
from pg_extended.Types import Background
from pg_extended.Core import DynamicValue, AnimatedValue, Callback
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.TextBox import TextBox

LINE_SPLIT_UNICODES = ' \t\u00A0\u2000\u200A\u3000'+',.;:!?\'\"(){}[]/\\|-_\n\r\f\v'

class TextInput:
  def __init__(self, section: Section, fontPath: str, textColor: pg.Color, max: int = -1, placeholder: str = None, placeholderTextColor: pg.Color = None, border: int = 0, borderColor: pg.Color = None, focusBorderColor: pg.Color = None, focusBackground: Background = None, callback: Callback = None, alignTextHorizontal: str = 'center', alignTextVertical: str = 'center'):
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
    self.callback = callback
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
    self.lastEvent = ''
    self.lastKey = ''
    self.events = {}
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
      [DynamicValue(255), DynamicValue(0)],
      500, 'start', 'easeIn'
    )

    if self.placeholderTextColor is None:
      self.placeholderTextColor = self.textColor

    if self.border > 0:
      self.borderRect = pg.Rect(self.section.x - border, self.section.y - border, self.section.width + (border * 2), self.section.height + (border * 2))

    self.textBox = TextBox(self.section, self.placeholder, self.fontPath, self.placeholderTextColor, False)

    self.textBox.alignTextHorizontal = alignTextHorizontal
    self.textBox.alignTextVertical = alignTextVertical

    self.textBox.paddingLeft = 2
    self.textBox.paddingRight = 2

    self._setupEvents()

    self.update()

  @staticmethod
  def getSplitText(text):
    splitArr = ['']

    for char in text:
      if char.isspace():
        if splitArr[-1].isspace():
          splitArr[-1] += char
        else:
          splitArr.append(char)
      elif char in LINE_SPLIT_UNICODES:
        splitArr.append(char)
      else:
        if splitArr[-1] and not splitArr[-1].isspace() and splitArr[-1] not in LINE_SPLIT_UNICODES:
          splitArr[-1] += char
        else:
          splitArr.append(char)

    if splitArr[0] == '':
      splitArr = splitArr[1:]

    return splitArr

  def _setupEvents(self):
    def unicode():
      self.inputText += self.lastKey

    def backspace():
      self.inputText = self.inputText[:-1]

    def ctrlBackspace():
      splitArr = self.getSplitText(self.inputText)

      self.inputText = ''.join(splitArr[:-1])

    def copy():
      pyperclip.copy(self.inputText)

    def paste():
      self.inputText += pyperclip.paste()

    self.events = {
      'unicode': unicode,
      'backspace': backspace,
      'ctrlBackspace': ctrlBackspace,
      'copy': copy,
      'paste': paste,
      'pass': lambda: None
    }

  def setTextBoxValue(self):
    if self.inputText == '':
      self.textBox.textColor = self.placeholderTextColor
      self.textBox.text = self.placeholder
    else:
      self.textBox.textColor = self.textColor
      self.textBox.text = self.inputText

  def handleCallback(self):
    if not self.active:
      return None

    if (not self.callback is None) and (not self.valueOnLastCallback == self.inputText):
      self.valueOnLastCallback = self.inputText

      self.callback.call({'value': self.inputText})

  def checkEvent(self, event: pg.Event) -> bool | None:
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
      self.typing = True
      self.typingStart = time.perf_counter()

      eventTriggered = False

      if event.mod & pg.KMOD_CTRL:
        if event.key == pg.K_BACKSPACE:
          eventTriggered = True
          self.lastEvent = 'ctrlBackspace'
        elif event.key == pg.K_c:
          eventTriggered = True
          self.lastEvent = 'copy'
        elif event.key == pg.K_v:
          eventTriggered = True
          self.lastEvent = 'paste'
        else:
          self.lastEvent = 'pass'
      else:
        eventTriggered = True
        if event.key == pg.K_BACKSPACE:
          self.lastEvent = 'backspace'
        else:
          self.lastKey = event.unicode
          self.lastEvent = 'unicode'

      if eventTriggered:
        self.events[self.lastEvent]()
        self.setTextBoxValue()
        self.textBox.update()

    elif event.type == pg.KEYUP:
      if self.typing:
        self.typing = False
        self.dynamicAutoInputInterval = self.autoInputInterval

        self.handleCallback()

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

        self.events[self.lastEvent]()

        self.setTextBoxValue()

    self.textBox.update()

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
