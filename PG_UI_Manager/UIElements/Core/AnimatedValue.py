import time
from typing import Iterable, Union
from .DynamicValue import DynamicValue

INTERPOLATION_TYPES = ['linear', 'easeIn', 'easeOut', 'easeInOut', 'custom']
DEFAULT_POS_VALS = ['start', 'end']

numType = Union[int, float]

'''
AnimatedValue is a class that provides a value that can be interpolated between multiple DynamicValues with an interpolation step function.

It can be hooked to other UI elements to create an animated UI element.
Other than that, it can also be used for any other task that might need a value to go from one number to another with any function you want.

It supports following interpolation types:
- 'linear', 'easeIn', 'easeOut', 'easeInOut' and 'custom'
- a custom interpolation function must take three inputs of int or float type and return one int or float.

Parameters:
- [required] values:              An iterable of DynamicValues (must be more than 1). This is the set of values the class with interpolate over.
- [required] duration:            Duration of the animation in ms
- [optional] defaultPos:          The default values the class with have. Either start or end. (default is start)
- [optional] interpolation:       The type of interpolation to use when animating the value. (default is linear)
- [optional] callback:            A callable to call when a animation is done. (default is None)
- [optional] customInterpolation: A custom interpolation function as described above. (default is None)

Useable methods:
- trigger:          Starts the animation over time.
- resolveValue:     Resolves the value of the class if in the middle of an animation.
- updateRestingPos: Snaps the value to it's default position.
'''
class AnimatedValue:
  def __init__(self, values: Iterable[DynamicValue], duration: numType, defaultPos: str = 'start', interpolation: str = 'linear', callback: callable = None, customInterpolation: callable = None):
    if len(values) < 2:
      raise ValueError("Animator requires a minimum of two values to animate between.")

    if not interpolation in INTERPOLATION_TYPES:
      raise ValueError(f'Invalid interpolation type: {interpolation}. Must be one of: {INTERPOLATION_TYPES}')

    if interpolation == 'custom' and customInterpolation is None:
      raise ValueError('Custom interpolation function must be provided when using "custom" interpolation type.')

    if not defaultPos in DEFAULT_POS_VALS:
      raise ValueError(f'Invalid defaultPos: {defaultPos}. Must be one of: {DEFAULT_POS_VALS}')

    self.values = values
    self.duration = duration
    self.interpolation = interpolation
    self.callback = callback
    self.defaultPos = defaultPos

    if self.defaultPos == 'start':
      self.value = values[0].value
    else:
      self.value = values[-1].value

    self.animStart = None
    self.reverse = False

    if self.interpolation == 'linear':
      self.interpolationStep = self.linear
    elif self.interpolation == 'easeIn':
      self.interpolationStep = self.easeIn
    elif self.interpolation == 'easeOut':
      self.interpolationStep = self.easeOut
    elif self.interpolation == 'easeInOut':
      self.interpolationStep = self.easeInOut
    elif self.interpolation == 'custom':
      self.interpolationStep = customInterpolation

  @staticmethod
  def linear(start: numType, end: numType, t: numType) -> numType:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    return start + (end - start) * t

  @staticmethod
  def easeIn(start: numType, end: numType, t: numType) -> numType:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = t ** 2

    return start + (end - start) * t

  @staticmethod
  def easeOut(start: numType, end: numType, t: numType) -> numType:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = 1 - (1 - t) ** 2

    return start + (end - start) * t

  @staticmethod
  def easeInOut(start: numType, end: numType, t: numType) -> numType:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = 3 * t ** 2 - 2 * t ** 3

    return start + (end - start) * t

  def interpolate(self, t: numType):
    if t <= 0:
      return self.values[0].value
    elif t >= 1:
      return self.values[-1].value

    processingVals = [value.value for value in self.values]
    while len(processingVals) > 1:
      tmp = []

      for i in range(len(processingVals) - 1):
        tmp.append(
          self.interpolationStep(processingVals[i], processingVals[i + 1], t)
        )

      processingVals = tmp

    self.value = processingVals[0]

  def resolveValue(self):
    if self.animStart is None:
      return

    elapsedTime = (time.perf_counter() * 1000) - self.animStart

    if elapsedTime >= self.duration:
      if self.reverse:
        self.value = self.values[0].value
      else:
        self.value = self.values[-1].value

      self.animStart = None

      if self.callback is not None:
        self.callback()
    else:
      [value.resolveValue() for value in self.values]

      if self.reverse:
        t = 1 - (elapsedTime / self.duration)
      else:
        t = elapsedTime / self.duration

      self.interpolate(t)

  def updateRestingPos(self):
    [value.resolveValue() for value in self.values]

    if self.reverse:
      self.value = self.values[0].value
    else:
      self.value = self.values[-1].value

  def trigger(self, reverse: bool = False):
    self.animStart = time.perf_counter() * 1000

    self.reverse = reverse
