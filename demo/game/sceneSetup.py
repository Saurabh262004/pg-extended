import pg_extended as pgx

def addScene(window: pgx.Window):
  scene1 = pgx.Scene()

  atlas1 = pgx.TextureAtlas('demo/game/assets/1.png', 16, 16, namesJsonURL='demo/game/assets/1.names.json')

  atlas2 = pgx.TextureAtlas('demo/game/assets/2.png', 44, 48)

  level1 = pgx.Level(5, 5, 16, 16, 'demo/game/level1.json')

  scene1.addElement(atlas1, 'atlas1')

  scene1.addElement(atlas2, 'atlas2')

  scene1.addElement(level1, 'level1')

  window.addScene(scene1, 'scene1')
