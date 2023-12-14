from pygame import Surface, SRCALPHA, sprite, mask, Rect, draw # import specific function 
from helpers import create_list_boundaries

sprite_group_boundaries = sprite.Group()

class Boundaries(sprite.Sprite):
    def __init__(self, vertices):
        super().__init__()
        self.vertices = vertices


        # Creates bounding rectangle for polygon by taking the union of individual
        # rectangles created for each vertex
        self.rect = Rect(vertices[0], (0,0)).unionall([Rect(v, (0,0)) for v in vertices])

        # Generate surface for the mask
        self.mask_surface = self.create_mask_surface()
        # Creates the mask from the surface
        self.mask = mask.from_surface(self.mask_surface)

        # Draw polygon
        self.points = vertices

    def create_mask_surface(self):
        # calculates the minimum and maximum x and y of the polygon vertices 
        # to determine the dimensions of the mask surface
        min_x = min(point[0] for point in self.vertices)
        max_x = max(point[0] for point in self.vertices)
        min_y = min(point[1] for point in self.vertices)
        max_y = max(point[1] for point in self.vertices)
        # compute the width and height of the surface
        width = max_x - min_x
        height = max_y - min_y

        # created transparent surface
        surface = Surface((width, height), SRCALPHA)
        # CRUCIAL. drawing the polygon on the mask surface
        draw.polygon(surface, (255, 255, 255), [(x - min_x, y - min_y) for x, y in self.vertices])
        
        return surface
    
    def draw(self):
        ...


# FIX OTHERS BOUNDARIES: it doesn't find it
def create_boundaries():
    for index in range(1, 7):
        list_points = create_list_boundaries("Delimitator", index)
        surface = Boundaries(list_points) # check if position and size are correct
        sprite_group_boundaries.add(surface)        
