from pygame.sprite import Sprite
from pygame import Surface, Rect
import numpy as np

class Target(Sprite):
    def __init__(self):
        # INFO: work with position on the center of the target
        pos = (100, 100)
        width = 20
        height = 20

        self.image = Surface((width, height))
        self.rect = self.image.get_rect(center=pos)


    def generate_position(self, path):
        list_sprites = [sprite for sprite in path]
        random_tile = np.random.choice(list_sprites)
        center_pos_x = random_tile.rect.centerx
        center_pos_y = random_tile.rect.centery

        self.rect.centerx = center_pos_x
        self.rect.centery = center_pos_y

    def collision(self, sprite):
        if Rect.colliderect(self.rect, sprite.rect):
            print("collided target")
            return True