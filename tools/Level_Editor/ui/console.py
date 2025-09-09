import pg_extended as pgx
from tools.Level_Editor.ui import colors

def add(app: pgx.Window):
  console = pgx.System(preLoadState=True)

  consoleFrame = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=30),
      'height': pgx.DynamicValue('classNum', app, classAttribute='screenHeight')
    }, colors.backdrop1
  )

  console.addElement(consoleFrame, 'consoleFrame')

  app.addSystem(console, 'console')

  app.setSystemZ('console', 1)
