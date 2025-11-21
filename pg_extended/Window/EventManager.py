import pygame as pg

class EventManager:
  def handleEvents(self):
    if not self.running:
      return None

    for event in pg.event.get():
      if self.customEventHandler is not None:
        self.customEventHandler(event)

      if event.type == pg.QUIT:
        self.running = False
      else:
        cursorChange = 'arrow'

        if self.activeScene is not None:
          cursorChange = self.activeScene.handleEvents(event)

        for systemID in self.systemZ:
          if systemID in self.activeSystems:
            if cursorChange == 'arrow':
              cursorChange = self.activeSystems[systemID].handleEvents(event)
            else:
              self.activeSystems[systemID].handleEvents(event)

        if cursorChange == 'hand':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        elif cursorChange == 'arrow':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        elif cursorChange == 'ibeam':
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_IBEAM)
