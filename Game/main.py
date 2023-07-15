import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#load images
#map
map_image = pg.image.load('Game/levels/level.png').convert_alpha()
#individual turret for mouse cursor
cursor_turret = pg.image.load('Game/assets/images/turrets/cursor_turret.png').convert_alpha()
#enemies
enemy_image = pg.image.load('Game/assets/images/enemies/enemy_1.png').convert_alpha()
#buttons
buy_turret_image = pg.image.load('Game/assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('Game/assets/images/buttons/cancel.png').convert_alpha()

#load json data for level
with open('Game/levels/level.tmj') as file:
  world_data = json.load(file)

def create_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] == 7:
    #check that there isnt already a turret there
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
    #if it is a free space then create turret
    if space_is_free == True:
      new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
      turret_group.add(new_turret)

#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  ########################
  # UPDATING SECTION
  ########################

  #update groups
  enemy_group.update()

  ########################
  # DRAWING SECTION
  ########################

  screen.fill("grey100")

  #draw level
  world.draw(screen)

  #draw groups
  enemy_group.draw(screen)
  turret_group.draw(screen)

  #draw buttons
  #button for placing turrets
  if turret_button.draw(screen):
    print("new turret")

  if cancel_button.draw(screen):
    print("cancel")

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      #check if mouse is on the game area
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        create_turret(mouse_pos)


  #update display
  pg.display.flip()

pg.quit()