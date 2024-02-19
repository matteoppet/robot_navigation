# file to debug things regarding hte pygame stuff

import pygame
from player import Player
from helpers import create_table_tiles
from csv_world import sprite_boundaries, sprite_path
import os

pygame.init()
screen = pygame.display.set_mode((1120, 1024))
clock = pygame.time.Clock()
running = True


PLAYER = Player()


SPRITE_GROUP_BOUNDARIES = sprite_boundaries
LIST_GROUP_BOUNDARIES = [sprite for sprite in SPRITE_GROUP_BOUNDARIES]

TABLE_TILES = create_table_tiles(SPRITE_GROUP_BOUNDARIES)

SPRITE_GROUP_PATH = sprite_path
LIST_GROUP_PATH = [sprite for sprite in SPRITE_GROUP_PATH]


def draw_boundaries():
    for sprite in LIST_GROUP_BOUNDARIES:
        pygame.draw.rect(screen, "red", (sprite.rect.x, sprite.rect.y, 32, 32))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    map_path = os.path.join(os.path.dirname(__file__), "../../map_files/png/map.png")
    map_image = pygame.image.load(map_path)
    screen.blit(map_image, (0,0))

    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()

    draw_boundaries()

    for sprite in LIST_GROUP_BOUNDARIES:
        collisions = pygame.sprite.collide_rect(PLAYER, sprite)
        if collisions:
            print("collided")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()