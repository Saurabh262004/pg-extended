from copy import deepcopy
from pg_extended.UI.Elements import UIElement
from pg_extended.UI.Elements import *

class CopyElement:
  @staticmethod
  def copyElement(element: UIElement) -> UIElement:
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
      deepcopy(section.dimensions),
      section.background,
      section.borderRadius,
      section.backgroundSizeType,
      section.backgroundPosition,
      section.backgroundSizePercent
    )

  @staticmethod
  def copyCircle(circle: Circle) -> Circle:
    return Circle(
      deepcopy(circle.dimensions),
      circle.background,
      circle.backgroundSizeType,
      circle.backgroundSizePercent
    )

  @staticmethod
  def copyTextBox(textBox: TextBox) -> TextBox:
    return TextBox(
      CopyElement.copySection(textBox.section),
      textBox.text,
      textBox.fontPath,
      textBox.textColor,
      textBox.drawSectionDefault,
      textBox.alignTextHorizontal,
      textBox.alignTextVertical
    )

  @staticmethod
  def copyButton(button: Button) -> Button:
    return Button(
      CopyElement.copySection(button.section),
      button.pressedBackground,
      button.borderColor,
      button.borderColorPressed,
      button.textBox.text,
      button.textBox.fontPath,
      button.textBox.textColor,
      button.onClick,
      button.onClickParams,
      button.border,
      button.onClickActuation
    )

  @staticmethod
  def copyToggle(toggle: Toggle) -> Toggle:
    return Toggle(
      CopyElement.copySection(toggle.section),
      toggle.indicatorColor,
      toggle.borderColor,
      toggle.borderColorToggled,
      toggle.onClick,
      toggle.onClickParams,
      toggle.sendStateInfoOnClick,
      toggle.border
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
      slider.onChangeInfo,
      slider.hoverToScroll
    )

  @staticmethod
  def copyTextInput(textInput: TextInput) -> TextInput:
    return TextInput(
      CopyElement.copySection(textInput.section),
      textInput.fontPath,
      textInput.textColor,
      textInput.max,
      textInput.placeholder,
      textInput.placeholderTextColor,
      textInput.border,
      textInput.borderColor,
      textInput.focusBorderColor,
      textInput.focusBackground,
      textInput.onChangeInfo,
      textInput.alignTextHorizontal,
      textInput.alignTextVertical
    )
