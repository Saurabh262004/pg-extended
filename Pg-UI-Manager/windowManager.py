from typing import Iterable, Optional, Union, Dict, List
import pygame as pg
from modules.UI.UIElements import DynamicValue as DV, System

numType = Union[int, float]

class Window:
  def __init__(self, title: str, screenRes: Iterable[int], minRes: Optional[Iterable[int]] = (480, 270), customLoopProcess: Optional[callable] = None, customUpdateProcess: Optional[callable] = None, customEventHandler: Optional[callable] = None, fps : Optional[int] = 60):
    self.title = title
    self.screenRes = screenRes
    self.customLoopProcess = customLoopProcess
    self.customEventHandler = customEventHandler
    self.customUpdateProcess = customUpdateProcess
    self.minRes = minRes
    self.screenWidth = max(self.screenRes[0], self.minRes[0])
    self.screenHeight = max(self.screenRes[1], self.minRes[1])
    self.fps = fps
    self.running = False
    self.systems: Dict[str, System] = {}
    self.activeSystems: Dict[str, System] = {}
    self.systemZ: Dict[str, int] = {}
    self.loggedSystemSwitch = None
    self.customData = {}

  def addSystem(self, system: System, systemID: str) -> bool:
    if systemID in self.systems:
      print(f'A system with ID: {systemID} already exists. please enter a unique ID')
      return False

    if not system.locked:
      print('Provided system is not locked, switching the system to locked state and removing its surface.')
      system.locked = True
      system.surface = None

    if not 'mainSection' in system.elements:
      print('the system must have a section with id \"mainSection\"')
      return False

    system.elements['mainSection'].dimensions['width'] = DV('classNum', self, classAttr='screenWidth')
    system.elements['mainSection'].dimensions['height'] = DV('classNum', self, classAttr='screenHeight')

    self.systems[systemID] = system

    return True

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

  def openWindow(self):
    pg.init()

    self.time = pg.time
    self.clock = self.time.Clock()
    pg.display.set_caption(self.title)
    self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight), pg.RESIZABLE)

    self.__initiateActiveSystems(self.screen)

    self.running = True
    self.__resetUI()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].draw()

    self.secondResize = False
    while self.running:
      self.__handleEvents()

      if self.secondResize or self.__screenResized():
        self.secondResize = not self.secondResize
        self.__resetUI()

      self.screen.fill((0, 0, 0))

      if self.customLoopProcess is not None:
        self.customLoopProcess()

      for systemID in self.systemZ:
        if systemID in self.activeSystems:
          self.activeSystems[systemID].draw()

      pg.display.flip()
      self.clock.tick(self.fps)

    self.closeWindow()

  def closeWindow(self):
    self.running = False
    self.deactivateSystems('all')

    del self.screen
    del self.time
    del self.clock

    pg.quit()

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

        for systemID in self.systemZ:
          if systemID in self.activeSystems:
            cursorChangeTMP = self.activeSystems[systemID].handleEvents(event)

            if cursorChangeTMP == 'hand':
              cursorChange = cursorChangeTMP

        if cursorChange == 'hand':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

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

    if self.customUpdateProcess is not None:
      self.customUpdateProcess()

    for systemID in self.systemZ:
      if systemID in self.activeSystems:
        self.activeSystems[systemID].update()
