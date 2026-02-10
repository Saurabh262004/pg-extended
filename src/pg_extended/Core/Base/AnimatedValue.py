from typing import Literal
import time
from pg_extended.Core.Base.DynamicValue import DynamicValue
from pg_extended.Types import CallableLike

class InterpolationAlgos:
	# ---  interpolation functions ---
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

	# --- reduction functions ---
	@staticmethod
	def deCasteljau(vals: list[int | float], t: float, interpolation: CallableLike) -> int | float:
		while len(vals) > 1:
			tmp = []

			for i in range(len(vals) - 1):
				tmp.append(
					interpolation(vals[i], vals[i + 1], t)
				)

			vals = tmp

		return vals[0]

	@staticmethod
	def linearChain(vals: list[int | float], t: float, interpolation: CallableLike) -> int | float:
		n = len(vals) - 1

		segment = min(int(t * n), n - 1)

		local_t = (t - (segment / n)) * n

		return interpolation(vals[segment], vals[segment + 1], local_t)

	@staticmethod
	def step(vals: list[int | float], t: float, *_args) -> int | float:
		index = int(t * len(vals))

		index = min(index, len(vals) - 1)

		return vals[index]

	@staticmethod
	def weighted(vals: list[int | float], t: float, *_args) -> int | float:
		n = len(vals)

		total_weight = 0.0
		acc = 0.0

		for i, v in enumerate(vals):
			pos = i / (n - 1)
			w = max(0.0, 1.0 - abs(t - pos))
			acc += v * w
			total_weight += w

		return acc / total_weight if total_weight != 0 else vals[0]

	@staticmethod
	def catmullRom(vals: list[int | float], t: float, *_args) -> int | float:
		padded = [vals[0]] + vals + [vals[-1]]
		n = len(padded) - 3  # number of spline segments

		seg = min(int(t * n), n - 1)
		local_t = (t - seg / n) * n

		p0, p1, p2, p3 = padded[seg:seg + 4]

		t2 = local_t * local_t
		t3 = t2 * local_t

		val = 0.5 * (
			2 * p1 +
			(-p0 + p2) * local_t +
			(2*p0 - 5*p1 + 4*p2 - p3) * t2 +
			(-p0 + 3*p1 - 3*p2 + p3) * t3
		)

		return val

INTERPOLATION_TYPES = ['linear', 'easeIn', 'easeOut', 'easeInOut', 'custom']
INTERPOLATION_TYPES_TYPE = Literal['linear', 'easeIn', 'easeOut', 'easeInOut', 'custom']

REDUCER_TYPES = ['deCasteljau', 'linearChain', 'step', 'weighted', 'catmullRom', 'custom']
REDUCER_TYPES_TYPE = Literal['deCasteljau', 'linearChain', 'step', 'weighted', 'catmullRom', 'custom']

DEFAULT_POS_VALS = ['start', 'end']
DEFAULT_POS_VALS_TYPE = Literal['start', 'end']

type valuesType = list[DynamicValue | AnimatedValue | int | float] | tuple[DynamicValue | AnimatedValue | int | float]

INTERPOLATION_MAP = {
	'linear': InterpolationAlgos.linear,
	'easeIn': InterpolationAlgos.easeIn,
	'easeOut': InterpolationAlgos.easeOut,
	'easeInOut': InterpolationAlgos.easeInOut
}

REDUCER_MAP = {
	'deCasteljau': InterpolationAlgos.deCasteljau,
	'linearChain': InterpolationAlgos.linearChain,
	'step': InterpolationAlgos.step,
	'weighted': InterpolationAlgos.weighted,
	'catmullRom': InterpolationAlgos.catmullRom
}

