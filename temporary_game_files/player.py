from pygame.sprite import Sprite, collide_rect
from pygame.image import load
from pygame import mask, Rect, Surface
import pygame
import os
import numpy as np


class Player(Sprite):
    def __init__(self):
        # INFO: work with position on the center of the rectangle
        # INFO: player size: 16x16 pixels
        initial_pos = (32, 32)
        size = (32, 32)
        
        self.image = Surface((size))
        self.rect = self.image.get_rect(topleft=initial_pos)
        self.mask = mask.from_surface(self.image)

    def update(self, action): 
        speed_player = 1

        if action == 0: # up
            self.rect.y -= speed_player
        elif action == 1: # down
            self.rect.y += speed_player
        elif action == 2: # left
            self.rect.x -= speed_player
        elif action == 3: # right
            self.rect.x += speed_player

    def generate_position(self, ground):
        list_ground = [sprite for sprite in ground]

        random_ground_tile = np.random.choice(list_ground)
        
        self.rect.center = random_ground_tile.rect.center


    def collision(self, obstacles):
        for sprite in obstacles:
            collision = collide_rect(self, sprite)

            if collision: return True