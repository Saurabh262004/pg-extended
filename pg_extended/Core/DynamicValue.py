from typing import Union, Optional, Callable, Dict, Any

REFERENCE_TYPES = ('number', 'percent', 'dictNum', 'classNum', 'dictPer', 'classPer', 'callable')

'''
DynamicValue is a class that allows you to create dynamic values that can change based on different reference types.

It supports the following reference types:
- 'number':   A static number value.
- 'percent':  A percentage of a static number value.
- 'dictNum':  A number value from a dictionary using a specified key.
- 'classNum': A number value from a class attribute.
- 'dictPer':  A percentage of a number value from a dictionary using a specified key.
- 'classPer': A percentage of a number value from a class attribute.
- 'callable': A callable that returns a value.
-             You can also specify parameters for the callable.

Parameters:
- [required] referenceType:      The type of the reference (one of the REFERENCE_TYPES).
- [required] reference:          The reference value, which can be a number, dictionary, class, or callable.
- [Optional] callableParameters: Parameters to pass to the callable function (default is None).
- [Optional] dictKey:            The key to use when accessing a value from a dictionary (default is None).
- [Optional] classAttr:          The attribute name to use when accessing a value from a class (default is None).
- [Optional] percent:            The percentage value to use when calculating a percentage (default is None).

Useable methods:
- resolveValue: Calculates the value based on the reference type and updates the `value` attribute.
'''
class DynamicValue:
  def __init__(self, referenceType: str, reference: Union[Callable, float, Dict[str, float], object], callableParameters: Optional[Any] = None, dictKey: Optional[str] = None, classAttribute: Optional[str] = None, percent: Optional[float] = None):
    self.referenceType = referenceType
    self.reference = reference
    self.callableParameters = callableParameters
    self.dictKey = dictKey
    self.classAttr = classAttribute
    self.percent = percent
    self.value = None
    self.resolveValue: Callable = None

    if not self.referenceType in REFERENCE_TYPES:
      raise ValueError(f'Invalid dimType value received, value must be one of the following: {REFERENCE_TYPES}')

    if (self.referenceType == 'callable') and not callable(self.reference):
      raise ValueError('If referenceType is custumCallable then reference must be callable')

    if (self.referenceType == 'dictNum' or self.referenceType == 'dictPer') and not (isinstance(self.reference, dict)):
      raise ValueError('If referenceType is dictNum or dictPer then given reference must be a dict object')

    if (self.referenceType == 'dictNum' or self.referenceType == 'dictPer') and (self.dictKey is None):
      raise ValueError('If referenceType is dictNum or dictPer then dictKey must be defined')

    if (self.referenceType == 'classNum' or self.referenceType == 'classPer') and not (isinstance(self.reference, object)):
      raise ValueError('If referenceType is classNum or classPer then given reference must be an object')

    if (self.referenceType == 'classNum' or self.referenceType == 'classPer') and (self.classAttr is None):
      raise ValueError('If referenceType is classNum or classPer then classAttr must be defined')

    if (self.referenceType == 'percent' or self.referenceType == 'dictPer' or self.referenceType == 'classPer') and (self.percent is None):
      raise ValueError('If referenceType is percent, dictPer or classPer percent must be defined')

    self.assignResolveMethod()

    self.resolveValue()

  def __getByNumber(self):
    self.value = self.reference

  def __getByPercent(self):
    self.value = self.reference * (self.percent / 100)

  def __getByCallableWithParams(self):
    self.value = self.reference(self.callableParameters)

  def __getByCallableWithoutParams(self):
    self.value = self.reference()

  def __getByDictNum(self):
    self.value = self.reference[self.dictKey]

  def __getByDictPer(self):
    self.value = self.reference[self.dictKey] * (self.percent / 100)

  def __getByClassNum(self):
    self.value = getattr(self.reference, self.classAttr, 0)

  def __getByClassPer(self):
    self.value = getattr(self.reference, self.classAttr, 0) * (self.percent / 100)

  def assignResolveMethod(self):
    if self.referenceType == 'number':
      self.resolveValue = self.__getByNumber
    elif self.referenceType == 'percent':
      self.resolveValue = self.__getByPercent
    elif self.referenceType == 'callable' and self.callableParameters is None:
      self.resolveValue = self.__getByCallableWithoutParams
    elif self.referenceType == 'callable':
      self.resolveValue = self.__getByCallableWithParams
    elif self.referenceType == 'dictNum':
      self.resolveValue = self.__getByDictNum
    elif self.referenceType == 'dictPer':
      self.resolveValue = self.__getByDictPer
    elif self.referenceType == 'classNum':
      self.resolveValue = self.__getByClassNum
    elif self.referenceType == 'classPer':
      self.resolveValue = self.__getByClassPer
