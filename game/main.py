import pygame
from helpers.player import Player
from helpers.world import World
from helpers.helpers import collide_player, reset_game, mouse_function, create_distance_sprites, create_table_tiles, calculate_distance_boundaries
import numpy as np
from stable_baselines3 import PPO 


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

sprite_group_path = WORLD.sprite_group_path
list_group_path = [sprite for sprite in WORLD.sprite_group_path]

TABLE_TILES = create_table_tiles(sprite_group_boundaries_floor)


# player section
PLAYER = Player()


# DISTANCE
create_distance_sprites()
sprite_group_for_distance = create_distance_sprites()

goal_position = (0,0)

models_dir = "models/1703967944"
model_path = f"{models_dir}/300000.zip"
model = PPO.load(model_path)

running = True
while running:
    
    # draw sprites
    sprite_group_boundaries_floor.draw(SCREEN)
    sprite_group_path.draw(SCREEN)
    sprite_group.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        goal_position = mouse_function(event, list_group_path, SCREEN)

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

    #print(pygame.font.get_fonts())

    font = pygame.font.SysFont("jetbrainsmono", 14)
    left_text = font.render(f"{direction_distance['left']}", True, "red")
    right_text = font.render(f"{direction_distance['right']}", True, "red")
    up_text = font.render(f"{direction_distance['up']}", True, "red")
    down_text = font.render(f"{direction_distance['down']}", True, "red")
    SCREEN.blit(left_text, (PLAYER.x - 20, PLAYER.y +16))
    SCREEN.blit(right_text, (PLAYER.x + 30, PLAYER.y +16))
    SCREEN.blit(up_text, (PLAYER.x +4, PLAYER.y -20))
    SCREEN.blit(down_text, (PLAYER.x + 4, PLAYER.y +50))
    
    if goal_position != (0,0):
        distance_from_goal = np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([goal_position[0], goal_position[1]]))

        obs = np.array([
            PLAYER.rect.centerx,
            PLAYER.rect.centery,
            goal_position[0],
            goal_position[1],
            distance_from_goal,
            direction_distance["left"],
            direction_distance["right"],
            direction_distance["up"],
            direction_distance["down"]
        ])

        action, _ = model.predict(obs)
        PLAYER.ai_move(action)
        

    pygame.display.flip()
    CLOCK.tick(60)


# some problem with sensors, adjust that