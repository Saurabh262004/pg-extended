from typing import Any
from pg_extended.Core.Base import DynamicValue, AnimatedValue
from pg_extended.Types import CallableLike

class Callback:
  def __init__(self, triggers: list[str] | tuple[str], func: CallableLike, staticArgs: dict[str, Any] = None, extraArgKeys: dict[str, str] = None):
    self.triggers = triggers
    self.func = func
    self.staticArgs = staticArgs or {}
    self.resolvedArgs = {}
    self.extraArgKeys = extraArgKeys or {}
    self.totalArgs = {}

  def _setExtraArgs(self, args: dict[str, Any] = None):
    args = args or {}

    self.totalArgs = self.staticArgs.copy()

    for key, value in args.items():
      if key in self.extraArgKeys:
        self.totalArgs[self.extraArgKeys[key]] = value

  def resolveArgs(self):
    self.resolvedArgs = {}

    for key in self.totalArgs:
      val = self.totalArgs[key]

      if isinstance(val, (DynamicValue, AnimatedValue)):
        val.resolveValue()
        self.resolvedArgs[key] = val.value
      else:
        self.resolvedArgs[key] = val

  def call(self, extraArgs: dict[str, Any] = None):
    extraArgs = extraArgs or {}

    self._setExtraArgs(extraArgs)

    self.resolveArgs()

    self.func(**self.resolvedArgs)

class CallbackSet:
  def __init__(self, callbacks: list[Callback] | tuple[Callback]):
    self.callbacks = callbacks
    self.callbacksDict = {}

    for callback in self.callbacks:
      for tgr in callback.triggers:
        self.callbacksDict.setdefault(tgr, []).append(callback)

  def call(self, trigger: str, extraArgs: dict[str, Any] = None):
    if trigger not in self.callbacksDict: return None

    for callback in self.callbacksDict[trigger]:
      callback.call(extraArgs)
