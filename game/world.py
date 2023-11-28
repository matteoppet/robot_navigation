import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class World:
    def __init__(self):
        self.tmx_data = load_pygame("../assets/tsx/basic.tmx")

        self.sprite_group = pygame.sprite.Group()

    def create_tiles(self):
        for layer in self.tmx_data:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x*32, y*32)
                    Tile(pos=pos, surf=surf, groups=self.sprite_group)
                    
    def create_objects(self):
        for obj in self.tmx_data.objects:
            pos = (obj.x, obj.y)
            if obj.type in ("Vegetation", "Props"):
                Tile(pos=pos, surf=obj.image, groups=self.sprite_group)