from copy import copy
from pg_extended.UI.Elements import *

class CopyElement:
	@staticmethod
	def copyElement(element: UIElement) -> UIElement:
		# from pg_extended.UI import Section, Circle, TextBox, Button, Slider, TextInput

		if isinstance(element, Section):
			return CopyElement.copySection(element)
		elif isinstance(element, Circle):
			return CopyElement.copyCircle(element)
		elif isinstance(element, TextBox):
			return CopyElement.copyTextBox(element)
		elif isinstance(element, Button):
			return CopyElement.copyButton(element)
		elif isinstance(element, Toggle):
			return CopyElement.copyToggle(element)
		elif isinstance(element, Slider):
			return CopyElement.copySlider(element)
		elif isinstance(element, TextInput):
			return CopyElement.copyTextInput(element)
		else:
			raise ValueError('Unsupported element type for copying')

	@staticmethod
	def copySection(section: Section) -> Section:
		return Section(
			copy(section.dimensions),
			section.background,
			section.borderRadius,
			section.backgroundSizeType,
			section.backgroundPosition,
			section.backgroundSizePercent
		)

	@staticmethod
	def copyCircle(circle: Circle) -> Circle:
		return Circle(
			copy(circle.dimensions),
			circle.background,
			circle.backgroundSizeType,
			circle.backgroundSizePercent
		)

	@staticmethod
	def copyTextBox(textBox: TextBox) -> TextBox:
		element = TextBox(
			CopyElement.copySection(textBox.section),
			textBox.text,
			textBox.fontPath,
			textBox.textColor,
			textBox.fontSize
		)

		element.drawSectionDefault = textBox.drawSectionDefault
		element.alignTextHorizontal = textBox.alignTextHorizontal
		element.alignTextVertical = textBox.alignTextVertical
		element.paddingLeft = textBox.paddingLeft
		element.paddingRight = textBox.paddingRight
		element.active = textBox.active
		element.activeDraw = textBox.activeDraw
		element.activeUpdate = textBox.activeUpdate
		element.lazyUpdate = textBox.lazyUpdate
		element.lazyUpdateOverride = textBox.lazyUpdateOverride

		return element

	@staticmethod
	def copyButton(button: Button) -> Button:
		return Button(
			CopyElement.copyTextBox(button.textBox),
			button.callback,
			button.border,
			button.defaultBorderBG,
			button.pressedBG,
			button.pressedBorderBG
		)

	@staticmethod
	def copyToggle(toggle: Toggle) -> Toggle:
		return Toggle(
			CopyElement.copySection(toggle.section),
			toggle.indicatorColor,
			toggle.borderColor,
			toggle.borderColorToggled,
			toggle.border,
			toggle.callback
		)

	@staticmethod
	def copySlider(slider: Slider) -> Slider:
		return Slider(
			slider.orientation,
			CopyElement.copySection(slider.section),
			CopyElement.copySection(slider.dragElement) if slider.dragElementType == 'section' else CopyElement.copyCircle(slider.dragElement),
			slider.valueRange,	
			slider.scrollSpeed,
			slider.filledSliderBackground,
			slider.callback,
			slider.hoverToScroll
		)

	@staticmethod
	def copyTextInput(textInput: TextInput) -> TextInput:
		element = TextInput(
			CopyElement.copySection(textInput.section),
			textInput.fontPath,
			textInput.textColor,
			textInput.callback
		)

		element.max = textInput.max
		element.placeholder = textInput.placeholder
		element.border = textInput.border
		element.borderColor = textInput.borderColor
		element.focusBorderColor = textInput.focusBorderColor
		element.background = textInput.background
		element.focusBackground = textInput.focusBackground
		element.alignTextHorizontal = textInput.alignTextHorizontal
		element.active = textInput.active
		element.activeDraw = textInput.activeDraw
		element.activeUpdate = textInput.activeUpdate
		element.activeEvents = textInput.activeEvents
		element.lazyUpdate = textInput.lazyUpdate
		element.autoInputDelay = textInput.autoInputDelay
		element.autoInputMinInterval = textInput.autoInputMinInterval
		element.autoInputInterval = textInput.autoInputInterval
		element.autoInputSpeedIncrease = textInput.autoInputSpeedIncrease

		return element
