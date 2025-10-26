from typing import Union
import pygame as pg

type Background = Union[pg.Color, pg.Surface]

type TileIdentifier = Union[tuple[int, int], str, tuple[int, int, int], tuple[int, int, int, int], pg.Color]
