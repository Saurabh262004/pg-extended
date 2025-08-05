import pygame as pg
from PG_UI_Manager.UIElements.Core import DynamicValue as DV
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
    background=pg.Color(200, 200, 200)),
  elementID='mainSection'
)

# Button
system.addElement(
  element=Button(
    section=Section(
      dimensions={
        'x': DV('classPer', app, classAttr='screenWidth', percent=5),
        'y': DV('classPer', app, classAttr='screenWidth', percent=5),
        'width': DV('classPer', app, classAttr='screenWidth', percent=10),
        'height': DV('classPer', app, classAttr='screenWidth', percent=5)
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
    onClick=lambda: print('Button clicked!'),
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
        'x': DV('classPer', app, classAttr='screenWidth', percent=5),
        'y': DV('classPer', app, classAttr='screenWidth', percent=17),
        'width': DV('classPer', app, classAttr='screenWidth', percent=10),
        'height': DV('classPer', app, classAttr='screenWidth', percent=5)
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
        'x': DV('classPer', app, classAttr='screenWidth', percent=5),
        'y': DV('classPer', app, classAttr='screenWidth', percent=28),
        'width': DV('classPer', app, classAttr='screenWidth', percent=25),
        'height': DV('classPer', app, classAttr='screenWidth', percent=2)
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
        'radius': DV('classPer', app, classAttr='screenWidth', percent=2)
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
        'x': DV('classPer', app, classAttr='screenWidth', percent=5),
        'y': DV('classPer', app, classAttr='screenWidth', percent=35),
        'width': DV('classPer', app, classAttr='screenWidth', percent=25),
        'height': DV('classPer', app, classAttr='screenWidth', percent=5)
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
    centerText=True
  ),
  elementID='myTextBox'
)

app.addSystem(system, 'mainSystem')

app.setSystemZ('mainSystem', 0)

app.activateSystems('mainSystem')

app.openWindow()
