from typing import Union, Optional, Callable, Dict, Any

numType = Union[int, float]

DIMENSION_REFERENCE_TYPES = ('number', 'percent', 'dictNum', 'classNum', 'dictPer', 'classPer', 'customCallable')

class DynamicValue:
  def __init__(self, referenceType: str, reference: Union[Callable, numType, Dict[str, numType], object], callableParameters: Optional[Any] = None, dictKey: Optional[str] = None, classAttr: Optional[str] = None, percent: Optional[numType] = None):
    self.referenceType = referenceType
    self.reference = reference
    self.callableParameters = callableParameters
    self.dictKey = dictKey
    self.classAttr = classAttr
    self.percent = percent
    self.value = None
    self.resolveValue: Callable

    if not self.referenceType in DIMENSION_REFERENCE_TYPES:
      raise ValueError(f'Invalid dimType value received, value must be one of the following: {DIMENSION_REFERENCE_TYPES}')

    if (self.referenceType == 'customCallable') and not callable(self.reference):
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

    if self.referenceType == 'number':
      self.resolveValue = self.__getByNumber
    elif self.referenceType == 'percent':
      self.resolveValue = self.__getByPercent
    elif self.referenceType == 'customCallable':
      self.resolveValue = self.__getByCustomCallable
    elif self.referenceType == 'dictNum':
      self.resolveValue = self.__getByDictNum
    elif self.referenceType == 'dictPer':
      self.resolveValue = self.__getByDictPer
    elif self.referenceType == 'classNum':
      self.resolveValue = self.__getByClassNum
    elif self.referenceType == 'classPer':
      self.resolveValue = self.__getByClassPer

    self.resolveValue()

  def __getByNumber(self):
    self.value = self.reference

  def __getByPercent(self):
    self.value = self.reference * (self.percent / 100)

  def __getByCustomCallable(self):
    if not self.callableParameters is None:
      self.value = self.reference(self.callableParameters)
    else:
      self.value = self.reference()

  def __getByDictNum(self):
    self.value = self.reference[self.dictKey]

  def __getByDictPer(self):
    self.value = self.reference[self.dictKey] * (self.percent / 100)

  def __getByClassNum(self):
    self.value = getattr(self.reference, self.classAttr, 0)

  def __getByClassPer(self):
    self.value = getattr(self.reference, self.classAttr, 0) * (self.percent / 100)
