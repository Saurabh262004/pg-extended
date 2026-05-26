import pg_extended as pgx
from demo import sharedResources
from demo.loopProcess import loopProcess
from demo.ui.gui import addOverlaySystem

# start a window with "demo" title, 854x480 resolution and custom loop process
app = pgx.Window('demo', (854, 480), customLoopProcess=loopProcess)

# stored window in sharedResources for easy access in other modules
sharedResources.data['app'] = app

# add overlay system in window
addOverlaySystem(app)

# systems must have a z-index to be used
app.setSystemZ('overlay', 0)

# multiple systems can be activated
app.activateSystems('overlay')

# start the game loop
app.openWindow()
