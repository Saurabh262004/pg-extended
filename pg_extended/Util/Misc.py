class Misc:
  # maps a number from one range to another
  @staticmethod
  def mapRange(num: float, start1: float, start2: float, end1: float, end2: float) -> float:
    # return the mid-point of the end range if the start1 and start2 are the same
    if start1 == start2:
      return (end1 + end2) / 2

    return end1 + (num - start1) * (end2 - end1) / (start2 - start1)

  # check if all the values are in an iterable if yes return True else return False
  @staticmethod
  def allIn(values: list | tuple, itr: list | tuple) -> bool:
    for v in values:
      if not v in itr:
        return False
    return True
