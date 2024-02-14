import pygame
import os
from utils.player import Player
from stable_baselines3 import PPO
import numpy as np
from utils.helpers import create_table_tiles, calculate_distance_boundaries
from utils.csv_world import sprite_boundaries, sprite_path


class Goal:
    def __init__(self):
        super().__init__()

        self.x, self.y = (975, 250)
        self.width, self.height = (25, 25)

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)


class Agent:
    def __init__(self):
        id_model = "1706883391"
        timesteps = "7000000"
        self.model = PPO.load(f"training_agent/models/{id_model}/PPO_MODEL_{timesteps}")

    def get_game_state(self):
        return {
            "agent": np.array([
                PLAYER.x,
                PLAYER.y,
                self.get_distance_from_goal(),
                *self.get_sensors_distance("left"),
                *self.get_sensors_distance("right"),
                *self.get_sensors_distance("up"),
                *self.get_sensors_distance("down")
            ]),
            "target": np.array([
                GOAL.rect.x,
                GOAL.rect.y
            ])
        }

    def get_distance_from_goal(self):
        return np.linalg.norm(np.array([PLAYER.x, PLAYER.y]) - np.array([GOAL.rect.x, GOAL.rect.y]), axis=-1)

    def get_sensors_distance(self, direction):
        if direction == "left":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "right":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "up":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            return [distance_1, distance_2]

        if direction == "down":
            distance_1, distance_2, index_tile_1, index_tile_2 = calculate_distance_boundaries(TABLE_TILES, PLAYER, direction)
            return [distance_1, distance_2]

    def generatation_positions(self, target=None):
        target = target.lower()
        if target == None:
            print("Target value given: None")
        else:
            # get the center of random index tile of the path and use this
            random_tile = np.random.choice(LIST_GROUP_PATH)
            center_pos_x = random_tile.rect.centerx 
            center_pos_y = random_tile.rect.centery

            if target == "player":
                PLAYER.x = PLAYER.rect.x = center_pos_x
                PLAYER.y = PLAYER.rect.y = center_pos_y
            elif target == "goal":
                GOAL.x = GOAL.rect.x = center_pos_x
                GOAL.y = GOAL.rect.y = center_pos_y
            else:
                raise ValueError("Target value error. It must be goal or player.")


def collision_agent(agent, boundaries):
    for sprite in boundaries:
        collisions = pygame.sprite.collide_rect(agent, sprite)
        if collisions:
            return True

def goal_reached(agent, goal):
    collisions = pygame.sprite.collide_rect(agent, goal)
    if collisions:
        return True


pygame.init()
screen = pygame.display.set_mode((1120, 1024))
clock = pygame.time.Clock()
running = True

map_path = os.path.join(os.path.dirname(__file__), "../map_files/png/map.png")
map_image = pygame.image.load(map_path)

PLAYER = Player()
GOAL = Goal()

SPRITE_GROUP_PATH = sprite_path
LIST_GROUP_PATH = [sprite for sprite in SPRITE_GROUP_PATH]

SPRITE_GROUP_BOUNDARIES = sprite_boundaries
LIST_GROUP_BOUNDARIES = [sprite for sprite in SPRITE_GROUP_BOUNDARIES]
TABLE_TILES = create_table_tiles(SPRITE_GROUP_BOUNDARIES)

AGENT = Agent()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_image, (0,0))
    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    screen.blit(GOAL.image, (GOAL.rect.x, GOAL.rect.y))

    action = AGENT.model.predict(AGENT.get_game_state())[0]
    PLAYER.ai_move(action)

    if collision_agent(PLAYER, LIST_GROUP_BOUNDARIES) or goal_reached(PLAYER, GOAL):
        AGENT.generatation_positions("player")
        AGENT.generatation_positions("goal")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()