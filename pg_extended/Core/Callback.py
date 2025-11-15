from typing import Any
from pg_extended.Core import DynamicValue, AnimatedValue
from pg_extended.Types import callableLike

class Callback:
  def __init__(self, trigger: str, func: callableLike, staticArgs: dict[str, Any] = {}, extraArgKeys: list[str] | tuple[str] = ()):
    self.trigger = trigger
    self.func = func
    self.args = staticArgs
    self.resolvedArgs = {}
    self.extraArgKeys = extraArgKeys

  def setExtraArgs(self, args: list[Any] | tuple[Any]):
    for i in range(len(args)):
      self.args[self.extraArgKeys[i]] = args[i]

  def resolveArgs(self):
    self.resolvedArgs = {}

    if self.args is None: return None

    for key in self.args:
      val = self.args[key]

      if isinstance(val, (DynamicValue, AnimatedValue)):
        val.resolveValue()
        self.resolvedArgs[key] = val.value
      else:
        self.resolvedArgs[key] = val

  def call(self):
    self.resolveArgs()

    self.func(**self.resolvedArgs)
