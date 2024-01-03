import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Game stuff imports
from helpers.player import Player
from helpers.world import World
from helpers.helpers import collide_player, create_random_position_for_ai, create_table_tiles, calculate_distance_boundaries


import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1120, 992))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("jetbrainsmono", 14)

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

# player section
PLAYER = Player()

TABLE_TILES = create_table_tiles(sprite_group_boundaries_floor)

class Goal(pygame.sprite.Sprite):
    def __init__(self):
        self.index = 0

        self.x, self.y = create_random_position_for_ai(list_group_path)

        self.image = pygame.Surface((20, 20))
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)

    def next_goal(self):
        self.x, self.y = create_random_position_for_ai(list_group_path)
        self.rect.x, self.rect.y = self.x, self.y


GOAL = Goal()


class Robot(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(9,), dtype=np.float64)
        
        self.old_distance = 10000

    def step(self, action):

        sprite_group_boundaries_floor.draw(SCREEN)
        sprite_group_path.draw(SCREEN)
        sprite_group.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # action
        PLAYER.ai_move(action)

        SCREEN.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
        pygame.draw.rect(SCREEN, "red", (GOAL.x, GOAL.y, 20, 20))

        # done variable
        self.terminated = False
        self.truncated = False
        if PLAYER.y < 0 and (PLAYER.y+32) > 992:
            self.truncated = True
        elif PLAYER.x < 0 and (PLAYER.x+32) > 1120:
            self.truncated = True
        
        # reward variable
        self.distance = pygame.math.Vector2(PLAYER.rect.centerx, PLAYER.rect.centery).distance_to((GOAL.x, GOAL.y))
        self.reward, self.terminated = self.reward_function(self.distance)

        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        self.direction_distance_texts(direction_distance)

        # update observation
        self.observation = self.get_observation(direction_distance)
        self.info = {}

        pygame.display.flip()
        pygame.display.update()
        CLOCK.tick(self.metadata["render_fps"])
 
        return self.observation, self.reward, self.terminated, self.truncated, self.info
    

    def reward_function(self, distance_from_goal):
        COLLISION_PENALTY = -10.0
        GOAL_REWARD = 100.0
        DISTANCE_PENALTY_WEIGHT = 0.01

        goal_reached = pygame.sprite.collide_rect(PLAYER, GOAL)
        if goal_reached:
            GOAL.next_goal()
            return GOAL_REWARD, False # The false return is for the self.terminated variable

        collision_boundaries = collide_player(PLAYER, list_group_boundarties_floor, "list")
        if collision_boundaries:
            return COLLISION_PENALTY, True # The true return is for the self.terminated variable
        
        distance_penalty = -DISTANCE_PENALTY_WEIGHT * distance_from_goal
        total_reward = GOAL_REWARD + distance_penalty

        return total_reward, False # The false return is for the self.terminated variable


    def get_observation(self, direction_distance):
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
        observation = np.array(
            [
                PLAYER.rect.centerx, 
                PLAYER.rect.centery, 
                GOAL.x, 
                GOAL.y, 
                self.distance,
                direction_distance["left"],
                direction_distance["right"],
                direction_distance["up"],
                direction_distance["down"]
            ])
        return observation


    def direction_distance_texts(self, direction_distance):
        left_text = FONT.render(f"{direction_distance['left']}", True, "red")
        right_text = FONT.render(f"{direction_distance['right']}", True, "red")
        up_text = FONT.render(f"{direction_distance['up']}", True, "red")
        down_text = FONT.render(f"{direction_distance['down']}", True, "red")
        SCREEN.blit(left_text, (PLAYER.x - 20, PLAYER.y +16))
        SCREEN.blit(right_text, (PLAYER.x + 30, PLAYER.y +16))
        SCREEN.blit(up_text, (PLAYER.x +4, PLAYER.y -20))
        SCREEN.blit(down_text, (PLAYER.x + 4, PLAYER.y +50))


    def reset(self, seed=None, options=None):
        PLAYER.reset()
        self.distance = pygame.math.Vector2(PLAYER.rect.centerx, PLAYER.rect.centery).distance_to((GOAL.x, GOAL.y))

        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        # update observation
        self.observation = self.get_observation(direction_distance)
        info = {}

        return self.observation, info