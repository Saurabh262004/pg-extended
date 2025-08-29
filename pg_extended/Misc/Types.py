from typing import Union
import pygame as pg
from pg_extended.UI.Elements import *
from pg_extended.Game.Elements import *

BackgroundType = Union[pg.Color, pg.Surface]

UIElementType = Union[Section, Circle, TextBox, Button, Toggle, Slider, TextInput]

TileIdentifierType = Union[tuple[int, int], str, tuple[int, int, int], tuple[int, int, int, int], pg.Color]

GameElementType = Union[TextureAtlas, Level, Entity, Player]
