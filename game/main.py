import pygame
from player import Player
from world import World
from sensors import create_sensors, draw_lines, sprite_group_sensors
from helpers import collide_player, collide_sensors
from settings import LENGTH_SENSOR


pygame.init()
screen = pygame.display.set_mode((1120, 992))
clock = pygame.time.Clock()

# world section
WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
sprite_group_floor = WORLD.sprite_group_floor
list_group_floor = [sprite for sprite in sprite_group_floor]

# player section
PLAYER = Player()

# sensors section
create_sensors(PLAYER.rect.centerx, PLAYER.rect.centery, length_sensor=LENGTH_SENSOR)
sprite_group_sens = sprite_group_sensors
global_list_sensors_colliding = []



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw sprites
    sprite_group_floor.draw(screen)
    sprite_group.draw(screen)

    # draw and move player
    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()

    # draw lines player
    for sprite in sprite_group_sens:
        if sprite.name in ("right", "down"):
            sprite.rect.x = PLAYER.rect.centerx
            sprite.rect.y = PLAYER.rect.centery
        elif sprite.name == "left":
            sprite.rect.x = PLAYER.rect.centerx-LENGTH_SENSOR
            sprite.rect.y = PLAYER.rect.centery
        elif sprite.name == "up":
            sprite.rect.x = PLAYER.rect.centerx
            sprite.rect.y = PLAYER.rect.centery-LENGTH_SENSOR

        if sprite.name in global_list_sensors_colliding:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height, color="red")
        else:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)

    # check collisions
    collide_player(PLAYER, list_group_floor)

    list_sensors_colliding = collide_sensors(sprite_group_sens, sprite_group_floor)
    global_list_sensors_colliding = list_sensors_colliding

    pygame.display.flip()
    clock.tick(60)
