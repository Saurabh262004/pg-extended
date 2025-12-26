import pygame as pg

class ImgManipulation:
  # deforms the image to perfectly fit in the container
  @staticmethod
  def squish(image: pg.Surface, containerSize: tuple[int | float, int | float] | list[int | float], smoothscale: bool = True, scalePercent: int | None = 100) -> pg.Surface:
    if smoothscale:
      return pg.transform.smoothscale(
        image,
        (
          containerSize[0] * (scalePercent / 100),
          containerSize[1] * (scalePercent / 100)
        )
      )

    return pg.transform.scale(
      image,
      (
        containerSize[0] * (scalePercent / 100),
        containerSize[1] * (scalePercent / 100)
      )
    )

  # resizes the image to the smallest possible fit while preserving the original aspect ratio
  @staticmethod
  def fit(image: pg.Surface, containerSize: tuple[int | float, int | float] | list[int | float], smoothscale: bool = True, scalePercent: int | None = 100) -> pg.Surface:
    containerWidth, containerHeight = containerSize

    imageWidth, imageHeight = image.get_width(), image.get_height()

    scale = min(containerWidth / imageWidth, containerHeight / imageHeight) * (scalePercent / 100)

    newWidth = int(imageWidth * scale)
    newHeight = int(imageHeight * scale)

    if smoothscale:
      return pg.transform.smoothscale(image, (newWidth, newHeight))

    return pg.transform.scale(image, (newWidth, newHeight))

  # resizes the image to the largest possible fit while preserving the original aspect ratio
  @staticmethod
  def fill(image: pg.Surface, containerSize: tuple[int | float, int | float] | list[int | float], smoothscale: bool = True, scalePercent: int | None = 100) -> pg.Surface:
    containerWidth, containerHeight = containerSize

    imageWidth, imageHeight = image.get_width(), image.get_height()

    scale = max(containerWidth / imageWidth, containerHeight / imageHeight) * (scalePercent / 100)

    newWidth = int(imageWidth * scale)
    newHeight = int(imageHeight * scale)

    if smoothscale:
      return pg.transform.smoothscale(image, (newWidth, newHeight))

    return pg.transform.scale(image, (newWidth, newHeight))

  # returns an image with it's borders rounded.
  @staticmethod
  def roundImage(img: pg.Surface, radius: float) -> pg.Surface:
    w, h = img.get_size()

    mask = pg.Surface((w, h), pg.SRCALPHA)

    pg.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)

    result = pg.Surface((w, h), pg.SRCALPHA)

    result.blit(img, (0, 0))
    result.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    return result

  # make a 2xn or nx2 pixel surface with provided colors that can later be smoothscaled to get a color gradient
  @staticmethod
  def getGradient(colors: list[pg.Color | tuple[int, int, int] | tuple[int, int, int, int]], sizes: list[int], direction: str, thickness: int = 2) -> pg.Surface:
    if direction in ('up', 'left'):
      colors.reverse()
      sizes.reverse()

    if direction in ('up', 'down'):
      w = thickness
      h = sum(sizes)
    else:
      w = sum(sizes)
      h = thickness

    surface = pg.Surface((w, h), pg.SRCALPHA)

    if direction in ('up', 'down'):
      for i in range(len(colors)):
        pg.draw.rect(surface, colors[i], (0, sum(sizes[:i]), thickness, sizes[i]), 0)
    else:
      for i in range(len(colors)):
        pg.draw.rect(surface, colors[i], (sum(sizes[:i]), 0, sizes[i], thickness), 0)

    return surface
