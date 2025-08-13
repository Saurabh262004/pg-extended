import pygame as pg
from PG_UI_Manager.UIElements.Core import DynamicValue as DV, AnimatedValue
from PG_UI_Manager.UIElements import *
from PG_UI_Manager import System, Window

app = Window('Main Window', (480, 270))

system = System(preLoadState=True)

# the mandatory main section
system.addElement(
  element=Section(
    dimensions={
      'x': DV('number', 0),
      'y': DV('number', 0),
      'width': DV('number', 1),
      'height': DV('number', 1)
    },
    background=pg.Color(0, 0, 10)),
  elementID='mainSection'
)

# animators
topToBottom = AnimatedValue(
  values=(
    DV('classPer', app, classAttribute='screenHeight', percent=1),
    DV('classPer', app, classAttribute='screenHeight', percent=89)
  ),
  duration=400,
  defaultPos='end',
  interpolation='linear'
)

leftToRight = AnimatedValue(
  values=(
    DV('classPer', app, classAttribute='screenWidth', percent=1),
    DV('classPer', app, classAttribute='screenWidth', percent=89)
  ),
  duration=300,
  defaultPos='end',
  interpolation='easeIn'
)

swTolw = AnimatedValue(
  values=(
    DV('classPer', app, classAttribute='screenWidth', percent=98),
    DV('classPer', app, classAttribute='screenWidth', percent=10)
  ),
  duration=200,
  defaultPos='end',
  interpolation='easeOut'
)

shTolh = AnimatedValue(
  values=(
    DV('classPer', app, classAttribute='screenHeight', percent=98),
    DV('classPer', app, classAttribute='screenHeight', percent=10)
  ),
  duration=100,
  defaultPos='end',
  interpolation='easeInOut'
)

app.customAnimatedValues.extend((topToBottom, leftToRight, swTolw, shTolh))

# animated section
system.addElement(
  element=Section(
    dimensions={
     'x': DV('classNum', leftToRight, classAttribute='value'),
     'y': DV('classNum', topToBottom, classAttribute='value'),
     'width': DV('classNum', swTolw, classAttribute='value'),
     'height': DV('classNum', shTolh, classAttribute='value')
    },
    background=pg.Color(0, 200, 200)
  ),
  elementID='animSection'
)

system.elements['animSection'].lazyUpdate = False

def triggerAnimations():
  rev = not topToBottom.reverse

  topToBottom.trigger(rev)
  leftToRight.trigger(rev)
  swTolw.trigger(rev)
  shTolh.trigger(rev)

# Button
system.addElement(
  element=Button(
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'y': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'width': DV('classPer', app, classAttribute='screenWidth', percent=10),
        'height': DV('classPer', app, classAttribute='screenWidth', percent=5)
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
  element=Toggle(
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'y': DV('classPer', app, classAttribute='screenWidth', percent=17),
        'width': DV('classPer', app, classAttribute='screenWidth', percent=10),
        'height': DV('classPer', app, classAttribute='screenWidth', percent=5)
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
  element=Slider(
    orientation='horizontal',
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'y': DV('classPer', app, classAttribute='screenWidth', percent=28),
        'width': DV('classPer', app, classAttribute='screenWidth', percent=25),
        'height': DV('classPer', app, classAttribute='screenWidth', percent=2)
      },
      background=pg.Color(80, 80, 80),
      borderRadius=6,
      backgroundSizeType='fit',
      backgroundSizePercent=100
    ),
    dragElement=Circle(
      dimensions={
        'x': DV('number', 0),
        'y': DV('number', 0),
        'radius': DV('classPer', app, classAttribute='screenWidth', percent=2)
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
  element=TextBox(
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'y': DV('classPer', app, classAttribute='screenWidth', percent=35),
        'width': DV('classPer', app, classAttribute='screenWidth', percent=25),
        'height': DV('classPer', app, classAttribute='screenWidth', percent=5)
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
  TextInput(
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttribute='screenWidth', percent=5),
        'y': DV('classPer', app, classAttribute='screenWidth', percent=42),
        'width': DV('classPer', app, classAttribute='screenWidth', percent=25),
        'height': DV('classPer', app, classAttribute='screenWidth', percent=5)
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
    resizable=True,
    alignTextHorizontal='center',
    alignTextVertical='center',
    onChangeInfo={
      'callable': lambda value: print(f'Text Box value changed to: {value}'),
      'params': None,
      'sendValue': True
    }
  ), 'myTextInput'
)

app.addSystem(system, 'mainSystem')

app.setSystemZ('mainSystem', 0)

app.activateSystems('mainSystem')

app.openWindow()
