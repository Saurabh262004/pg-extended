import pg_extended as pgx
from tools.Level_Editor.ui import colors
from tools.Level_Editor import sharedAssets

def add(app: pgx.Window):
  grid = pgx.System(preLoadState=True)

  gridFrame = pgx.Section(
    {
      'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=30),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=70),
      'height': pgx.DynamicValue('classNum', app, classAttribute='screenHeight')
    }, colors.themes[sharedAssets.theme]['grid']
  )

  grid.addElement(gridFrame, 'gridFrame')

  app.addSystem(grid, 'grid')

  app.setSystemZ('grid', 0)
