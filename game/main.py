import pygame
from helpers.player import Player
from helpers.world import World
from helpers.helpers import collide_player, collide_sensors, reset_game, mouse_function, create_distance_sprites, create_table_tiles, calculate_distance_boundaries
from helpers.settings import LENGTH_SENSOR


pygame.init()
SCREEN = pygame.display.set_mode((1120, 992))
CLOCK = pygame.time.Clock()

# world section
WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
sprite_group_boundaries_floor = WORLD.sprite_group_boundaries_floor
list_group_boundarties_floor = [sprite for sprite in sprite_group_boundaries_floor]
TABLE_TILES = create_table_tiles(sprite_group_boundaries_floor)

# player section
PLAYER = Player()


# DISTANCE
create_distance_sprites()
sprite_group_for_distance = create_distance_sprites()


running = True
while running:
    
    # draw sprites
    sprite_group_boundaries_floor.draw(SCREEN)
    sprite_group.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_function(event, list_group_boundarties_floor, SCREEN)

    # draw and move player
    SCREEN.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()

    # check collisions
    died = collide_player(PLAYER, list_group_boundarties_floor, "list")
    if died:
        reset_game(PLAYER)

    direction_distance = {}
    for direction in ["left", "right", "up", "down"]:
        distance = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
        direction_distance[direction] = distance

    pygame.display.flip()
    CLOCK.tick(60)


# TODO: create the game with the prediction of the AI  TRY IT
# TODO: Put the distance for boundaries at the edges of the player 