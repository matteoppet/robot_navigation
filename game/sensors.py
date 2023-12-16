from pygame import sprite, Rect, Surface, SRCALPHA, mask, draw

sprite_group_sensors = sprite.Group()

class Sensors(sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y, direction, length_sensor):
        super().__init__()

        self.name = direction
        self.length_sensor = length_sensor

        if direction == "right":
            self.rect = Rect(player_pos_x, player_pos_y, length_sensor, 5)
        elif direction == "left":
            self.rect = Rect(player_pos_x-self.length_sensor, player_pos_y, self.length_sensor, 5)
        elif direction == "up":
            self.rect = Rect(player_pos_x, player_pos_y-self.length_sensor, 5, self.length_sensor)
        elif direction == "down":
            self.rect = Rect(player_pos_x, player_pos_y, 5, self.length_sensor)
        else:
            raise Exception("No Rect class created in Sensors class, Fault: direction")

        self.image = Surface((self.rect.width, self.rect.height), SRCALPHA)
        self.mask = mask.from_surface(self.image)
        self.image.fill("white")


def create_sensors(player_pos_x, player_pos_y, length_sensor):
    for index in ["right", "left", "up", "down"]:
        surface = Sensors(player_pos_x, player_pos_y, index, length_sensor)
        sprite_group_sensors.add(surface)
        

def draw_lines(screen, rect_x, rect_y, rect_width, rect_height, color=(255, 255, 255)):
    draw.rect(
        screen, 
        color, 
        (rect_x, rect_y, rect_width, rect_height),
    )
