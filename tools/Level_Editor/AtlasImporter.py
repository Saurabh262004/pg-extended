from typing import Optional
import os
from math import floor
import pygame as pg
import pg_extended as pgx

# initialize stuff globally for access in other functions
atlasDetails = {
  'tileWidth': {'set': False, 'value': 16},
  'tileHeight': {'set': False, 'value': 16},
  'paddingX': {'set': False, 'value': 0},
  'paddingY': {'set': False, 'value': 0},
  'tilestOffsetX': {'set': False, 'value': 0},
  'tilestOffsetY': {'set': False, 'value': 0}
}

window = None
system = None
atlasImage = None
textureSection = None
controlPanel = None
doneButton = None
atlas = None
initialMousePose = None
dragging = False

def eventLoop(event: pg.event.Event):
  global initialMousePose, dragging, textureSection
  update = False

  if event.type == pg.MOUSEWHEEL:
    if event.y > 0:
      textureSection.backgroundSizePercent *= 1.2
    else:
      textureSection.backgroundSizePercent /= 1.2

    update = True

  elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
    initialMousePose = pg.mouse.get_pos()
    dragging = True

  elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
    dragging = False

  elif dragging and event.type == pg.MOUSEMOTION:
    currentMousePos = pg.mouse.get_pos()
    mouseDiffX = currentMousePos[0] - initialMousePose[0]
    mouseDiffY = currentMousePos[1] - initialMousePose[1]

    textureSection.backgroundOffset[0] += mouseDiffX
    textureSection.backgroundOffset[1] += mouseDiffY

    initialMousePose = currentMousePos
    update = True

  elif event.type == pg.KEYDOWN:
    if event.key == pg.K_UP or event.key == pg.K_w:
      textureSection.backgroundOffset[1] += textureSection.drawImage.get_height() / 20
      update = True
    elif event.key == pg.K_DOWN or event.key == pg.K_s:
      textureSection.backgroundOffset[1] -= textureSection.drawImage.get_height() / 20
      update = True
    elif event.key == pg.K_LEFT or event.key == pg.K_a:
      textureSection.backgroundOffset[0] += textureSection.drawImage.get_width() / 20
      update = True
    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
      textureSection.backgroundOffset[0] -= textureSection.drawImage.get_width() / 20
      update = True
    elif event.key == pg.K_r:
      textureSection.backgroundSizePercent = 100
      textureSection.backgroundOffset = [0, 0]
      update = True

  if update:
    textureSection.update()

def drawLoop():
  textureX = textureSection.imageX
  textureY = textureSection.imageY

  ogTextureWidth = atlasImage.get_width()
  ogTextureHeight = atlasImage.get_height()

  textureWidth = textureSection.drawImage.get_width()
  textureHeight = textureSection.drawImage.get_height()

  textureWidthChange = textureWidth / ogTextureWidth
  textureHeightChange = textureHeight / ogTextureHeight

  tileWidth = atlasDetails['tileWidth']['value'] * textureWidthChange
  tileHeight = atlasDetails['tileHeight']['value'] * textureHeightChange

  paddingX = atlasDetails['paddingX']['value'] * textureWidthChange
  paddingY = atlasDetails['paddingY']['value'] * textureHeightChange

  textureOffsetX = atlasDetails['tilestOffsetX']['value'] * textureWidthChange
  textureOffsetY = atlasDetails['tilestOffsetY']['value'] * textureHeightChange

  totalTilesX = floor((textureWidth - textureOffsetX) / (tileWidth + paddingX))
  totalTilesY = floor((textureHeight - textureOffsetY) / (tileHeight + paddingY))

  for x in range(totalTilesX):
    for y in range(totalTilesY):
      pg.draw.rect(
        window.screen,
        pg.Color(255, 255, 255),
        pg.Rect(
          textureX + textureOffsetX + (x * (tileWidth + paddingX)),
          textureY + textureOffsetY + (y * (tileHeight + paddingY)),
          tileWidth,
          tileHeight
        ),
        1
      )

