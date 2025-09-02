import pygame as pg
from demo import colors
import pg_extended as pgx
from demo import sharedResources

def loopProcess():
  app: pgx.Window = sharedResources.data['app']

  app.screen.fill(colors.back1)
