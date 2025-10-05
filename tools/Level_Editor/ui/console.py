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
    }, colors.themes[sharedAssets.theme]['backdrop1']
  )

  importAtlasButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5),
        'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5),
        'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=10)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ),
    colors.themes[sharedAssets.theme]['secondary'],
    text='Import  Atlas',
    fontPath='Arial',
    textColor=colors.themes[sharedAssets.theme]['text'],
    onClick=setAtlas,
    onClickActuation='buttonUp'
  )

  atlasIndex = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=20),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=29)
    }, pg.Color(217, 217, 217)
  )

  textureGrid = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=50),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=50)
    }, pg.Color(217, 217, 217)
  )

  fileOptions = save = load = import_ = export = None

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

  def fileAnimStop():
    if fileOptions is not None:
      fileOptions.lazyUpdateOverride = False

      if not fileOptionsAnim.reverse:
        save.activeDraw = save.activeEvents = True
        load.activeDraw = load.activeEvents = True
        import_.activeDraw = import_.activeEvents = True
        export.activeDraw = export.activeEvents = True

    fileOptions.update()

  file = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
        'y': pgx.DynamicValue('number', 0),
        'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
        'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=6)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='File', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text'], onClick=fileAnimStart
  )

  fileOptionsAnim = pgx.AnimatedValue(
    (
      pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=6),
      pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=30)
    ), 200, 'start', 'easeInOut', fileAnimStop
  )

  fileOptions = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classNum', fileOptionsAnim, classAttribute='value')
    }, colors.themes[sharedAssets.theme]['backdrop1'], 7
  )

  save = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=30),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Save', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  load = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=50),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Load', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  import_ = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=70),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Import', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  export = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptions),
        'y': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'width': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptions, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Export', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  fileBack = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5)
    }, colors.themes[sharedAssets.theme]['primary']
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