def inputOnChange(inputValue: str, inputType: str):
  if inputType == 'tileWidth':
    defaultValue = 16
  elif inputType == 'tileHeight':
    defaultValue = 16
  elif inputType == 'paddingX':
    defaultValue = 0
  elif inputType == 'paddingY':
    defaultValue = 0
  elif inputType == 'tilestOffsetX':
    defaultValue = 0
  elif inputType == 'tilestOffsetY':
    defaultValue = 0

  try:
    value = int(inputValue)
    if value < 1:
      value = defaultValue
  except:
    value = defaultValue

  atlasDetails[inputType]['set'] = True
  atlasDetails[inputType]['value'] = value

  inputElement = system.textInputs[f'{inputType}Input']
  inputElement.inputText = str(value)
  inputElement.setTextBoxValue()

def closingSeq():
  window.closeWindow()

def importAtlas(atlasURL: str) -> Optional[pgx.TextureAtlas]:
  print('what')
  if not (os.path.exists(atlasURL) and os.path.isfile(atlasURL)):
    print('File does not exist')
    return None

  global atlasDetails, window, system, atlasImage, textureSection, controlPanel, doneButton, atlas, eventLoop, drawLoop, inputOnChange, closingSeq

  window = pgx.Window('Atlas Importer', (1024, 576), customEventHandler=eventLoop, customDrawProcess=drawLoop)

  system = pgx.System()

  atlasImage = pg.image.load(atlasURL)

  textureSection = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=8),
      'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
      'height': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=92)
    }, atlasImage, backgroundSizeType='fit'
  )

  textureSection.backgroundSmoothScale = False

  controlPanel = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
      'height': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=8)
    }, pg.Color(20, 20, 20), 0
  )

  doneButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=90),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=16),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=68)
      }, pg.Color(50, 50, 50), 4
    ),
    pg.Color(137, 82, 182),
    text='Done',
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    onClick=closingSeq,
    onClickActuation='buttonUp'
  )

  tileWidthInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=2),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='Tile Width',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'tileWidth',
      'sendValue': True
    }
  )

  tileHeightInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=12),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='Tile Height',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'tileHeight',
      'sendValue': True
    }
  )

  paddingXInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=22),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='paddingX',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'paddingX',
      'sendValue': True
    }
  )

  paddingYInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=32),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='Padding Y',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'paddingY',
      'sendValue': True
    }
  )

  tilestOffsetXInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=42),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='Offset X',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'tilestOffsetX',
      'sendValue': True
    }
  )

  tilestOffsetYInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=52),
        'y': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=25),
        'width': pgx.DynamicValue('classPer', controlPanel, classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', controlPanel, classAttribute='height', percent=50)
      }, pg.Color(50, 50, 50), 4
    ),
    fontPath='Helvetica',
    textColor=pg.Color(250, 250, 250),
    placeholder='Offset Y',
    placeholderTextColor=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': inputOnChange,
      'params': 'tilestOffsetY',
      'sendValue': True
    }
  )

  system.addElement(textureSection, 'textureSection')
  system.addElement(controlPanel, 'controlPanel')
  system.addElement(doneButton, 'doneButton')
  system.addElement(tileWidthInput, 'tileWidthInput')
  system.addElement(tileHeightInput, 'tileHeightInput')
  system.addElement(paddingXInput, 'paddingXInput')
  system.addElement(paddingYInput, 'paddingYInput')
  system.addElement(tilestOffsetXInput, 'tilestOffsetXInput')
  system.addElement(tilestOffsetYInput, 'tilestOffsetYInput')

  window.addSystem(system, 'system')

  window.setSystemZ('system', 1)

  window.activateSystems('system')

  window.openWindow()

  atlas = pgx.TextureAtlas(
    atlasURL,
    atlasDetails['tileWidth']['value'],
    atlasDetails['tileHeight']['value'],
    atlasDetails['paddingX']['value'],
    atlasDetails['paddingY']['value'],
    atlasDetails['tilestOffsetX']['value'],
    atlasDetails['tilestOffsetY']['value']
  )

  return atlas
