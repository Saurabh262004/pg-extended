import types
import pygame as pg

type Background = pg.Color | pg.Surface

type TileIdentifier = tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, int] | pg.Color | str

type callableLike = types.FunctionType | types.BuiltinFunctionType | types.MethodType
