from pygame import sprite, Rect, Surface, SRCALPHA, mask, draw

sprite_group_sensors = sprite.Group()

class Sensors(sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y, direction):
        super().__init__()

        self.name = direction

        if direction == "right":
            self.rect = Rect(player_pos_x, player_pos_y, 100, 5)
        elif direction == "left":
            self.rect = Rect(player_pos_x-100, player_pos_y, 100, 5)
        elif direction == "up":
            self.rect = Rect(player_pos_x, player_pos_y-100, 5, 100)
        elif direction == "down":
            self.rect = Rect(player_pos_x, player_pos_y, 5, 100)
        else:
            raise Exception("No Rect class created in Sensors class, Fault: direction")

        self.image = Surface((self.rect.width, self.rect.height), SRCALPHA)
        self.mask = mask.from_surface(self.image)


def create_sensors(player_pos_x, player_pos_y):
    for index in ["right", "left", "up", "down"]:
        surface = Sensors(player_pos_x, player_pos_y, index)
        sprite_group_sensors.add(surface)
        

def draw_lines(screen, rect_x, rect_y, rect_width, rect_height, color="white"):
    draw.rect(
        screen, 
        color, 
        (rect_x, rect_y, rect_width, rect_height)
    )
