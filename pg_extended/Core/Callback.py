from typing import Any
from pg_extended.Core import DynamicValue, AnimatedValue
from pg_extended.Types import callableLike

class Callback:
  def __init__(self, triggers: list[str] | tuple[str], func: callableLike, staticArgs: dict[str, Any] = {}, extraArgKeys: list[str] | tuple[str] = ()):
    self.triggers = triggers
    self.func = func
    self.args = staticArgs
    self.resolvedArgs = {}
    self.extraArgKeys = extraArgKeys

  def setExtraArgs(self, args: dict[str, Any] = {}):
    for key in args:
      if key in self.extraArgKeys:
        self.args[key] = args[key]

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

class CallbackSet:
  def __init__(self, callbacks: list[Callback] | tuple[Callback]):
    self.callbacks = callbacks
    self.callbacksDict = {}

    for callback in self.callbacks:
      for tgr in callback.triggers:
        self.callbacksDict.setdefault(tgr, []).append(callback)

  def resolveArgs(self):
    for callback in self.callbacks:
      callback.resolveArgs()

  def call(self, trigger: str, extraArgs: dict[str, Any] = {}):
    if trigger not in self.callbacksDict: return None

    for callback in self.callbacksDict[trigger]:
      callback.setExtraArgs(extraArgs)

    for callback in self.callbacksDict[trigger]:
      callback.call()
