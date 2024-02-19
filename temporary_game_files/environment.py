import gymnasium as gym
from gymnasium import spaces

# utils class
from world import walls_sprites_group, ground_sprites_group, exits_sprites_group
from player import Player
from target import Target
from sensors import calculate_distance, lines_data
from settings import WINDOW_X, WINDOW_Y

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

        self.WALLS_SPRITES_GROUP = walls_sprites_group
        self.GROUND_SPRITES_GROUP = ground_sprites_group
        self.EXITS_SPRITES_GROUP = exits_sprites_group

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
        return calculate_distance(self.PLAYER, self.WALLS_SPRITES_GROUP)


    def _get_distance_from_target(self):
        return np.linalg.norm(np.array(
            np.array([*self._agent_location]) - np.array([*self._target_location])
        ))
    

    def _get_positions_sensors_lines(self):
        return lines_data(self.PLAYER)


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.TARGET.generate_position(self.EXITS_SPRITES_GROUP)
        self._target_location = self.TARGET.rect.center

        self.PLAYER.generate_position(self.GROUND_SPRITES_GROUP)
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
            self.TARGET.generate_position(self.EXITS_SPRITES_GROUP)
            
        return reward


    def step(self, action):
        self.PLAYER.update(action)
        self._agent_location = self.PLAYER.rect.center

        # episode terminated if there is a collision or the agent reach the target
        terminated = False
        agent_crashed = self.PLAYER.collision(self.WALLS_SPRITES_GROUP) # handled in player file
        agent_target_reached = self.TARGET.collision(self.PLAYER) # handled in target file

        if agent_crashed or agent_target_reached:
            terminated = True

        reward = self.reward_function(agent_crashed, agent_target_reached)

        observation = self._get_obs()
        info = {}

        self._target_location = self.TARGET.rect.center

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

        
        map_png_path = "../temporary_map_files/tileset_dungeon_2/png/map.png"
        map_file = os.path.join(os.path.dirname(__file__), map_png_path)
        map = pygame.image.load(map_file)

        if self.render_mode == "human":

            # self.window.fill("white")

            # for sprite in self.OBSTACLE_SPRITES_GROUP:
            #     border_thickness = 2

            #     color_obstacles = (61, 61, 61)
            #     pygame.draw.rect(self.window, color_obstacles, sprite.rect, border_thickness, border_radius=2)


            # data_sensors = self._get_info_sensors()
            # lines_position_data = self._get_positions_sensors_lines()
            # for name_sensor, info_sensor in data_sensors.items():
                
            #     pos_start = lines_position_data[name_sensor]["pos_start"]
            #     pos_end = lines_position_data[name_sensor]["pos_end"]
            #     color_lines = (230, 230, 230)
            #     pygame.draw.line(self.window, color_lines, pos_start, pos_end)
                
            #     if info_sensor["point_of_collision"] != None:
            #         x_collision = info_sensor["point_of_collision"][0]
            #         y_collision = info_sensor["point_of_collision"][1]
                    
            #         pygame.draw.circle(self.window, "red", (x_collision, y_collision), radius=2)


            # color_player = (126, 97, 173)
            # border_thickness = 2
            # pygame.draw.rect(self.window, color_player, self.PLAYER.rect, border_thickness)

            # rect_target = pygame.Rect(self._target_location[0], self._target_location[1], 30, 30)
            # pygame.draw.rect(self.window, "blue", rect_target)


            self.window.fill("black")

            for sprite in self.WALLS_SPRITES_GROUP:
                pygame.draw.rect(self.window, "gray", sprite.rect)

            for sprite in self.GROUND_SPRITES_GROUP:
                pygame.draw.rect(self.window, "white", sprite.rect)

            pygame.draw.rect(self.window, (126, 97, 173), self.PLAYER.rect)

            data_sensors = self._get_info_sensors()
            lines_position_data = self._get_positions_sensors_lines()
            for name_sensor, info_sensor in data_sensors.items():
                
                pos_start = lines_position_data[name_sensor]["pos_start"]
                pos_end = lines_position_data[name_sensor]["pos_end"]
                color_lines = (230, 230, 230)
                pygame.draw.line(self.window, color_lines, pos_start, pos_end)
                
                if info_sensor["point_of_collision"] != None:
                    x_collision = info_sensor["point_of_collision"][0]
                    y_collision = info_sensor["point_of_collision"][1]
                    
                    pygame.draw.circle(self.window, "red", (x_collision, y_collision), radius=2)

            # self.window.blit(map, (0, 0))

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


# increase length sensors