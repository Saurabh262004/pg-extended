from demo import colors
import pg_extended as pgx

def addOverlaySystem(window: pgx.Window):
  overlaySystem = pgx.System(preLoadState=True)

  menuAnim = pgx.AnimatedValue(
    [
      pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=-80),
      pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=5)
    ], 400, 'start', 'easeInOut'
  )

  def triggerMenuAnimation():
    if menuAnim.hasPlayedOnce:
      menuAnim.trigger(not menuAnim.reverse)
    else:
      menuAnim.trigger()

  menuSection = pgx.Section(
    {
      'x': pgx.DynamicValue('classNum', menuAnim, classAttribute='value'),
      'y': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=10),
      'width': pgx.DynamicValue('classPer', window, classAttribute='screenWidth', percent=80),
      'height': pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=80)
    }, colors.section, 4
  )

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

  toggleText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 20, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 30, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=10),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=5)
      }, colors.secondary
    ), 'Toggle:', 'Helvetica', colors.text
  )

  toggle = pgx.Toggle(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 6, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 21.5, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=6),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=3)
      }, colors.back1, 4
    ), colors.text, colors.primary, colors.primary
  )

  sliderText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 20, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 10, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=10),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=5)
      }, colors.secondary
    ), 'Slider:', 'Helvetica', colors.text
  )

  slider = pgx.Slider(
    'horizontal',
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 6, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 8.45, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=30),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=2)
      }, colors.back1, 2
    ),
    pgx.Section(
      {
        'x': pgx.DynamicValue('number', 0),
        'y': pgx.DynamicValue('number', 0),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=3),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=2)
      }, colors.primary, 2
    ), (0, 100), 5, colors.text
  )

  textInputText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 20, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 5.8, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=10),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=5)
      }, colors.secondary
    ), 'Text Input:', 'Helvetica', colors.text
  )

  textInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('callable', lambda menuSection: menuSection.x + menuSection.width / 6, menuSection),
        'y': pgx.DynamicValue('callable', lambda menuSection: menuSection.y + menuSection.width / 5.6, menuSection),
        'width': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=30),
        'height': pgx.DynamicValue('classPer', menuSection, classAttribute='width', percent=4)
      }, colors.primary, 2
    ), 'Helvetica', colors.text, 12, 'Type here...', colors.back1
  )

  window.customAnimatedValues.append(menuAnim)

  menuSection.lazyUpdate = False
  toggleText.lazyUpdate = False
  toggle.lazyUpdate = False
  sliderText.lazyUpdate = False
  slider.lazyUpdate = False
  textInputText.lazyUpdate = False
  textInput.lazyUpdate = False

  overlaySystem.addElement(menuSection, 'menuSection')
  overlaySystem.addElement(menuButton, 'menuButton')
  overlaySystem.addElement(toggleText, 'toggleText')
  overlaySystem.addElement(toggle, 'toggle')
  overlaySystem.addElement(sliderText, 'sliderText')
  overlaySystem.addElement(slider, 'slider')
  overlaySystem.addElement(textInputText, 'textInputText')
  overlaySystem.addElement(textInput, 'textInput')

  window.addSystem(overlaySystem, 'overlay')
