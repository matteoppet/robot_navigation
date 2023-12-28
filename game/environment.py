import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Game stuff imports
from game.helpers.player import Player
from game.helpers.world import World
from game.helpers.sensors import create_sensors, draw_lines, sprite_group_sensors
from game.helpers.helpers import collide_player, collide_sensors, reset_game, mouse_function, create_random_position_for_ai, create_table_tiles, calculate_distance_boundaries
from game.helpers.settings import LENGTH_SENSOR


import pygame

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

# player section
PLAYER = Player()

# sensors section
create_sensors(PLAYER.rect.centerx, PLAYER.rect.centery, length_sensor=LENGTH_SENSOR)
sprite_group_sens = sprite_group_sensors
global_list_sensors_colliding = []


TABLE_TILES = create_table_tiles(sprite_group_boundaries_floor)


class Robot(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(4)
        """
            1. position x (center of the rect)
            2. position y (center of the rect)
            3. position x goal (center of the rect)
            4. position y goal (center of the rect)
            5. distance from goal
            6. sensor left
            7. sensor right
            8. sensor up
            9. sensor down
        """
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(9,), dtype=np.float64)
        
        self.old_distance = 10000

        self.POSITION_TO_MOVE = create_random_position_for_ai(list_group_boundarties_floor)


    def step(self, action):
        # action
        PLAYER.ai_move(action)

        # done variable
        self.terminated = False
        self.truncated = False
        if PLAYER.y < 0 and PLAYER.y > 992:
            self.truncated = True
        elif PLAYER.x < 0 and PLAYER.x > 1120:
            self.truncated = True
        
        # reward variable
        self.reward = 0
   
        x_goal, y_goal = self.POSITION_TO_MOVE
        if PLAYER.rect.centerx == x_goal and PLAYER.rect.centery == y_goal:
            print("Goal reached")
            self.reward += 1000
            self.terminated = True # when the player has reached the goal, the episode terminates
        if collide_player(PLAYER, list_group_boundarties_floor, "list"):
            self.reward -= 100
            self.truncated = True

        self.distance = np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([x_goal, y_goal]))
        if self.distance < self.old_distance:
            self.reward += 1
        else:
            self.reward -= 1
        self.old_distance = self.distance

        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        # update observation
        self.observation = np.array(
            [
                PLAYER.rect.centerx, 
                PLAYER.rect.centery, 
                x_goal, 
                y_goal, 
                self.distance,
                direction_distance["left"],
                direction_distance["right"],
                direction_distance["up"],
                direction_distance["down"]
            ])
        self.info = {}


        return self.observation, self.reward, self.terminated, self.truncated, self.info


    def reset(self, seed=None, options=None):
        PLAYER.reset()
        self.POSITION_TO_MOVE = create_random_position_for_ai(list_group_boundarties_floor)
        x_goal, y_goal = self.POSITION_TO_MOVE
        self.distance = np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([x_goal, y_goal]))
        
        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        # update observation
        self.observation = np.array(
            [
                PLAYER.rect.centerx, 
                PLAYER.rect.centery, 
                x_goal, 
                y_goal, 
                self.distance,
                direction_distance["left"],
                direction_distance["right"],
                direction_distance["up"],
                direction_distance["down"]
            ])
        info = {}

        return self.observation, info


    def render(self):
        sprite_group_boundaries_floor.draw(SCREEN)
        sprite_group.draw(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        SCREEN.blit(PLAYER.image, (PLAYER.x, PLAYER.y))

        pygame.display.flip()
        pygame.display.update()
        CLOCK.tick(self.metadata["render_fps"])


# TODO: works, but there are not boundaries, the AI doesn't care about boundaries (CHECK REWARDS)
# TODO: init the pygame screen only if the render function is being called
        
# calculate the distance from the boundaries