import pygame as pg
import pg_extended as pgx

def addOverlaySystem(window: pgx.Window):
  overlaySystem = pgx.System(preLoadState=True)

  menuButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('number', 10),
        'y': pgx.DynamicValue('number', 10),
        'width': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=10),
        'height': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=5)
      }, pg.Color(124, 173, 217), 4
    ), pg.Color(75, 142, 203),
    text='Menu',
    fontPath='Helvetica',
    textColor=pg.Color(247, 245, 244),
    onClick=lambda: print('Menu button clicked')
  )

  overlaySystem.addElement(menuButton, 'menuButton')

  window.addSystem(overlaySystem, 'overlay')
