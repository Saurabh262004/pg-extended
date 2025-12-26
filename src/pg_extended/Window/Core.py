from pg_extended.Types import CallableLike
import pg_extended as pgx

from .SystemManager import SystemManager
from .SceneManager import SceneManager
from .EventManager import EventManager
from .MainLoop import MainLoop
from .Lifecycle import Lifecycle
from .Utility import Utility

class Window(SystemManager, SceneManager, EventManager, MainLoop, Lifecycle, Utility):
  def __init__(self, title: str, screenRes: list[int] | tuple[int, int], customLoopProcess: CallableLike | None = None, customUpdateProcess: CallableLike | None = None, customEventHandler: CallableLike | None = None, customDrawProcess: CallableLike | None = None, fps : int | None = 60):
    self.title: str = title
    self.screenRes: list[int] | tuple[int, int] = screenRes
    self.customLoopProcess: CallableLike | None = customLoopProcess
    self.customEventHandler: CallableLike | None = customEventHandler
    self.customUpdateProcess: CallableLike | None = customUpdateProcess
    self.customDrawProcess: CallableLike | None = customDrawProcess
    self.screenWidth: int = self.screenRes[0]
    self.screenHeight: int = self.screenRes[1]
    self.fps: int = fps

    self.running: bool = False
    self.systems: dict[str, pgx.UI.System] = {}
    self.activeSystems: dict[str, pgx.UI.System] = {}
    self.systemZ: dict[str, int] = {}
    self.scenes: dict[str, pgx.Game.Scene] = {}
    self.activeScene: pgx.Game.Scene = None
    self.viewPort: pgx.Game.ViewPort = None
    self.customDynamicValues: dict[str, pgx.Core.DynamicValue] = {}
    self.lazyDynamicValues: dict[str, pgx.Core.DynamicValue] = {}
    self.customAnimatedValues: dict[str, pgx.Core.AnimatedValue] = {}
    self.customData: dict = {}
    self.firstUpdate = True
