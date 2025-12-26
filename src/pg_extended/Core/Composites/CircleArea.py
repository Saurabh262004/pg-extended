from pg_extended.Core.Base.DynamicValue import DynamicValue
from pg_extended.Core.Base.AnimatedValue import AnimatedValue

type NumValue = DynamicValue | AnimatedValue | int | float

class CircleArea:
  def __init__(self, dimensions: dict[str, NumValue]):
    self.dimensions = dimensions

    if not len(self.dimensions) == 3:
      raise ValueError(f'dimensions must contain 3 Dimension objects, received: {len(self.dimensions)}')

    for key in ('x', 'y', 'radius'):
      if not key in self.dimensions:
        raise ValueError('dimensions must contain all of the following keys: \'x\', \'y\', \'radius\'')

    self.x: int | float
    self.y: int | float
    self.radius: int | float

    self.update()

  def getDimValue(self, key: str) -> int | float:
    return self.dimensions[key].value if isinstance(self.dimensions[key], (DynamicValue, AnimatedValue)) else self.dimensions[key]

  def update(self):
    for key in self.dimensions:
      if isinstance(self.dimensions[key], (DynamicValue, AnimatedValue)):
        self.dimensions[key].resolveValue()

    self.x = self.getDimValue("x")
    self.y = self.getDimValue("y")
    self.radius = self.getDimValue("radius")
