from typing import Iterable, Optional
from pygame import Surface as pgSurface, transform as pgTransform

# maps a number from one range to another
def mapRange(num: float, start1: float, start2: float, end1: float, end2: float) -> float:
  # return the mid-point of the end range if the start1 and start2 are the same
  if start1 == start2:
    return (end1 + end2) / 2

  return end1 + (num - start1) * (end2 - end1) / (start2 - start1)

# check if all the values are in an iterable if yes return True else return False
def allIn(values: Iterable, itr: Iterable) -> bool:
  for v in values:
    if not v in itr:
      return False
  return True

# deforms the image to perfectly fit in the container
def squish(image: pgSurface, containerSize: Iterable, scalePercent: Optional[int] = 100) -> pgSurface:
  return pgTransform.smoothscale(
    image,
    (
      containerSize[0] * (scalePercent / 100),
      containerSize[1] * (scalePercent / 100)
    )
  )

# resizes the image to the smallest possible fit while preserving the original aspect ratio
def fit(image: pgSurface, containerSize: Iterable, scalePercent: Optional[int] = 100) -> pgSurface:
  containerWidth, containerHeight = containerSize

  imageWidth, imageHeight = image.get_width(), image.get_height()

  scale = min(containerWidth / imageWidth, containerHeight / imageHeight) * (scalePercent / 100)

  newWidth = int(imageWidth * scale)
  newHeight = int(imageHeight * scale)

  return pgTransform.smoothscale(image, (newWidth, newHeight))

# resizes the image to the largest possible fit while preserving the original aspect ratio
def fill(image: pgSurface, containerSize: Iterable, scalePercent: Optional[int] = 100) -> pgSurface:
  containerWidth, containerHeight = containerSize

  imageWidth, imageHeight = image.get_width(), image.get_height()

  scale = max(containerWidth / imageWidth, containerHeight / imageHeight) * (scalePercent / 100)

  newWidth = int(imageWidth * scale)
  newHeight = int(imageHeight * scale)

  return pgTransform.smoothscale(image, (newWidth, newHeight))
