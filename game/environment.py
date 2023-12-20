import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Game stuff imports
from player import Player
from world import World
from sensors import create_sensors, draw_lines, sprite_group_sensors
from helpers import collide_player, collide_sensors, reset_game, mouse_function
from settings import LENGTH_SENSOR


def update_and_draw_lines():
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
            draw_lines(SCREEN, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height, color="red")
        else:
            draw_lines(SCREEN, sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)


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
        """
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(5,), dtype=np.float64)
        
        self.POSITION_TO_MOVE = (0,0)
        self.old_distance = 10000


    def step(self, action):
        # action
        if action == 0:
            PLAYER.y -= 2
            PLAYER.rect.y -= 2
        elif action == 1:
            PLAYER.y += 2
            PLAYER.rect.y += 2
        elif action == 2:
            PLAYER.x += 2
            PLAYER.rect.x += 2
        elif action == 3:
            PLAYER.x -= 2
            PLAYER.rect.x -= 2

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
            self.reward += 100
        if collide_player(PLAYER, list_group_boundarties_floor):
            self.reward -= 200

        self.distance = np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([x_goal, y_goal]))
        if self.distance < self.old_distance:
            self.reward += 1
        else:
            self.reward -= 1
        self.old_distance = self.distance


        # update observation
        self.observation = np.array([PLAYER.x, PLAYER.x, x_goal, y_goal, self.distance])
        self.info = {}

        return self.observation, self.reward, self.terminated, self.truncated, self.info


    def reset(self, seed=None, options=None):
        PLAYER.reset()
        x_goal, y_goal = (0,0)
        self.POSITION_TO_MOVE = (0,0)
        distance = np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([x_goal, y_goal]))
        
        self.observation = np.array([PLAYER.x, PLAYER.x, x_goal, y_goal, distance])
        info = {}
        return self.observation, info


    def render(self):
        sprite_group_boundaries_floor.draw(SCREEN)
        sprite_group.draw(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.POSITION_TO_MOVE = mouse_function(event, list_group_boundarties_floor, SCREEN)

        SCREEN.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
        PLAYER.move()

        update_and_draw_lines()

        died = collide_player(PLAYER, list_group_boundarties_floor)
        if died:
            reset_game()

        list_sensor_colliding = collide_sensors(sprite_group_sens, sprite_group_boundaries_floor)
        global_list_sensors_colliding = list_sensor_colliding

        pygame.display.flip()
        pygame.display.update()
        CLOCK.tick(self.metadata["render_fps"])



# TODO: create random points where the AI needs to go, then we simulates it with the click of the mouse
    # function situated in helpers.py