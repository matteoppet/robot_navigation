import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Game stuff imports
from helpers.player import Player
from helpers.world import World
from helpers.helpers import create_table_tiles, calculate_distance_boundaries

import pygame


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x, self.y = (222, 840)
        self.width, self.height = (25, 25)

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)


class Boundarie(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        self.image = pygame.Surface(pos)
        self.rect = self.image.get_rect(toplet=pos)

        super().__init__(group)



class RobotWorld(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    PLAYER = Player()
    GOAL = Goal()

    def __init__(self, window_mode, window_size, clock_global_var, render_mode=None):

        self.window_mode = window_mode
        self.window_size_x, self.window_size_y = window_size
        self.clock_global_var = clock_global_var

        # agent: pos_x, pos_y, distance_from_goal, sensors (all 4 side)
        # target: pos_x, pos_y
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    low=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                    high=np.array([self.window_size_x, self.window_size_y, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]),
                    shape=(11,),
                    dtype=np.float64),
                
                "target": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([self.window_size_x, self.window_size_y]),
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
        # initialize immediately 
        self.window = self.window_mode
        self.clock = self.clock_global_var

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


    def _get_distance_info(self):
        return {"distance": np.linalg.norm(np.array([self._agent_location[0], self._agent_location[1]]) - np.array([self._target_location[0], self._target_location[1]]), ord=1)}


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

        return reward


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._target_location = (self.GOAL.x, self.GOAL.y)
        self._agent_location = (self.player_x_init, self.player_y_init)

        observation = self._get_obs()
        info = self._get_distance_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    

    def step(self, action):
        self.PLAYER.ai_move(action)

        self._sensor_left = {}

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
        if self.render_mode == "human":
            SPRITE_GROUP_BOUNDARIES.draw(self.window)
            SPRITE_GROUP_PATH.draw(self.window)
            SPRITE_GROUP.draw(self.window)

            self.window.blit(self.PLAYER.image, (self.PLAYER.x, self.PLAYER.y))
            self.window.blit(self.GOAL.image, (self.GOAL.x, self.GOAL.y))

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


pygame.init()
pygame.display.init()
clock = pygame.time.Clock()

# Size PyGame window
window_size = (1120, 1024)

window_mode = pygame.display.set_mode(window_size)


WORLD = World()
WORLD.create_tiles()

SPRITE_GROUP = WORLD.sprite_group

SPRITE_GROUP_BOUNDARIES = WORLD.sprite_group_boundaries_floor
LIST_GROUP_BOUNDARIES = [sprite for sprite in SPRITE_GROUP_BOUNDARIES]

SPRITE_GROUP_PATH = WORLD.sprite_group_path
LIST_GROUP_PATH = [sprite for sprite in SPRITE_GROUP_PATH]

TABLE_TILES = create_table_tiles(SPRITE_GROUP_BOUNDARIES)


# train this agent
# random position agent not used