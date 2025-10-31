from pg_extended.UI.Elements.Gradient import getGradient
from pg_extended.UI.Elements.Section import Section
from pg_extended.UI.Elements.Circle import Circle
from pg_extended.UI.Elements.TextBox import TextBox
from pg_extended.UI.Elements.Button import Button
from pg_extended.UI.Elements.Toggle import Toggle
from pg_extended.UI.Elements.Slider import Slider
from pg_extended.UI.Elements.TextInput import TextInput

from typing import Union

type UIElement = Union[Section, Circle, TextBox, Button, Toggle, Slider, TextInput]
