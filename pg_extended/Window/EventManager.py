import pygame as pg

CURSOR_CONSTANTS = {
  None: pg.SYSTEM_CURSOR_ARROW,
  'arrow': pg.SYSTEM_CURSOR_ARROW,
  'hand': pg.SYSTEM_CURSOR_HAND,
  'ibeam': pg.SYSTEM_CURSOR_IBEAM
}

class EventManager:
  @staticmethod
  def setCursor(cursor):
    pg.mouse.set_cursor(cursor)

  def handleEvents(self):
    if not self.running:
      return None

    for event in pg.event.get():
      if self.customEventHandler is not None:
        self.customEventHandler(event)

      if event.type == pg.QUIT:
        self.running = False
      else:
        cursorChange = None

        if self.activeScene is not None:
          cursorChange = self.activeScene.handleEvents(event)

        for systemID in self.systemZ:
          if systemID in self.activeSystems:
            if cursorChange is None:
              cursorChange = self.activeSystems[systemID].handleEvents(event)
            else:
              self.activeSystems[systemID].handleEvents(event)

        self.setCursor(CURSOR_CONSTANTS[cursorChange])
