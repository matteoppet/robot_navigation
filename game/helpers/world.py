import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, name, pos, surf, layer, groups):
        self.name = name
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self._layer = layer
        super().__init__(groups)
        

class World:
    def __init__(self):
        self.tmx_data = load_pygame("../assets/tsx/basic_3.tmx")

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group_objects = pygame.sprite.Group()
        self.sprite_group_boundaries_floor = pygame.sprite.Group()
        self.sprite_group_path = pygame.sprite.Group()

    def create_tiles(self):
        layer_index = 0
        index_name_boundaries = 0
        index_name_others = 0
        for layer in self.tmx_data:
            if hasattr(layer, "data"):
                if layer.name == "Boundaries grass":
                    for x, y, surf in layer.tiles():
                        pos = (x*32, y*32)
                        Tile(name=index_name_boundaries, pos=pos, surf=surf, layer=layer_index, groups=self.sprite_group_boundaries_floor)
                        index_name_boundaries += 1
                elif layer.name == "Path":
                    for x, y, surf in layer.tiles():
                        pos = (x*32, y*32)
                        Tile(name=index_name_boundaries, pos=pos, surf=surf, layer=layer_index, groups=self.sprite_group_path)
                        index_name_boundaries += 1
                else:
                    for x, y, surf in layer.tiles():
                        pos = (x*32, y*32)
                        Tile(name=index_name_others, pos=pos, surf=surf, layer=layer_index, groups=self.sprite_group)
                        index_name_others += 1
                
            layer_index += 1
                    
    def create_objects(self):
        layer_index = 0
        index_name_objects = 0
        for obj in self.tmx_data.objects:
            pos = (obj.x, obj.y)
            if obj.type in ("Vegetation", "Props"):
                Tile(name=index_name_objects, pos=pos, surf=obj.image, layer=layer_index, groups=self.sprite_group_objects)
                index_name_objects += 1
            layer_index += 1