class AnimatedValue:
	def __init__(self, values: valuesType, duration: float, defaultPos: DEFAULT_POS_VALS_TYPE = 'start', interpolation: INTERPOLATION_TYPES_TYPE = 'linear', reducer: REDUCER_TYPES_TYPE = 'deCasteljau', callback: CallableLike = None, customInterpolation: CallableLike = None, customReducer: CallableLike = None, resolveNow: bool = True):
		if len(values) < 2:
			raise ValueError("Animator requires a minimum of two values to animate between.")

		if duration <= 0:
			raise ValueError("Invalid duration for animation.")

		if not interpolation in INTERPOLATION_TYPES:
			raise ValueError(f'Invalid interpolation type: {interpolation}. Must be one of: {INTERPOLATION_TYPES}')

		if interpolation == 'custom' and customInterpolation is None:
			raise ValueError('Custom interpolation function must be provided when using "custom" interpolation type.')

		if not reducer in REDUCER_TYPES:
			raise ValueError(f'Invalid defaultPos: {defaultPos}. Must be one of: {DEFAULT_POS_VALS}')

		self.values = values
		self.rawValues: list[int | float] = []
		self.duration = duration
		self.interpolation = interpolation
		self.reducer = reducer
		self.callback = callback
		self.defaultPos = defaultPos
		self.value = None

		if resolveNow:
			self.updateValues()

			if self.defaultPos == 'start':
				self.value = self.rawValues[0]
			else:
				self.value = self.rawValues[-1]

		self.animStart: float = None
		self.reverse: bool = False
		self.repeats: int = 0
		self.alternate: bool = False
		self.hasPlayedOnce: bool = False
		self.delay: int = 0

		if self.interpolation in INTERPOLATION_MAP:
			self.interpolationStep = INTERPOLATION_MAP[self.interpolation]
		elif self.interpolation == 'custom':
			self.interpolationStep = customInterpolation

		if self.reducer in REDUCER_MAP:
			self.reducer = REDUCER_MAP[self.reducer]
		elif self.reducer == 'custom':
			self.reducer = customReducer

	# get raw values from animated / dynamic values
	def updateValues(self):
		self.rawValues = []

		for value in self.values:
			if isinstance(value, (DynamicValue, AnimatedValue)):
				value.resolveValue()
				self.rawValues.append(value.value)
			else:
				self.rawValues.append(value)

	# get an interpolated value from normalized t
	def interpolate(self, t: float):
		if t <= 0:
			self.value = self.rawValues[0]
			return

		if t >= 1:
			self.value = self.rawValues[-1]
			return

		self.value = self.reducer(list(self.rawValues), t, self.interpolationStep)

	def _getNormalizedT(self, elapsedTime: float) -> float:
		return 1 - (elapsedTime / self.duration) if self.reverse else (elapsedTime / self.duration)

	# calculate current animation time, get normalized t, call .interpolate() etc..
	# most importantly this is the function you need to call to update the animated value
	def resolveValue(self):
		if self.animStart is None:
			self.updateRestingPos()
			return

		elapsedTime = ((time.perf_counter() * 1000) - self.animStart) - self.delay

		self.updateValues()

		if elapsedTime >= self.duration:
			self.finishAnim()
		else:
			self.interpolate(self._getNormalizedT(elapsedTime))

	# handle animation ends, repeats, callbacks used by .resolveValue()
	def finishAnim(self):
		if self.reverse:
			self.value = self.rawValues[0]
		else:
			self.value = self.rawValues[-1]

		self.animStart = None

		self.hasPlayedOnce = True

		if self.repeats > 0:
			self.repeats -= 1
			self.trigger(self.reverse, self.repeats, self.alternate)
			return None

		if self.repeats == -1:
			self.trigger(self.reverse, self.repeats, self.alternate)
			return None

		if self.callback is not None:
			self.callback()

	# updates the value to a default idle position when no animation is playing
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

		compacted:
		(B and not A) or (A and (B == C))

		I know this shit ain't getting me a single extra frame
		'''

		pickStart = (B and not A) or (A and (B == C))

		self.value = self.rawValues[0] if pickStart else self.rawValues[-1]

	# triggers animation
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

	# stops all animations, resets repeats and instantly snaps the value to a resting position
	def terminate(self):
		if self.animStart is None:
			return None

		self.animStart = None
		self.repeats = 0

		if self.reverse:
			self.value = self.rawValues[0]
		else:
			self.value = self.rawValues[-1]
