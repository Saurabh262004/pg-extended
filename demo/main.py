import pg_extended as pgx
from .gui import addOverlaySystem

app = pgx.Window('demo', (800, 600))

addOverlaySystem(app)

app.setSystemZ('overlay', 0)

app.activateSystems('overlay')

app.openWindow()
