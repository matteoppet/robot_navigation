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
        size = (16, 16)
        
        self.image = Surface((size))
        self.rect = Rect(*initial_pos, 16, 16)
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

    def generate_position(self, path):
        list_sprites = [sprite for sprite in path]
        random_tile = np.random.choice(list_sprites)
        center_pos_x = random_tile.rect.centerx
        center_pos_y = random_tile.rect.centery

        self.rect.centerx = center_pos_x
        self.rect.centery = center_pos_y


    def collision(self, obstacles):
        for sprite in obstacles:
            collision = collide_rect(self, sprite)

            if collision: return True