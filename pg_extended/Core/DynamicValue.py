from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pg_extended.Types import callableLike
import types

if TYPE_CHECKING:
  from pg_extended.Core.AnimatedValue import AnimatedValue

type reference = int | float | dict | object | callableLike | str | DynamicValue | AnimatedValue

class DynamicValue:
  def __init__(self, ref: reference, lookup: str | None = None, args: dict[str, Any] | None = None, percent: int | float | None = None):
    self.reference = ref
    self.lookup = lookup
    self.args = args
    self.percent = percent
    self.value: Any = None
    self.resolveValue: callableLike = None

    self.assignResolveMethod()

    self.resolveValue()

  def _IFPer(self):
    self.value = self.reference / 100 * self.percent

  def _dictLookup(self):
    self.value = self.reference[self.lookup]

  def _dictLookupPer(self):
    self.value = self.reference[self.lookup] / 100 * self.percent

  def _CV(self):
    self.reference.resolveValue()
    self.value = self.reference.value

  def _CVPer(self):
    self.reference.resolveValue()
    self.value = self.reference.value / 100 * self.percent

  def _call(self):
    self.value = self.reference()

  def _callPer(self):
    self.value = self.reference() / 100 * self.percent

  def _callArgs(self):
    self.value = self.reference(**self.args)

  def _callArgsPer(self):
    self.value = self.reference(**self.args) / 100 * self.percent

  def _objLookup(self):
    self.value = getattr(self.reference, self.lookup)

  def _objLookupPer(self):
    self.value = getattr(self.reference, self.lookup) / 100 * self.percent

  def _direct(self):
    self.value = self.reference

  def assignResolveMethod(self):
    from pg_extended.Core.AnimatedValue import AnimatedValue

    # numbers with a percent value given
    if isinstance(self.reference, (int, float)) and self.percent is not None:
      self.resolveValue = self._IFPer

    # dicts
    elif isinstance(self.reference, dict) and self.lookup is not None:
      if self.percent is None:
        self.resolveValue = self._dictLookup
      else:
        self.resolveValue = self._dictLookupPer

    # DV or AV
    elif isinstance(self.reference, DynamicValue) or isinstance(self.reference, AnimatedValue):
      if self.percent is None:
        self.resolveValue = self._CV
      else:
        self.resolveValue = self._CVPer

    # look for callable at the very end
    elif isinstance(self.reference, (types.FunctionType | types.BuiltinFunctionType | types.MethodType)):
      if self.args is None:
        if self.percent is None:
          self.resolveValue = self._call
        else:
          self.resolveValue = self._callPer
      else:
        if self.percent is None:
          self.resolveValue = self._callArgs
        else:
          self.resolveValue = self._callArgsPer

    # anything else left and lookup is provided, assume it's a class + attribute
    elif isinstance(self.lookup, str):
      if self.percent is None:
        self.resolveValue = self._objLookup
      else:
        self.resolveValue = self._objLookupPer

    # dump everything else into direct
    else:
      self.resolveValue = self._direct
