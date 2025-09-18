import pg_extended as pgx
from tools.Level_Editor import sharedAssets
from tools.Level_Editor.ui import console, grid

app = sharedAssets.app = pgx.Window('Level Editor', (1280, 720), (746, 420))

grid.add(app)

console.add(app)

app.activateSystems(('grid', 'console'))

app.openWindow()
