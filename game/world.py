import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, layer, groups):
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self._layer = layer
        super().__init__(groups)
        

class World:
    def __init__(self):
        self.tmx_data = load_pygame("../assets/tsx/basic.tmx")

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group_objects = pygame.sprite.Group()
        self.sprite_group_floor = pygame.sprite.Group()

    def create_tiles(self):
        layer_index = 0
        for layer in self.tmx_data:
            if hasattr(layer, "data"):
                if layer.name == "Floor grass":
                    for x, y, surf in layer.tiles():
                        pos = (x*32, y*32)
                        Tile(pos=pos, surf=surf, layer=layer_index, groups=self.sprite_group_floor)
                else:
                    for x, y, surf in layer.tiles():
                        pos = (x*32, y*32)
                        Tile(pos=pos, surf=surf, layer=layer_index, groups=self.sprite_group)
            layer_index += 1
                    
    def create_objects(self):
        layer_index = 0
        for obj in self.tmx_data.objects:
            pos = (obj.x, obj.y)
            if obj.type in ("Vegetation", "Props"):
                Tile(pos=pos, surf=obj.image, layer=layer_index, groups=self.sprite_group_objects)
            layer_index += 1
