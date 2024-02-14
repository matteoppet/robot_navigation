import gymnasium as gym
from gymnasium import spaces

# utils class
from world import sprite_ground, sprite_boundaries
from player import Player
from target import Target
from sensors import calculate_distance
from settings import WINDOW_X, WINDOW_Y, TILE_WIDTH, TILE_HEIGHT

import pygame
import os
import numpy as np 


class RobotWorld(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode=None):
        low_agent = np.array([0 for _ in range(0, 19)])
        high_agent = np.array([np.inf for _ in range(0, 19)])
        low_target = np.array([0, 0])
        high_target = np.array([880, 560])


        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    low=low_agent,
                    high=high_agent,
                    shape=(19,),
                    dtype=np.float64
                ),
                
                "target": spaces.Box(
                    low=low_target,
                    high=high_target,
                    shape=(2,),
                    dtype=np.float64
                )
            }
        )

        # actions: "up", "down", "left", "right"
        self.action_space = spaces.Discrete(4)

        self.render_mode = render_mode

        # if human-rendering is used
        self.window = None
        self.clock = None

        self.SPRITE_GROUND = sprite_ground
        self.SPRITE_BOUNDARIES = sprite_boundaries

        self.PLAYER = Player()
        self.TARGET = Target()

        self.prev_base_reward = None


    def _get_obs(self):
        info_sensors = self._get_info_sensors()
        agent_obs = [
            self._agent_location[0], 
            self._agent_location[1],
            self._get_distance_from_target()]
        agent_obs.append(info["distance"] for sensor_name, info in info_sensors.items())

        return {
            "agent": np.array(agent_obs),

            "target": np.array([
                self._target_location[0],
                self._target_location[1]
            ])
        }


    def _get_info_sensors(self):
        return calculate_distance(self.PLAYER, self.SPRITE_BOUNDARIES)


    def _get_distance_from_target(self):
        return np.linalg.norm(np.array(
            np.array([*self._agent_location]) - np.array([*self._target_location])
        ))


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.TARGET.generate_position(self.SPRITE_GROUND)
        self._target_location = self.TARGET.rect.center

        self.PLAYER.generate_position(self.SPRITE_GROUND)
        self._agent_location = self.PLAYER.rect.center

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self._render_frame()

        return observation, info


    def reward_function(self, crash, target_reached):
        reward = 0
        distance = self._get_distance_from_target()

        base_reward = -50*distance
        if self.prev_base_reward is not None:
            reward = base_reward - self.prev_base_reward
        self.prev_base_reward = base_reward

        if crash:
            reward = -200.0
        
        if target_reached:
            reward = 500.0
            self.TARGET.generate_position(self.SPRITE_GROUND)
        return reward


    def step(self, action):
        self.PLAYER.update(action)
        self._agent_location = self.PLAYER.rect.center

        # episode terminated if there is a collision or the agent reach the target
        terminated = False
        agent_crashed = self.PLAYER.collision(self.SPRITE_BOUNDARIES) # handled in player file
        agent_target_reached = self.TARGET.collision(self.PLAYER) # handled in target file

        if agent_crashed or agent_target_reached:
            terminated = True

        reward = self.reward_function(agent_crashed, agent_target_reached)

        self._target_location = self.TARGET.rect.center

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self._render_frame()
        
        return observation, reward, terminated, False, info


    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("AI Movements")
            pygame.font.init()

            window_size = (WINDOW_X, WINDOW_Y)
            self.window = pygame.display.set_mode(window_size)
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":

            for sprite in self.SPRITE_BOUNDARIES:
                rect = pygame.Rect(sprite.rect.x, sprite.rect.y, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.window, "gray", rect)

            for sprite in self.SPRITE_GROUND:
                rect = pygame.Rect(sprite.rect.x, sprite.rect.y, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.window, "white", rect)

            data_sensors = self._get_info_sensors()
            for name_sensor, info_sensor in data_sensors.items():
                
                if info_sensor["point_of_collision"] != None:
                    x_collision = info_sensor["point_of_collision"][0]
                    y_collision = info_sensor["point_of_collision"][1]
                    rect_sensor = pygame.Rect(x_collision, y_collision, 3, 3)

                    pygame.draw.rect(self.window, "red", rect_sensor)

            pygame.draw.rect(self.window, "green", self.PLAYER.rect)

            rect_target = pygame.Rect(self._target_location[0], self._target_location[1], 10, 10)
            pygame.draw.rect(self.window, "blue", rect_target)

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


# adjust rect sensors