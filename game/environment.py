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
        self.POSITIONS_TO_MOVE = [
            (181, 188), 
            (276, 309), 
            (304, 475), 
            (92, 449), 
            (476, 447), 
            (369, 621), 
            (579, 589), 
            (973, 455), 
            (569, 517), 
            (579, 787)]
        self.index = 0

        self.x, self.y = self.POSITIONS_TO_MOVE[self.index]

        self.image = pygame.Surface((20, 20))
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)

    def next_goal(self):
        self.index += 1
        self.x, self.y = self.POSITIONS_TO_MOVE[self.index]
        self.rect.x, self.rect.y = self.POSITIONS_TO_MOVE[self.index]


GOAL = Goal()


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
        self.reward = 0

        collision = pygame.sprite.collide_rect(PLAYER, GOAL)
        if collision:
            print("Goal reached")
            self.reward += 1000
            # self.terminated = True # when the player has reached the goal, the episode terminates
            GOAL.next_goal()
        if collide_player(PLAYER, list_group_boundarties_floor, "list"):
            self.reward -= 100
            self.truncated = True

        self.distance = np.linalg.norm(np.array([PLAYER.rect.centerx, PLAYER.rect.centery]) - np.array([GOAL.x, GOAL.y]))
        if self.distance < self.old_distance:
            self.reward += 1
        else:
            self.reward = -1
        self.old_distance = self.distance

        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        font = pygame.font.SysFont(None, 20)
        left_text = font.render(f"{direction_distance['left']}", True, "red")
        right_text = font.render(f"{direction_distance['right']}", True, "red")
        up_text = font.render(f"{direction_distance['up']}", True, "red")
        down_text = font.render(f"{direction_distance['down']}", True, "red")
        SCREEN.blit(left_text, (PLAYER.x - 20, PLAYER.y +16))
        SCREEN.blit(right_text, (PLAYER.x + 30, PLAYER.y +16))
        SCREEN.blit(up_text, (PLAYER.x +4, PLAYER.y -20))
        SCREEN.blit(down_text, (PLAYER.x + 4, PLAYER.y +50))


        # update observation
        self.observation = np.array(
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
        self.info = {}


        pygame.display.flip()
        pygame.display.update()
        CLOCK.tick(self.metadata["render_fps"])

        return self.observation, self.reward, self.terminated, self.truncated, self.info


    def reset(self, seed=None, options=None):
        PLAYER.reset()
        self.distance = np.linalg.norm(np.array([PLAYER.rect.centerx, PLAYER.rect.centery]) - np.array([GOAL.x, GOAL.y]))

        direction_distance = {}
        for direction in ["left", "right", "up", "down"]:
            distance_boundarie = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            direction_distance[direction] = distance_boundarie

        # update observation
        self.observation = np.array(
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
        info = {}

        return self.observation, info
