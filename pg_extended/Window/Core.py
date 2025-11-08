from typing import Iterable, Optional, Union, Dict
import pg_extended as pgx

from .SystemManager import SystemManager
from .SceneManager import SceneManager
from .EventManager import EventManager
from .MainLoop import MainLoop
from .Lifecycle import Lifecycle
from .Utility import Utility

class Window(SystemManager, SceneManager, EventManager, MainLoop, Lifecycle, Utility):
  def __init__(self, title: str, screenRes: Iterable[int], customLoopProcess: Optional[callable] = None, customUpdateProcess: Optional[callable] = None, customEventHandler: Optional[callable] = None, customDrawProcess: Optional[callable] = None, fps : Optional[int] = 60):
    self.title: str = title
    self.screenRes: Iterable[int] = screenRes
    self.customLoopProcess: Union[callable, None] = customLoopProcess
    self.customEventHandler: Union[callable, None] = customEventHandler
    self.customUpdateProcess: Union[callable, None] = customUpdateProcess
    self.customDrawProcess: Union[callable, None] = customDrawProcess
    self.screenWidth: int = self.screenRes[0]
    self.screenHeight: int = self.screenRes[1]
    self.fps: int = fps

    self.running: bool = False
    self.systems: Dict[str, pgx.UI.System] = {}
    self.activeSystems: Dict[str, pgx.Game.System] = {}
    self.systemZ: Dict[str, int] = {}
    self.scenes: Dict[str, pgx.Game.Scene] = {}
    self.activeScene: pgx.Game.Scene = None
    self.viewPort: pgx.Game.ViewPort = None
    self.customDynamicValues: Dict[str, pgx.Core.DynamicValue] = {}
    self.lazyDynamicValues: Dict[str, pgx.Core.DynamicValue] = {}
    self.customAnimatedValues: Dict[str, pgx.Core.AnimatedValue] = {}
    self.customData: dict = {}
    self.firstUpdate = True
