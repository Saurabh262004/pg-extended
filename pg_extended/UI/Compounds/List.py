from typing import Dict
from pg_extended.UI.Elements import UIElement
from pg_extended.UI.Elements import Circle
from pg_extended.Util.CopyElement import CopyElement
from pg_extended.Core.DynamicValue import DynamicValue

class List:
  def __init__(self, listPos: Dict[str, DynamicValue], listElement: UIElement, length: int, spacing: DynamicValue = None):
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

      if newElement.section:
        newElement.section.dimensions['x'] = self.listPos['x']
        newElement.section.dimensions['y'] = DynamicValue(self.getElementY, kwargs={'index': i})
      elif newElement.dimensions:
        newElement.dimensions['x'] = self.listPos['x']
        newElement.dimensions['y'] = DynamicValue(self.getElementY, kwargs={'index': i})

      self.elements.append(newElement)

  def getElementY(self, index: int) -> int | float:
    if self.listElement.section:
      elementHeight = self.listElement.section.height
    elif self.listElement.dimensions:
      if isinstance(self.listElement, Circle):
        elementHeight = self.listElement.radius * 2
      else:
        elementHeight = self.listElement.height

    self.spacing.resolveValue()

    spacingValue = self.spacing.value

    self.listPos['y'].resolveValue()

    containerY = self.listPos['y'].value

    return containerY + (index * (elementHeight + spacingValue))
