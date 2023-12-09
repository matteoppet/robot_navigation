import pygame
from player import Player
from world import World
from boundaries import create_boundaries, sprite_group_boundaries
from helpers import collide_player, draw_lines


pygame.init()
screen = pygame.display.set_mode((1120, 992))
clock = pygame.time.Clock()

WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
PLAYER = Player()

create_boundaries()
sprite_group_bound = sprite_group_boundaries

list_boundaries = []
# Draw polygon sprite boundaries
for sprite in sprite_group_boundaries:
    list_boundaries.append(sprite)


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
    draw_lines(screen, PLAYER)

    # check collision
    collide_player(PLAYER, list_boundaries)

    pygame.display.flip()
    # pygame.display.update()
    clock.tick(60)


# CHANGE COLOR OF THE LINES BASED ON THE DISTANCE FROM THE BOUNDARIES
# IDEAS:
# create a collide function for the lines and check if it collides