import time
from typing import Iterable, Optional, Union
from .DynamicValue import DynamicValue

INTERPOLATION_TYPES = ['linear', 'easeIn', 'easeOut', 'easeInOut', 'custom']
DEFAULT_POS_VALS = ['start', 'end']

numType = Union[int, float]

class AnimatedValue:
  def __init__(self, values: Iterable[DynamicValue], duration: numType, defaultPos: Optional[str] = 'start', interpolation: Optional[str] = 'linear', callback: Optional[callable] = None, customInterpolation: Optional[callable] = None):
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

  def trigger(self, reverse: Optional[bool] = False):
    self.animStart = time.perf_counter() * 1000

    self.reverse = reverse
