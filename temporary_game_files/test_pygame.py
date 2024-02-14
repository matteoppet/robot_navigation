import pygame
from temporary_game_files.world import sprite_ground, sprite_boundaries
from settings import WINDOW_X, WINDOW_Y, TILE_WIDTH, TILE_HEIGHT

pygame.init()
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
clock = pygame.time.Clock()
running = True

sprite_ground = sprite_ground
sprite_boundaries = sprite_boundaries

import os

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    for sprite_1 in sprite_ground:
        rect = pygame.Rect(sprite_1.rect.x, sprite_1.rect.y, TILE_WIDTH, TILE_HEIGHT)
        pygame.draw.rect(screen, "white", rect)

    for sprite_2 in sprite_boundaries:
        rect = pygame.Rect(sprite_2.rect.x, sprite_2.rect.y, TILE_WIDTH, TILE_HEIGHT)
        pygame.draw.rect(screen, "grey", rect)

    rect_player = pygame.Rect(32, 32, 10, 10)
    pygame.draw.rect(screen, "black", rect_player)

    map_path = os.path.join(os.path.dirname(__file__), "../temporary_map_files/tileset_tinyrooms/png/map.png")
    map_image = pygame.image.load(map_path)
    screen.blit(map_image, (0,0))

    player_path = os.path.join(os.path.dirname(__file__), "../temporary_map_files/tileset_tinyrooms/player/player.png")
    player_image = pygame.image.load(player_path)
    screen.blit(player_image, (32, 32))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()