import pygame as pg

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
