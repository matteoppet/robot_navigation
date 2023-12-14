import pygame
from player import Player
from world import World
from sensors import create_sensors, draw_lines, sprite_group_sensors
from boundaries import create_boundaries, sprite_group_boundaries
from helpers import collide_player, collide_sensors


pygame.init()
screen = pygame.display.set_mode((1120, 992))
clock = pygame.time.Clock()

# world section
WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects

# player section
PLAYER = Player()

# boundaries section
create_boundaries()
sprite_group_bound = sprite_group_boundaries
list_boundaries = [sprite for sprite in sprite_group_boundaries]


# sensors section
create_sensors(PLAYER.rect.centerx, PLAYER.rect.centery)
sprite_group_sens = sprite_group_sensors


global_list_sensors_colliding = []


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw sprites
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
            sprite.rect.x = PLAYER.rect.centerx-100
            sprite.rect.y = PLAYER.rect.centery
        elif sprite.name == "up":
            sprite.rect.x = PLAYER.rect.centerx
            sprite.rect.y = PLAYER.rect.centery-100

        if sprite.name in global_list_sensors_colliding:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height, color="red")
        else:
            draw_lines(screen, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)

    # check collisions
    collide_player(PLAYER, list_boundaries)

    list_sensors_colliding = collide_sensors(sprite_group_sens, sprite_group_bound)
    global_list_sensors_colliding = list_sensors_colliding
    

    pygame.display.flip()
    clock.tick(60)
