import time
from pg_extended.Core.DynamicValue import DynamicValue

INTERPOLATION_TYPES = ['linear', 'easeIn', 'easeOut', 'easeInOut', 'custom']
DEFAULT_POS_VALS = ['start', 'end']

class AnimatedValue:
  def __init__(self, values: list[DynamicValue] | tuple[DynamicValue], duration: float, defaultPos: str = 'start', interpolation: str = 'linear', callback: callable = None, customInterpolation: callable = None):
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

    self.animStart: float = None
    self.reverse: bool = False
    self.repeats: int = 0
    self.alternate: bool = False
    self.hasPlayedOnce: bool = False
    self.delay: int = 0

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
  def linear(start: float, end: float, t: float) -> float:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    return start + (end - start) * t

  @staticmethod
  def easeIn(start: float, end: float, t: float) -> float:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = t ** 2

    return start + (end - start) * t

  @staticmethod
  def easeOut(start: float, end: float, t: float) -> float:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = 1 - (1 - t) ** 2

    return start + (end - start) * t

  @staticmethod
  def easeInOut(start: float, end: float, t: float) -> float:
    if t <= 0:
      return start
    elif t >= 1:
      return end

    t = t**3 * (t * (t * 6 - 15) + 10)

    return start + (end - start) * t

  def updateValues(self):
    for value in self.values:
      value.resolveValue()

  def interpolate(self, t: float):
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
      self.updateRestingPos()
      return

    elapsedTime = ((time.perf_counter() * 1000) - self.animStart) - self.delay

    self.updateValues()

    if elapsedTime >= self.duration:
      if self.reverse:
        self.value = self.values[0].value
      else:
        self.value = self.values[-1].value

      self.animStart = None

      self.hasPlayedOnce = True

      if self.repeats > 0:
        self.repeats -= 1
        self.trigger(self.reverse, self.repeats, self.alternate)
        return
      elif self.repeats == -1:
        self.trigger(self.reverse, self.repeats, self.alternate)
        return

      if self.callback is not None:
        self.callback()

    else:
      if self.reverse:
        t = 1 - (elapsedTime / self.duration)
      else:
        t = elapsedTime / self.duration

      self.interpolate(t)

  def updateRestingPos(self):
    self.updateValues()

    A = self.hasPlayedOnce
    B = self.defaultPos == 'start'
    C = self.reverse

    '''
    this let's the system decide the resting position with only the default position when it hasn't ran yet
    once it has ran, the reverse value also has an effect on the resting value

    if self.hasPlayedOnce:
      if self.defaultPos == 'start':
        if self.reverse:
          self.value = self.values[0].value
        else:
          self.value = self.values[-1].value
      else:
        if self.reverse:
          self.value = self.values[-1].value
        else:
          self.value = self.values[0].value
    else:
      if self.defaultPos == 'start':
        self.value = self.values[0].value
      else:
        self.value = self.values[-1].value

    condition for choosing first value:
    (A and B and C) or (A and not B and not C) or (not A and B)
    condition for choosing last value:
    (A and B and not C) or (A and not B and C) or (not A and not B)

    compacted:
    (A and (B == C)) or (not A and B)
    '''

    pickStart = (A and (B == C)) or (not A and B)

    self.value = self.values[0].value if pickStart else self.values[-1].value

  def trigger(self, reverse: bool = False, repeats: int = 0, alternate: bool = False, delay: int = 0):
    self.animStart = time.perf_counter() * 1000

    self.repeats = repeats
    self.alternate = alternate
    self.delay = delay

    if self.hasPlayedOnce:
      if self.alternate:
        self.reverse = not self.reverse
      else:
        self.reverse = reverse
    else:
      self.reverse = reverse

  def terminate(self):
    self.animStart = None
    self.repeats = 0

    if self.reverse:
      self.value = self.values[0].value
    else:
      self.value = self.values[-1].value
