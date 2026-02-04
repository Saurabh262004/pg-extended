import time
import pyperclip
import pygame as pg
from pg_extended.Core import DynamicValue, AnimatedValue, Callback
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.TextBox import TextBox

LINE_SPLIT_UNICODES = ' \t\u00A0\u2000\u200A\u3000'+',.;:!?\'\"(){}[]/\\|-_\r\f\v'

class Cursor:
	def __init__(self, width: int, height: int, textBox: TextBox = None):
		self.section: Section = Section({
			'x': 0,
			'y': 0,
			'width': width,
			'height': height
		}, pg.Color(255, 255, 255))

		self.x: int = 0
		self.y: int = 0
		self.alpha = AnimatedValue((255, 0), 500, 'start', 'easeIn')
		self.textBox = textBox

	def update(self):
		# self.surface.x = self.x *
		pass

	def draw(self, surface: pg.Surface):
		self.section.draw(surface)

class TextInput_t:
	def __init__(
		self,
		section: Section,
		fontPath: str,
		textColor: pg.Color,
		fontSize: DynamicValue = None,
		callback: Callback = None
	):

		# controllable properties
		self.section = section
		self.fontPath = fontPath
		self.textColor = textColor
		self.fontSize = fontSize
		self.callback = callback
		self.placeholderTextColor = textColor

		self.max = -1
		self.placeholder = ''
		self.border = 1
		self.borderColor = pg.Color(10, 10, 10)
		self.focusBorderColor = pg.Color(10, 10, 10)
		self.background = self.section.background
		self.focusBackground = self.section.background

		self.alignTextHorizontal = 'center'

		self.active = True
		self.activeDraw = True
		self.activeUpdate = True
		self.activeEvents = True
		self.lazyUpdate = True

		self.autoInputDelay = 0.5
		self.autoInputMinInterval = 0.01
		self.autoInputInterval = 0.06
		self.autoInputSpeedIncrease = 0.8

		# things you probably shouldn't touch
		self.lazyUpdateOverride = False
		self.inFocus = False
		self.typing = False

		self.rawInput = ''
		self.inputByLines = []
		self.inputBySections = []

		self.lastEvent = ''
		self.lastKey = ''
		self.valueOnLastCallback = ''
		self.events = {}

		self.typingStart = 0
		self.lastAutoInputTime = 0
		self.dynamicAutoInputInterval = self.autoInputInterval

		if self.fontSize is None:
			self.fontSize = DynamicValue(24)

		if self.border > 0:
			self.borderRect = pg.Rect(self.section.x - self.border, self.section.y - self.border, self.section.width + (self.border * 2), self.section.height + (self.border * 2))

		self.textBoxes: list[TextBox] = [
			TextBox(
				{
					'x': self.section.dimensions['x'],
					'y': self.section.dimensions['y'],
					'width': self.section.dimensions['width'],
					'height': self.fontSize
				},
				self.placeholder, self.fontPath, self.placeholderTextColor, self.fontSize
			)
		]

	@staticmethod
	def getSplitText(text: str):
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

	def processInput(self):
		self.inputByLines = self.rawInput.splitlines()

		self.inputBySections = []
		for line in self.inputByLines:
			splitSections = self.getSplitText(line)
			self.inputBySections.extend(splitSections)

	def _setupEvents(self):
		def unicode():
			self.rawInput += self.lastKey

		def backspace():
			self.rawInput = self.rawInput[:-1]
			self._removeEmptyTextBoxes()

		def ctrlBackspace():
			splitArr = self.getSplitText(self.rawInput)

			self.rawInput = ''.join(splitArr[:-1])

			self._removeEmptyTextBoxes()

		def enter():
			self.rawInput += '\n'
			self._addNewTextBox()

		def copy():
			pyperclip.copy(self.rawInput)

		def paste():
			self.rawInput += pyperclip.paste()

		self.events = {
			'unicode': unicode,
			'backspace': backspace,
			'ctrlBackspace': ctrlBackspace,
			'enter': enter,
			'copy': copy,
			'paste': paste,
			'pass': lambda: None
		}

	def _addNewTextBox(self):
		newBox = None

		newBox = TextBox(
			{
				'x': self.section.dimensions['x'],
				'y': DynamicValue(lambda: self.section.y + (self.textBoxes.index(newBox) * self.fontSize.value), resolveNow=False),
				'width': self.section.dimensions['width'],
				'height': self.fontSize
			},
			'', self.fontPath, self.textColor, self.fontSize
		 )

		newBox.alignTextHorizontal = self.alignTextHorizontal

		self.textBoxes.append(newBox)

	def _removeEmptyTextBoxes(self):
		popBoxes = []

		for i in range(len(self.textBoxes)-2, 0, -1):
			if self.textBoxes[i].text == '':
				popBoxes.append(i)

		for index in popBoxes:
			self.textBoxes.pop(index)
