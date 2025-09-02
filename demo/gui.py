import pygame as pg
from demo import colors
import pg_extended as pgx

def addOverlaySystem(window: pgx.Window):
  menuSection = None

  # create a system with pre-loaded state
  overlaySystem = pgx.System(preLoadState=True)

  # an AnimatedValue can have multiple values to interpolates through, these values must be DynamicValues
  # a callback can also be set to run at the end of the animation
  menuAnimX = pgx.AnimatedValue(
    [
      pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=-80),
      pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=5)
    ], 400, 'start', 'easeInOut'
  )

  def triggerMenuAnimation():
    if menuAnimX.hasPlayedOnce:
      menuAnimX.trigger(not menuAnimX.reverse)
    else:
      menuAnimX.trigger()

  # if you want the animated values to update automatically append them into customAnimatedValues list
  window.customAnimatedValues.append(menuAnimX)

  menuSection = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', menuAnimX, classAttribute='value'),
      'y': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=10),
      'width': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=80),
      'height': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=80)
    }, colors.section, 4
  )

  menuSection.lazyUpdate = False

  overlaySystem.addElement(menuSection, 'menuSection')

  # a button that triggers the AnimatedValue for the x position of the section
  menuButton = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=92.5),
        'y': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=1.5),
        'width': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=6),
        'height': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=3)
      }, colors.primary, 4
    ), colors.secondary,
    text='Menu',
    fontPath='Helvetica',
    textColor=colors.text,
    onClick=triggerMenuAnimation
  )

  overlaySystem.addElement(menuButton, 'menuButton')

  toggleText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 20, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 30, menuSection),
        'width': pgx.DynamicValue('classPer', overlaySystem.sections['menuSection'], classAttribute='width', percent=10),
        'height': pgx.DynamicValue('classPer', overlaySystem.sections['menuSection'], classAttribute='width', percent=5)
      }, colors.secondary
    ), 'Toggle:', 'Helvetica', colors.text
  )

  toggleText.lazyUpdate = False

  overlaySystem.addElement(toggleText, 'toggleText')

  toggle = pgx.Toggle(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 6, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 25, menuSection),
        'width': pgx.DynamicValue('classPer', overlaySystem.sections['menuSection'], classAttribute='width', percent=8),
        'height': pgx.DynamicValue('classPer', overlaySystem.sections['menuSection'], classAttribute='width', percent=4)
      }, colors.back1, 4
    ), colors.text, colors.primary, colors.primary
  )

  toggle.lazyUpdate = False

  overlaySystem.addElement(toggle, 'toggle')

  window.addSystem(overlaySystem, 'overlay')
