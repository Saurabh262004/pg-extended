import pygame as pg

def getGradient(colors: list[pg.Color | tuple[int, int, int] | tuple[int, int, int, int]], sizes: list[int], direction: str) -> pg.Surface:
  if direction in ('up', 'left'):
    colors.reverse()
    sizes.reverse()

  if direction in ('up', 'down'):
    w = 1
    h = sum(sizes)

    xL = [0] * len(colors)
    yL = sizes
  else:
    w = sum(sizes)
    h = 1

    xL = sizes
    yL = [0] * len(colors)

  surface = pg.Surface((w, h), pg.SRCALPHA)

  x = y = 0

  for i in range(len(colors)):
    pg.draw.line(surface, colors[i], (x, y), (x + xL[i], y + yL[i]))
    x += xL[i]
    y += yL[i]

  return surface
