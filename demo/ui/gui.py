from demo import colors
import pg_extended as pgx

def addOverlaySystem(window: pgx.Window):
	overlaySystem = pgx.System(preLoadState=True)

	menuAnim = pgx.AnimatedValue(
		[
			pgx.DynamicValue(window, 'screenWidth', percent=-80),
			pgx.DynamicValue(window, 'screenWidth', percent=5)
		], 400, 'start', 'easeInOut'
	)

	def triggerMenuAnimation():
		if menuAnim.hasPlayedOnce:
			menuAnim.trigger(not menuAnim.reverse)
		else:
			menuAnim.trigger()

	menuSection = pgx.Section(
		{
			'x': pgx.DynamicValue(menuAnim, 'value'),
			'y': pgx.DynamicValue(window, 'screenHeight', percent=10),
			'width': pgx.DynamicValue(window, 'screenWidth', percent=80),
			'height': pgx.DynamicValue(window, 'screenHeight', percent=80)
		}, colors.section, 4
	)

	menuButton = pgx.Button(
		pgx.TextBox(
			pgx.Section(
				{
					'x': pgx.DynamicValue(window, 'screenWidth', percent=92.5),
					'y': pgx.DynamicValue(window, 'screenWidth', percent=1.5),
					'width': pgx.DynamicValue(window, 'screenWidth', percent=6),
					'height': pgx.DynamicValue(window, 'screenWidth', percent=3)
				}, colors.primary, 4
			), 'Menu', 'Helvetica', colors.text
		), pgx.CallbackSet((
			pgx.Callback(
				('mouseDown',),
				triggerMenuAnimation
			),
		))
	)

	toggleText = pgx.TextBox(
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 20),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 30),
				'width': pgx.DynamicValue(menuSection, 'width', percent=10),
				'height': pgx.DynamicValue(menuSection, 'width', percent=5)
			}, colors.secondary
		), 'Toggle:', 'Helvetica', colors.text
	)

	toggleText.alignTextHorizontal = 'left'

	toggle = pgx.Toggle(
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 5),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 21.5),
				'width': pgx.DynamicValue(menuSection, 'width', percent=6),
				'height': pgx.DynamicValue(menuSection, 'width', percent=3)
			}, colors.back1, 4
		), colors.text, colors.primary, colors.primary,
		callback=pgx.Callback(
			('None',),
			lambda v: print(f'got {v}'),
			extraArgKeys={'value': 'v'}
		)
	)

	sliderText = pgx.TextBox(
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 20),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 10),
				'width': pgx.DynamicValue(menuSection,'width', percent=10),
				'height': pgx.DynamicValue(menuSection,'width', percent=5)
			}, colors.secondary
		), 'Slider:', 'Helvetica', colors.text
	)

	sliderText.alignTextHorizontal = 'left'

	def printSliderVal(v, et):
		print(f'got {v} via {et}')

	slider = pgx.Slider(
		'horizontal',
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 5),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 8.45),
				'width': pgx.DynamicValue(menuSection, 'width', percent=30),
				'height': pgx.DynamicValue(menuSection, 'width', percent=2)
			}, colors.back1, 2
		),
		pgx.Circle(
			{
				'x': pgx.DynamicValue(0),
				'y': pgx.DynamicValue(0),
				'radius': pgx.DynamicValue(menuSection, 'width', percent=1.5)
			}, colors.primary
		), (0, 100), 5, colors.text,
		pgx.CallbackSet((
			pgx.Callback(
				('mouseUp', 'mouseDown'),
				printSliderVal,
				{'et': 'click'},
				{'value': 'v'}
			),
			pgx.Callback(
				('mouseDrag',),
				printSliderVal,
				{'et': 'drag'},
				{'value': 'v'}
			),
			pgx.Callback(
				('scroll',),
				printSliderVal,
				{'et': 'scroll'},
				{'value': 'v'}
			)
		))
	)

	textInputText = pgx.TextBox(
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 20),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 5.8),
				'width': pgx.DynamicValue(menuSection, 'width', percent=10),
				'height': pgx.DynamicValue(menuSection, 'width', percent=5)
			}, colors.secondary
		), 'Text Input:', 'Helvetica', colors.text
	)

	textInputText.alignTextHorizontal = 'left'

	textInput = pgx.TextInput(
		pgx.Section(
			{
				'x': pgx.DynamicValue(lambda: menuSection.x + menuSection.width / 5),
				'y': pgx.DynamicValue(lambda: menuSection.y + menuSection.width / 5.6),
				'width': pgx.DynamicValue(menuSection, 'width', percent=30),
				'height': pgx.DynamicValue(menuSection, 'width', percent=4)
			}, colors.primary, 2
		), 'Helvetica', colors.text,
		callback=pgx.Callback(
			('None',),
			lambda v: print(f'got text: {v}'),
			extraArgKeys={'value': 'v'}
		)
	)

	textInput.border = 0
	textInput.placeholder = 'Type here...'
	textInput.placeholderTextColor = colors.back1

	textInput.setTextBoxValue()

	window.customAnimatedValues['menuAnim'] = menuAnim

	menuSection.lazyUpdate = False
	toggleText.lazyUpdate = False
	toggle.lazyUpdate = False
	sliderText.lazyUpdate = False
	slider.lazyUpdate = False
	textInputText.lazyUpdate = False
	textInput.lazyUpdate = False

	textInput.textBox.alignTextHorizontal = 'center'

	overlaySystem.addElement(menuSection, 'menuSection')
	overlaySystem.addElement(menuButton, 'menuButton')
	overlaySystem.addElement(toggleText, 'toggleText')
	overlaySystem.addElement(toggle, 'toggle')
	overlaySystem.addElement(sliderText, 'sliderText')
	overlaySystem.addElement(slider, 'slider')
	overlaySystem.addElement(textInputText, 'textInputText')
	overlaySystem.addElement(textInput, 'textInput')

	window.addSystem(overlaySystem, 'overlay')
