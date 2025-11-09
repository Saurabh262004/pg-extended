import pg_extended as pgx
from tools.Level_Editor.ui import colors
from tools.Level_Editor import sharedAssets

def add(app: pgx.Window):
  grid = pgx.System(preLoadState=True)

  gridFrame = pgx.Section(
    {
      'x': pgx.DynamicValue(app, 'screenWidth', percent=30),
      'y': pgx.DynamicValue(0),
      'width': pgx.DynamicValue(app, 'screenWidth', percent=70),
      'height': pgx.DynamicValue(app, 'screenHeight')
    }, colors.themes[sharedAssets.theme]['grid']
  )

  grid.addElement(gridFrame, 'gridFrame')

  app.addSystem(grid, 'grid')

  app.setSystemZ('grid', 0)
