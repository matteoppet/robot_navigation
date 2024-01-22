import gymnasium as gym
from gymnasium import spaces

# Helpers imports
from helpers.player import Player
from helpers.helpers import create_table_tiles, calculate_distance_boundaries
from helpers.csv_world import sprite_boundaries, sprite_path

import pygame

import os
import numpy as np


SPRITE_GROUP_BOUNDARIES = sprite_boundaries
LIST_GROUP_BOUNDARIES = [sprite for sprite in SPRITE_GROUP_BOUNDARIES]

TABLE_TILES = create_table_tiles(SPRITE_GROUP_BOUNDARIES)

SPRITE_GROUP_PATH = sprite_path
LIST_GROUP_PATH = [sprite for sprite in SPRITE_GROUP_PATH]


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x, self.y = (975, 250)
        self.width, self.height = (25, 25)

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def generate_goal(self):
        # get the center of random index tile of the path and use this
        random_tile = np.random.choice(LIST_GROUP_PATH)
        
        center_pos_x = random_tile.rect.centerx 
        center_pos_y = random_tile.rect.centery

        # change x and y of the agent and also of the rectangle
        self.x = center_pos_x
        self.y = center_pos_y

        self.rect.x = self.x
        self.rect.y = self.y


class Boundarie(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        self.image = pygame.Surface(pos)
        self.rect = self.image.get_rect(toplet=pos)

        super().__init__(group)


class RobotWorld(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    PLAYER = Player()
    GOAL = Goal()

    def __init__(self, render_mode=None):
        # agent: pos_x, pos_y, distance_from_goal, sensors (all 4 side)
        # target: pos_x, pos_y
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    low=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                    high=np.array([1120, 1024, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]),
                    shape=(11,),
                    dtype=np.float64),
                
                "target": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([1120, 1024]),
                    shape=(2,),
                    dtype=np.float64)
            }
        )
        # actions: "up", "down", "left", "right"
        self.action_space = spaces.Discrete(4)

        self.render_mode = render_mode
        print("Render mode given:", self.render_mode)

        # if human-rendering is used
        self.window = None # window to draw on
        self.clock = None # correct framerate in human-mode

        self.prev_base_reward = None

        # player initial positions INFO: if changes, change in player file too (helpers dir)
        self.player_x_init = 975
        self.player_y_init = 150


    def _get_obs(self):
        distance = self._get_distance_info()
        return {
            "agent": np.array([
                self._agent_location[0],
                self._agent_location[1],
                distance["distance"],
                *self.get_sensors_distance("left"),
                *self.get_sensors_distance("right"),
                *self.get_sensors_distance("up"),
                *self.get_sensors_distance("down")
            ]),
            "target": np.array([
                self._target_location[0],
                self._target_location[1]
            ])
        }


    # if want return something else, add to the dict and change the name of the fuction to "_get_info"
    def _get_distance_info(self):
        return {"distance": np.linalg.norm(np.array([self._agent_location[0], self._agent_location[1]]) - np.array([self._target_location[0], self._target_location[1]]), axis=-1)}


    def random_agent_location(self, boundaries):
        r = True
        while r:
            random_x, random_y = np.random.randint(0, self.window_size_x), np.random.randint(0, self.window_size_y)
            temporary_rect = pygame.Rect(random_x, random_y, 40, 40) # the agent's width, height: plus +20 each
            possible = pygame.Rect.collidelist(temporary_rect, boundaries)

            self._agent_location = (random_x, random_y)

            distance_from_goal = self._get_distance_info()

            self._agent_location = (random_x, random_y) # stored temporarily, changed after
            if possible == -1 and not distance_from_goal["distance"] < 100:
                r = False
                return (random_x, random_y)
            
        raise("Error: Unable to find a valid agent location")


    def collision_agent(self, agent, boundaries):
        for sprite in boundaries:
            collisions = pygame.sprite.collide_rect(agent, sprite)
            if collisions:
                return True


    def goal_reached(self, agent, goal):
        collisions = pygame.sprite.collide_rect(agent, goal)
        if collisions:
            return True


    def get_sensors_distance(self, direction):
        if direction == "left":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, self.PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "right":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, self.PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "up":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, self.PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "down":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, self.PLAYER, direction)
            return [distance_1, distance_2]
        
    
    def info_display(self):
        # Rectangle to write the info on
        # Agent coordinates
        # Target coordinates
        # Distance
        
        base = pygame.draw.rect(
            self.window,
            "black",
            (590, 10, 260, 145),
            border_radius=2
        )

        font = pygame.font.SysFont("arialblack", 18)

        pos_text_player_position = (605, 30)
        player_position = font.render(
            f"PLAYER: x: {self._agent_location[0]}, y: {self._agent_location[1]}",
            False,
            (255, 255, 255)
        )
        self.window.blit(player_position, pos_text_player_position)

        pos_text_target_position = (605, 70)
        target_position = font.render(
            f"TARGET: x: {self._target_location[0]}, y: {self._target_location[1]}",
            False,
            (255, 255, 255)
        )
        self.window.blit(target_position, pos_text_target_position)

        pos_distance_text = (605, 110)
        distance_dict = self._get_distance_info()
        distance = font.render(
            f"Distance: {distance_dict['distance']:.2f}",
            False,
            (255, 255, 255)
        )
        self.window.blit(distance, pos_distance_text)
      
    
    def reward_function(self, crash, goal_reached):
        reward = 0
        distance = self._get_distance_info()

        base_reward = -50*distance["distance"]
        if self.prev_base_reward is not None:
            reward = base_reward - self.prev_base_reward
        self.prev_base_reward = base_reward

        if crash:
            reward = -200.0

        if goal_reached:
            reward = 100.0
            self.GOAL.generate_goal()
            print("generate next goal")

        return reward


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._target_location = (self.GOAL.x, self.GOAL.y)
        self._agent_location = (self.player_x_init, self.player_y_init)

        self.PLAYER.x, self.PLAYER.y = self._agent_location
        self.PLAYER.rect.x, self.PLAYER.rect.y = self.PLAYER.x, self.PLAYER.y

        observation = self._get_obs()
        info = self._get_distance_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    

    def step(self, action):
        self.PLAYER.ai_move(action)
        self._agent_location = (self.PLAYER.x, self.PLAYER.y)

        # episode terminated if there is a collision or the agent reach the goal
        terminated = False
        agent_crashed = self.collision_agent(self.PLAYER, LIST_GROUP_BOUNDARIES)
        agent_reached_goal = self.goal_reached(self.PLAYER, self.GOAL)

        if agent_crashed or agent_reached_goal:
            terminated = True

        reward = self.reward_function(agent_crashed, agent_reached_goal)

        observation = self._get_obs()
        info = self._get_distance_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info        
    

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('Agent movements')
            pygame.font.init()

            window_size = (1120, 1024)
            self.window = pygame.display.set_mode(window_size)

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        map_path = os.path.join(os.path.dirname(__file__), "../assets/images/basic_4.png")
        map_image = pygame.image.load(map_path)

        if self.render_mode == "human":

            self.window.blit(map_image, (0,0))

            self.window.blit(self.PLAYER.image, (self.PLAYER.x, self.PLAYER.y))
            self.window.blit(self.GOAL.image, (self.GOAL.x, self.GOAL.y))

            self.info_display()

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

