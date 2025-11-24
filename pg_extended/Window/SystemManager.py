import pygame as pg
import pg_extended as pgx

class SystemManager:
  def addSystem(self, system: pgx.UI.System, systemID: str) -> bool:
    if systemID in self.systems:
      print(f'A system with ID: {systemID} already exists. please enter a unique ID')
      return False

    if not system.locked:
      print('Provided system is not locked, switching the system to locked state and removing its surface.')
      system.locked = True
      system.surface = None

    self.systems[systemID] = system

    return True

  def activateSystems(self, systemIDs: list[str] | tuple[str] | str) -> bool:
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
      self.initiateActiveSystems(self.screen)
      self.resetUI()

    return not interrupted

  def deactivateSystems(self, systemIDs: list[str] | tuple[str] | str) -> bool:
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

        self.activeSystems = {}
      elif not systemIDs in self.systems:
        print(f'A system with ID: {systemIDs} does not exist or is already deactivated. Automatically skipped this task.')
        interrupted = True
      else:
        self.activeSystems[systemIDs].locked = True
        del self.activeSystems[systemIDs].surface
        del self.activeSystems[systemIDs]

    return not interrupted

  def setSystemZ(self, systemID: str, zIndex: int) -> bool | None:
    keysToRemove = [key for key, value in self.systemZ.items() if value == zIndex]

    for key in keysToRemove:
      del self.systemZ[key]

    self.systemZ[systemID] = zIndex

    self.systemZ = dict(sorted(self.systemZ.items(), key=lambda item: item[1]))

  def initiateActiveSystems(self, surface: pg.Surface):
    for systemID in self.activeSystems:
      if self.activeSystems[systemID].locked:
        self.activeSystems[systemID].initiate(surface)
