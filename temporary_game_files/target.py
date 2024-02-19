from pygame.sprite import Sprite
from pygame import Surface, Rect
import numpy as np

class Target(Sprite):
    def __init__(self):
        # INFO: work with position on the center of the target
        pos = (900, 850)
        width = 20
        height = 20

        self.image = Surface((width, height))
        self.rect = self.image.get_rect(center=pos)


    def generate_position(self, exits):
        list_exits = [sprite for sprite in exits]

        random_exit = np.random.choice(list_exits)
        
        self.rect.center = random_exit.rect.center

    def collision(self, sprite):
        if Rect.colliderect(self.rect, sprite.rect):
            print("collided target")
            return True
    