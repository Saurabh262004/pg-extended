from typing import Iterable, Optional, Union, Dict, List
import pygame as pg
from pg_extended.Core import DynamicValue, AnimatedValue
from pg_extended.Game import Scene, ViewPort
from pg_extended.UI import System

'''
Window is a class that represents your main application window.
It is used to create and manage the main window of your application, handle events, and manage UI systems.

Parameters:
- [required] title:               The title of the window.
- [required] screenRes:           The resolution of the window (width, height).
- [Optional] minRes:              The minimum resolution of the window (default is (480, 270)).
- [Optional] customLoopProcess:   A custom function to be called in the main loop (default is None).
- [Optional] customUpdateProcess: A custom function to be called in the update process (default is None).
- [Optional] customEventHandler:  A custom function to handle events (default is None).

Usable methods:
- addSystem:         Adds a system to the window.
- activateSystems:   Activates the specified systems.
- deactivateSystems: Deactivates the specified systems.
- setSystemZ:        Sets the z-index of a system.
- changeTitle:       Changes the title of the window.
- openWindow:        Opens the main window and starts the main loop.
- closeWindow:       Closes the main window and cleans up resources.
'''
class Window:
  def __init__(self, title: str, screenRes: Iterable[int], minRes: Optional[Iterable[int]] = (480, 270), customLoopProcess: Optional[callable] = None, customUpdateProcess: Optional[callable] = None, customEventHandler: Optional[callable] = None, fps : Optional[int] = 60):
    self.title: str = title
    self.screenRes: Iterable[int] = screenRes
    self.customLoopProcess: Union[callable, None] = customLoopProcess
    self.customEventHandler: Union[callable, None] = customEventHandler
    self.customUpdateProcess: Union[callable, None] = customUpdateProcess
    self.minRes: Iterable[int] = minRes
    self.screenWidth: int = max(self.screenRes[0], self.minRes[0])
    self.screenHeight: int = max(self.screenRes[1], self.minRes[1])
    self.fps: int = fps

    self.running: bool = False
    self.systems: Dict[str, System] = {}
    self.activeSystems: Dict[str, System] = {}
    self.systemZ: Dict[str, int] = {}
    self.scenes: Dict[str, Scene] = {}
    self.activeScene: Scene = None
    self.viewPort: ViewPort = None
    self.customDynamicValues: List[DynamicValue] = []
    self.lazyDynamicValues: List[DynamicValue] = []
    self.customAnimatedValues: List[AnimatedValue] = []
    self.customData: dict = {}
    self.firstUpdate = True

  def addScene(self, scene: Scene, sceneID: str) -> bool:
    if sceneID in self.scenes:
      print(f'A scene with ID: {sceneID} already exists. please enter a unique ID')
      return False

    if not scene.locked:
      print('Provided scene is not locked, switching the scene to locked state and removing its surface.')
      scene.locked = True
      scene.surface = None

    self.scenes[sceneID] = scene

    return True

  def addSystem(self, system: System, systemID: str) -> bool:
    if systemID in self.systems:
      print(f'A system with ID: {systemID} already exists. please enter a unique ID')
      return False

    if not system.locked:
      print('Provided system is not locked, switching the system to locked state and removing its surface.')
      system.locked = True
      system.surface = None

    self.systems[systemID] = system

    return True

  def setActiveScene(self, sceneID: str) -> bool:
    interrupted = False

    if not self.scenes[sceneID]:
      print(f'A scene with ID: {sceneID} does not exist. Please provide a valid scene ID')
      interrupted = True
    elif self.scenes[sceneID] == self.activeScene:
      print(f'The scene with ID: {sceneID} is already active.')
      interrupted = True
    else:
      self.activeScene = self.scenes[sceneID]

      if self.running:
        self.__initiateActiveScene(self.screen)
        self.__resetUI()

    return not interrupted

  def activateSystems(self, systemIDs: Union[Iterable[str], str]) -> bool:
    interrupted = False

    if not isinstance(systemIDs, str):
      for systemID in systemIDs:
        if not systemID in self.systems:
          print(f'A system with ID: {systemID} does not exist. Automatically skipped this task.')
          interrupted = True
        elif systemID in self.activeSystems:
          print(f'The system with ID: {systemID} is already active.')
          interrupted = True
        else:
          self.activeSystems[systemID] = self.systems[systemID]
    else:
      if not systemIDs in self.systems:
        print(f'A system with ID: {systemIDs} does not exist. Please provide a valid system ID')
        interrupted = True
      elif systemIDs in self.activeSystems:
        print(f'The system with ID: {systemIDs} is already active.')
        interrupted = True
      else:
        self.activeSystems[systemIDs] = self.systems[systemIDs]

    if self.running:
      self.__initiateActiveSystems(self.screen)
      self.__resetUI()

    return not interrupted

  def deactivateScene(self) -> bool:
    if self.activeScene is None:
      print('No scene is currently active.')
      return False

    self.activeScene = None

    if self.running:
      self.__resetUI()

    return True

  def setViewPort(self, viewPort: ViewPort):
    self.viewPort = viewPort

    if self.running:
      self.viewPort.initiate(self.screen, self.activeScene)

  def deactivateSystems(self, systemIDs: Union[Iterable[str], str]) -> bool:
    interrupted = False

    if not isinstance(systemIDs, str):
      deleteSystems = []

      for systemID in systemIDs:
        if not systemID in self.activeSystems:
          print(f'A system with ID: {systemID} does not exist or is already deactivated. Automatically skipped this task.')
          interrupted = True
        else:
          self.activeSystems[systemID].locked = True
          del self.activeSystems[systemID].surface
          deleteSystems.append(systemID)

      for systemID in deleteSystems:
        del self.activeSystems[systemID]
    else:
      if systemIDs == 'all':
        for systemID in self.activeSystems:
          self.activeSystems[systemID].locked = True
          del self.activeSystems[systemID].surface

        self.activeSystems = []
      elif not systemIDs in self.systems:
        print(f'A system with ID: {systemIDs} does not exist or is already deactivated. Automatically skipped this task.')
        interrupted = True
      else:
        self.activeSystems[systemIDs].locked = True
        del self.activeSystems[systemIDs].surface
        del self.activeSystems[systemIDs]

    return not interrupted

  def __initiateActiveScene(self, surface: pg.Surface):
    if self.activeScene is not None and self.activeScene.locked:
      self.activeScene.initiate(surface)

  def __initiateActiveSystems(self, surface: pg.Surface):
    for systemID in self.activeSystems:
      if self.activeSystems[systemID].locked:
        self.activeSystems[systemID].initiate(surface)

  def setSystemZ(self, systemID: str, zIndex: int) -> Optional[bool]:
    keysToRemove = [key for key, value in self.systemZ.items() if value == zIndex]

    for key in keysToRemove:
      del self.systemZ[key]

    self.systemZ[systemID] = zIndex

    self.systemZ = dict(sorted(self.systemZ.items(), key=lambda item: item[1]))

  def changeTitle(self, title: str):
    self.title = title
    pg.display.set_caption(self.title)

  def __handleEvents(self):
    if not self.running:
      return None

    for event in pg.event.get():
      if self.customEventHandler is not None:
        self.customEventHandler(event)

      if event.type == pg.QUIT:
        self.running = False
      elif event.type == pg.VIDEORESIZE:
        new_width = max(self.minRes[0], event.w)
        new_height = max(self.minRes[1], event.h)
        self.screen = pg.display.set_mode((new_width, new_height), pg.RESIZABLE)
      else:
        cursorChange = 'arrow'

        if self.activeScene is not None:
          cursorChange = self.activeScene.handleEvents(event)

        for systemID in self.systemZ:
          if systemID in self.activeSystems:
            cursorChange = self.activeSystems[systemID].handleEvents(event)

        if cursorChange == 'hand':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        elif cursorChange == 'arrow':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        elif cursorChange == 'ibeam':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_IBEAM)

  def __updateLoop(self):
    self.__handleEvents()

    if self.secondResize or self.__screenResized():
      self.secondResize = not self.secondResize
      self.__resetUI()

    self.currentFPS = self.clock.get_fps()

    self.screen.fill((0, 0, 0))

    for dynamicValue in self.customDynamicValues:
      dynamicValue.resolveValue()

    for animatedValue in self.customAnimatedValues:
      animatedValue.resolveValue()

    if self.activeScene is not None:
      self.activeScene.update()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].update()

    if self.customLoopProcess is not None:
      self.customLoopProcess()

    if self.viewPort is not None:
      self.viewPort.update()

      if not self.viewPort.lazyRender:
        self.viewPort.renderScene()

      self.viewPort.draw()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].draw()

    self.firstUpdate = False
    pg.display.flip()
    self.clock.tick(self.fps)

  def openWindow(self):
    self.time = pg.time
    self.clock = self.time.Clock()
    self.currentFPS: int = self.clock.get_fps()

    pg.display.set_caption(self.title)

    self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight), pg.RESIZABLE)

    self.running = True
    self.secondResize = False

    self.__initiateActiveScene(self.screen)

    self.__initiateActiveSystems(self.screen)

    if self.viewPort is not None:
      self.viewPort.initiate(self.screen, self.activeScene)

    self.__resetUI()

    while self.running:
      self.__updateLoop()

    self.closeWindow()

  def closeWindow(self):
    self.running = False
    self.deactivateSystems('all')
    self.deactivateScene()

    del self.screen
    del self.time
    del self.clock

    pg.quit()

  def __screenResized(self) -> bool:
    if not self.running:
      return None

    tmpSW = self.screen.get_width()
    tmpSH = self.screen.get_height()

    if (self.screenWidth != tmpSW) or (self.screenHeight != tmpSH):
      self.screenWidth, self.screenHeight = self.screen.get_width(), self.screen.get_height()
      return True

    return False

  def __resetUI(self):
    if not self.running:
      return None

    for dynamicValue in self.lazyDynamicValues:
      dynamicValue.resolveValue()

    for animatedValue in self.customAnimatedValues:
      animatedValue.updateRestingPos()

    if self.customUpdateProcess is not None:
      self.customUpdateProcess()

    if self.activeScene is not None:
      self.activeScene.lazyUpdate()

    if self.viewPort is not None:
      self.viewPort.update()
      self.viewPort.renderScene()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].lazyUpdate()
