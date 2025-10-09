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
    print('Error importing atlas:\n', e)
    print_exc()

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
        'x': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=2.5),
        'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5),
        'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=5)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ),
    colors.themes[sharedAssets.theme]['secondary'],
    text='Import  Atlas',
    fontPath='Arial',
    textColor=colors.themes[sharedAssets.theme]['text'],
    onClick=setAtlas,
    onClickActuation='buttonUp'
  )

  atlasList = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=10),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=39)
    }, pg.Color(217, 217, 217)
  )

  tilesGrid = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=50),
      'width': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='height', percent=50)
    }, pg.Color(217, 217, 217)
  )

  fileOptionsSection = saveLevelButton = loadLevelButton = importLevelButton = exportLevelButton = None

  def fileAnimStart():
    fileOptionsSection.lazyUpdateOverride = True

    if fileOptionsAnim.hasPlayedOnce:
      fileOptionsAnim.trigger(not fileOptionsAnim.reverse)
    else:
      fileOptionsAnim.trigger()

    if fileOptionsAnim.reverse:
      saveLevelButton.activeDraw = saveLevelButton.activeEvents = False
      loadLevelButton.activeDraw = loadLevelButton.activeEvents = False
      importLevelButton.activeDraw = importLevelButton.activeEvents = False
      exportLevelButton.activeDraw = exportLevelButton.activeEvents = False

  def fileAnimStop():
    if fileOptionsSection is not None:
      fileOptionsSection.lazyUpdateOverride = False

      if not fileOptionsAnim.reverse:
        saveLevelButton.activeDraw = saveLevelButton.activeEvents = True
        loadLevelButton.activeDraw = loadLevelButton.activeEvents = True
        importLevelButton.activeDraw = importLevelButton.activeEvents = True
        exportLevelButton.activeDraw = exportLevelButton.activeEvents = True

    fileOptionsSection.update()

  fileOptionsTrigger = pgx.Button(
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

  fileOptionsSection = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classNum', fileOptionsAnim, classAttribute='value')
    }, colors.themes[sharedAssets.theme]['backdrop1'], 7
  )

  saveLevelButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptionsSection),
        'y': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=30),
        'width': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Save', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  loadLevelButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptionsSection),
        'y': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=50),
        'width': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Load', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  importLevelButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptionsSection),
        'y': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=70),
        'width': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Import', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  exportLevelButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda section: (section.x + (section.width / 100) * 5), fileOptionsSection),
        'y': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=90),
        'width': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=90),
        'height': pgx.DynamicValue('classPer', fileOptionsSection, classAttribute='width', percent=15)
      }, colors.themes[sharedAssets.theme]['primary'], 7
    ), colors.themes[sharedAssets.theme]['secondary'], text='Export', fontPath='Arial', textColor=colors.themes[sharedAssets.theme]['text']
  )

  fileOptionsTriggerBack = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', consoleFrame, classAttribute='width'),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=50),
      'height': pgx.DynamicValue('classPer', consoleFrame, classAttribute='width', percent=5)
    }, colors.themes[sharedAssets.theme]['primary']
  )

  saveLevelButton.activeDraw = False
  loadLevelButton.activeDraw = False
  importLevelButton.activeDraw = False
  exportLevelButton.activeDraw = False

  console.addElements(
    {
      'consoleFrame': consoleFrame,
      'importAtlasButton': importAtlasButton,
      'atlasList': atlasList,
      'fileOptionsTriggerBack': fileOptionsTriggerBack,
      'fileOptionsSection': fileOptionsSection,
      'saveLevelButton': saveLevelButton,
      'loadLevelButton': loadLevelButton,
      'importLevelButton': importLevelButton,
      'exportLevelButton': exportLevelButton,
      'fileOptionsTrigger': fileOptionsTrigger,
      'tilesGrid': tilesGrid
    }
  )

  app.customAnimatedValues.append(fileOptionsAnim)

  app.addSystem(console, 'console')

  app.setSystemZ('console', 1)
