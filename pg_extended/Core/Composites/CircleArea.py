from pg_extended.Core.Base.DynamicValue import DynamicValue
from pg_extended.Core.Base.AnimatedValue import AnimatedValue

type NumValue = DynamicValue | AnimatedValue | int | float

class CircleArea:
  def __init__(self, x: NumValue, y: NumValue, radius: NumValue):
    self.dims = {
      "x": x,
      "y": y,
      "radius": radius
    }

    self.x: int | float
    self.y: int | float
    self.radius: int | float

    self.update()

  def getDimValue(self, key: str) -> int | float:
    return self.dims[key].value if isinstance(self.dims[key], (DynamicValue, AnimatedValue)) else self.dims[key]

  def update(self):
    for key in self.dims:
      if isinstance(self.dims[key], (DynamicValue, AnimatedValue)):
        self.dims[key].resolveValue()

    self.x = self.getDimValue("x")
    self.y = self.getDimValue("y")
    self.radius = self.getDimValue("radius")
