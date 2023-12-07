from pygame import sprite, Surface, SRCALPHA, mask # import specific function 
from helpers import create_list_buondaries

sprite_group_boundaries = sprite.Group()

class Boundaries(sprite.Sprite):
    def __init__(self, size, pos, list_points):
        sprite.Sprite.__init__(self)

        # Create transparent background image
        self.image = Surface(size, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Draw polygon
        self.points = list_points

        # Create the collision mask
        self.mask = mask.from_surface(self.image)


# FIX OTHERS BOUNDARIES: it doesn't find it
def create_boundaries():
    for index in range(1, 3):
        list_points = create_list_buondaries("Delimitator", index)
        surface = Boundaries((20, 20), (0, 0), list_points) # check if position and size are correct
        sprite_group_boundaries.add(surface)        


# HERE I CREATE THE BOUNDARIES SPRITES
# I CALL CREATE_BOUNDARIES IN MAIN.PY
# THEN IT CALLS BUONDARIES CLASS AND CREATES THE SPRITE
# THEN I GO THROUGH THE SPRITES IN THE GROUP AND DRAW IT IN MAIN.PY
