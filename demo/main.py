import pg_extended as pgx
from demo import sharedResources
from demo.loopProcess import loopProcess
from demo.ui.gui import addOverlaySystem
from demo.game.sceneSetup import addScene

# start a window with "demo" title, 854x480 resolution and custom loop process
app = pgx.Window('demo', (854, 480), customLoopProcess=loopProcess)

# stored window in sharedResources for easy access in other modules
sharedResources.data['app'] = app

# add overlay system in window
addOverlaySystem(app)

# add a game scene to window
addScene(app)

# setup viewport
viewport = pgx.ViewPort(pgx.DynamicValue(0), pgx.DynamicValue(0), 1)
app.setViewPort(viewport)

# systems must have a z-index to be used
app.setSystemZ('overlay', 0)

# multiple systems can be activated
app.activateSystems('overlay')

# activate level1
app.scenes['scene1'].activateLevel('level1')

# activate scene1
app.setActiveScene('scene1')

# start the game loop
app.openWindow()
