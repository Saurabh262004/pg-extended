import pygame as pg
import pg_extended as pgx

app = pgx.Window('Main Window', (480, 270))

system = pgx.System(preLoadState=True)

# animators
topToBottom = pgx.AnimatedValue(
  values=(
    pgx.DynamicValue('classPer', app, classAttribute='screenHeight', percent=1),
    pgx.DynamicValue('classPer', app, classAttribute='screenHeight', percent=89)
  ),
  duration=300,
  defaultPos='end',
  interpolation='linear'
)

leftToRight = pgx.AnimatedValue(
  values=(
    pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=1),
    pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=89)
  ),
  duration=300,
  defaultPos='end',
  interpolation='easeIn'
)

swTolw = pgx.AnimatedValue(
  values=(
    pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=98),
    pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=10)
  ),
  duration=300,
  defaultPos='end',
  interpolation='easeOut'
)

shTolh = pgx.AnimatedValue(
  values=(
    pgx.DynamicValue('classPer', app, classAttribute='screenHeight', percent=98),
    pgx.DynamicValue('classPer', app, classAttribute='screenHeight', percent=10)
  ),
  duration=300,
  defaultPos='end',
  interpolation='easeInOut'
)

app.customAnimatedValues.extend((topToBottom, leftToRight, swTolw, shTolh))

# animated section
system.addElement(
  element=pgx.Section(
    dimensions={
     'x': pgx.DynamicValue('classNum', leftToRight, classAttribute='value'),
     'y': pgx.DynamicValue('classNum', topToBottom, classAttribute='value'),
     'width': pgx.DynamicValue('classNum', swTolw, classAttribute='value'),
     'height': pgx.DynamicValue('classNum', shTolh, classAttribute='value')
    },
    background=pg.Color(0, 200, 200)
  ),
  elementID='animSection'
)

system.elements['animSection'].lazyUpdate = False

def triggerAnimations():
  rev = not topToBottom.reverse

  topToBottom.trigger(rev, 1, True)
  leftToRight.trigger(rev, 1, True)
  swTolw.trigger(rev, 1, True)
  shTolh.trigger(rev, 1, True)

# Button
system.addElement(
  element=pgx.Button(
    section=pgx.Section(
      dimensions={
        'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=10),
        'height': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5)
      },
      background=pg.Color(100, 100, 100),
      borderRadius=5,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    pressedBackground=pg.Color(150, 150, 150),
    borderColor=pg.Color(0, 0, 0),
    borderColorPressed=pg.Color(255, 0, 0),
    text='Click Me',
    fontPath='Helvetica',
    textColor=pg.Color(255, 255, 255),
    onClick=triggerAnimations,
    border=1,
    onClickActuation='buttonDown'
  ),
  elementID='myButton'
)

# Toggle
system.addElement(
  element=pgx.Toggle(
    section=pgx.Section(
      dimensions={
        'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=17),
        'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=10),
        'height': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5)
      },
      background=pg.Color(100, 100, 100),
      borderRadius=6,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    indicatorColor=pg.Color(220, 220, 220),
    borderColor=pg.Color(0, 0, 0),
    borderColorToggled=pg.Color(200, 100, 0),
    onClick=lambda toggled: print(f'Toggle state: {toggled}'),
    sendStateInfoOnClick=True,
    border=1
  ),
  elementID='myToggle'
)

# Slider
system.addElement(
  element=pgx.Slider(
    orientation='horizontal',
    section=pgx.Section(
      dimensions={
        'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=28),
        'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=25),
        'height': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=2)
      },
      background=pg.Color(80, 80, 80),
      borderRadius=6,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    dragElement=pgx.Circle(
      dimensions={
        'x': pgx.DynamicValue('number', 0),
        'y': pgx.DynamicValue('number', 0),
        'radius': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=2)
      },
      background=pg.Color(220, 110, 220),
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    valueRange=(0, 100),
    scrollSpeed=5,
    filledSliderBackground=pg.Color(150, 150, 150),
    onChangeInfo={
      'callable': lambda value: print(f'Slider value changed to: {value}'),
      'params': None,
      'sendValue': True
    },
    hoverToScroll=False
  ),
  elementID='mySlider'
)

# TextBox
system.addElement(
  element=pgx.TextBox(
    section=pgx.Section(
      dimensions={
        'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=35),
        'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=25),
        'height': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5)
      },
      background=pg.Color(100, 100, 100),
      borderRadius=6,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    text='Hello World!',
    fontPath='Helvetica',
    textColor=pg.Color(255, 255, 255),
    drawSectionDefault=True,
    alignTextHorizontal='center',
    alignTextVertical='center'
  ),
  elementID='myTextBox'
)

# TextInput
system.addElement(
  element=pgx.TextInput(
    section=pgx.Section(
      dimensions={
        'x': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=42),
        'width': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=25),
        'height': pgx.DynamicValue('classPer', app, classAttribute='screenWidth', percent=5)
      },
      background=pg.Color(100, 100, 100),
      borderRadius=0,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    fontPath='Helvetica',
    textColor=pg.Color(255, 255, 255),
    placeholder='placeholder',
    placeholderTextColor=pg.Color(200, 200, 200),
    border=1,
    borderColor=pg.Color(0, 0, 0),
    focusBorderColor=pg.Color(255, 0, 0),
    focusBackground=pg.Color(80, 80, 80),
    alignTextHorizontal='center',
    alignTextVertical='center',
    onChangeInfo={
      'callable': lambda value: print(f'Text Box value changed to: {value}'),
      'params': None,
      'sendValue': True
    }
  ),
  elementID='myTextInput'
)

scene = pgx.Scene()

scene.addElement(
  element=pgx.TextureAtlas(
    tilesetURL='tests/assets/decorative_cracks_walls.png',
    tileWidth=16,
    tileHeight=16,
    namesJsonURL='tests/names.json'
  ),
  elementID='atlas1'
)

scene.addElement(
  element=pgx.TextureAtlas(
    tilesetURL='tests/assets/fire_animation.png',
    tileWidth=44,
    tileHeight=48
  ),
  elementID='atlas2'
)

scene.addElement(
  element=pgx.Level(
    numTilesX=5,
    numTilesY=5,
    tileWidth=64,
    tileHeight=64,
    tilesMatrixJsonURL='tests/level1.json'
  ),
  elementID='level1'
)

scene.activateLevel('level1')

def cc():
  try:
    return -pg.mouse.get_pos()[0] / 100
  except:
    return 0

viewPort = pgx.ViewPort(
  pgx.DynamicValue('callable', cc),
  pgx.DynamicValue('callable', cc),
  1
)

app.addSystem(system, 'mainSystem')

app.addScene(scene, 'mainScene')

app.setViewPort(viewPort)

app.setSystemZ('mainSystem', 0)

app.activateSystems('mainSystem')

app.setActiveScene('mainScene')

app.openWindow()
