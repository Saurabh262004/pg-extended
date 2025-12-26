import pygame as pg
from pg_extended.Core.Base.DynamicValue import DynamicValue
from pg_extended.Core.Base.AnimatedValue import AnimatedValue

type NumValue = DynamicValue | AnimatedValue | int | float

class RectArea:
  def __init__(self, dimensions: dict[str, NumValue]):
    self.dimensions: dict[str, NumValue] = dimensions

    if not len(self.dimensions) == 4:
      raise ValueError(f'dimensions must contain 4 Dimension objects, received: {len(self.dimensions)}')

    for key in ('x', 'y', 'width', 'height'):
      if not key in self.dimensions:
        raise ValueError('dimensions must contain all of the following keys: \'x\', \'y\', \'width\' \'height\'')

    self.x: int | float
    self.y: int | float
    self.width: int | float
    self.height: int | float

    self.rect: pg.Rect = pg.Rect(0, 0, 0, 0)

    self.update()

  def getDimValue(self, key: str) -> int | float:
    return self.dimensions[key].value if isinstance(self.dimensions[key], (DynamicValue, AnimatedValue)) else self.dimensions[key]

  def update(self):
    for key in self.dimensions:
      if isinstance(self.dimensions[key], (DynamicValue, AnimatedValue)):
        self.dimensions[key].resolveValue()

    self.x = self.getDimValue("x")
    self.y = self.getDimValue("y")
    self.width = self.getDimValue("width")
    self.height = self.getDimValue("height")
    
    self.rect.update(self.x, self.y, self.width, self.height)
