from pg_extended.UI.Elements import UIElement
from pg_extended.UI.Elements import Circle
from pg_extended.UI.CopyElement import CopyElement
from pg_extended.Core import DynamicValue

class List:
  def __init__(self, listPos: dict[str, DynamicValue], listElement: UIElement, length: int, spacing: DynamicValue = None):
    self.listPos = listPos
    self.listElement = listElement
    self.length = length

    self.elements = []

    if spacing is None:
      self.spacing = DynamicValue(0)
    else:
      self.spacing = spacing

    for i in range(length):
      newElement = CopyElement.copyElement(listElement)

      if hasattr(newElement, 'section'):
        newElement.section.dimensions['x'] = self.listPos['x']
        newElement.section.dimensions['y'] = DynamicValue(self.getElementY, args={'index': i})
      elif hasattr(newElement, 'dimensions'):
        newElement.dimensions['x'] = self.listPos['x']
        newElement.dimensions['y'] = DynamicValue(self.getElementY, args={'index': i})

      self.elements.append(newElement)

  def getElementY(self, index: int) -> int | float:
    if index > 0:
      prevElement = self.elements[index-1]

      if hasattr(prevElement, 'section'):
        prevElementBase = prevElement.section.dimensions['y'].value + prevElement.section.dimensions['height'].value
      elif hasattr(prevElement, 'dimensions'):
        prevElementBase = prevElement.dimensions['y'].value + prevElement.dimensions['height'].value
      else:
        self.listPos['y'].resolveValue()

        return self.listPos['y'].value

      self.spacing.resolveValue()

      return prevElementBase + self.spacing.value

    self.listPos['y'].resolveValue()

    return self.listPos['y'].value
