import pygame as pg
import pg_extended as pgx

class SceneManager:
  def addScene(self, scene: pgx.Game.Scene, sceneID: str) -> bool:
    if sceneID in self.scenes:
      print(f'A scene with ID: {sceneID} already exists. please enter a unique ID')
      return False

    if not scene.locked:
      print('Provided scene is not locked, switching the scene to locked state and removing its surface.')
      scene.locked = True
      scene.surface = None

    self.scenes[sceneID] = scene

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
        self.initiateActiveScene(self.screen)
        self.resetUI()

    return not interrupted

  def deactivateScene(self) -> bool:
    if self.activeScene is None:
      print('No scene is currently active.')
      return False

    self.activeScene = None

    if self.running:
      self.resetUI()

    return True

  def initiateActiveScene(self, surface: pg.Surface):
    if self.activeScene is not None and self.activeScene.locked:
      self.activeScene.initiate(surface)

