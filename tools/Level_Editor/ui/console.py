from traceback import print_exc
from easygui import fileopenbox
import pygame as pg
import pg_extended as pgx
from tools.Level_Editor import sharedAssets
from tools.Level_Editor.ui import colors
from tools.Level_Editor.AtlasImporter import importAtlas

def setAtlas():
  try:
    atlasURL = fileopenbox(title='Select Texture Atlas Image', filetypes=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tga'])

    if atlasURL is None:
      print('No file selected')
      return

    atlas = importAtlas(atlasURL)

    if isinstance(atlas, pgx.TextureAtlas):
      sharedAssets.atlases.append(atlas)
  except Exception as e:
    print('Error importing atlas:', e)
    print_exc()
    sharedAssets.atlas = None

def add(app: pgx.Window):
  global setAtlas

  console = pgx.System(preLoadState=True)

  consoleFrame = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=30),
      'height': pgx.DynamicValue('classNum', app, classAttribute='screenHeight')
    }, colors.backdrop1
  )

  importAtlasButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5),
        'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5),
        'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=10.5)
      }, colors.primary, 7
    ),
    colors.secondary,
    text='Import  Atlas',
    fontPath='Arial',
    textColor=colors.text,
    onClick=setAtlas,
    onClickActuation='buttonUp'
  )

  atlasIndex = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=20.5),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=60)
    }, pg.Color(217, 217, 217)
  )

  fileOptions = save = load = import_ = export = None

  def fileAnimStop():
    if fileOptions is not None:
      fileOptions.lazyUpdateOverride = False

      if not fileOptionsAnim.reverse:
        save.activeDraw = save.activeEvents = True
        load.activeDraw = load.activeEvents = True
        import_.activeDraw = import_.activeEvents = True
        export.activeDraw = export.activeEvents = True

    fileOptions.update()

  fileOptionsAnim = pgx.AnimatedValue(
    (
      pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=10),
      pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=60)
    ), 200, 'start', 'easeInOut', fileAnimStop
  )

  fileOptions = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classNum', fileOptionsAnim, classAttribute='value')
    }, colors.backdrop1, 7
  )

  def fileAnimStart():
    fileOptions.lazyUpdateOverride = True

    if fileOptionsAnim.hasPlayedOnce:
      fileOptionsAnim.trigger(not fileOptionsAnim.reverse)
    else:
      fileOptionsAnim.trigger()

    if fileOptionsAnim.reverse:
      save.activeDraw = save.activeEvents = False
      load.activeDraw = load.activeEvents = False
      import_.activeDraw = import_.activeEvents = False
      export.activeDraw = export.activeEvents = False

  save = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=30),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.primary, 7
    ), colors.secondary, text='Save', fontPath='Arial', textColor=colors.text
  )

  load = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=50),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.primary, 7
    ), colors.secondary, text='Load', fontPath='Arial', textColor=colors.text
  )

  import_ = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=70),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.primary, 7
    ), colors.secondary, text='Import', fontPath='Arial', textColor=colors.text
  )

  export = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.primary, 7
    ), colors.secondary, text='Export', fontPath='Arial', textColor=colors.text
  )

  fileBack = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5)
    }, colors.primary
  )

  file = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
        'y': pgx.DynamicValue('number', 0),
        'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
        'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=10)
      }, colors.primary, 7
    ), colors.secondary, text='File', fontPath='Arial', textColor=colors.text, onClick=fileAnimStart
  )

  textureGrid = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('callable', lambda section: section.height - section.width, consoleFrame),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width')
    }, pg.Color(217, 217, 217)
  )

  save.activeDraw = False
  load.activeDraw = False
  import_.activeDraw = False
  export.activeDraw = False

  console.addElement(consoleFrame, 'consoleFrame')
  console.addElement(importAtlasButton, 'importAtlas')
  console.addElement(atlasIndex, 'switchAtlas')
  console.addElement(fileBack, 'fileBack')
  console.addElement(fileOptions, 'fileOptions')
  console.addElement(save, 'save')
  console.addElement(load, 'load')
  console.addElement(import_, 'import')
  console.addElement(export, 'export')
  console.addElement(file, 'file')
  console.addElement(textureGrid, 'textureGrid')

  app.customAnimatedValues.append(fileOptionsAnim)

  app.addSystem(console, 'console')

  app.setSystemZ('console', 1)
