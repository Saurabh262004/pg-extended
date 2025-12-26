from pg_extended.Game.Elements.TextureAtlas import TextureAtlas
from pg_extended.Game.Elements.SpriteAnimation import SpriteAnimation
from pg_extended.Game.Elements.Entity import Entity
from pg_extended.Game.Elements.Player import Player
from pg_extended.Game.Elements.Level import Level

from typing import Union

type GameElement = Union[TextureAtlas, SpriteAnimation, Entity, Player, Level]
