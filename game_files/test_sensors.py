import pygame
import numpy as np
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, obstacles):
        super().__init__()

        pos = (300, 200)
        size = (16, 16)
        
        self.player_speed = 2

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.old_rect = self.rect.copy()

        self.obstacles = obstacles
        
        self.image.fill("black")

    def collision(self, direction):
        # video of the collision: https://youtu.be/W9uKzPFS1CI?si=IdE6UcPExr6NsMhN

        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.old_rect = self.rect.copy() # previous frame
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.rect.y += self.player_speed
            self.collision('vertical')
        if keys[pygame.K_UP]:
            self.rect.y -= self.player_speed
            self.collision('vertical')
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.player_speed
            self.collision('horizontal')
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.player_speed
            self.collision('horizontal')


class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        super().__init__(group)

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.old_rect = self.rect.copy()

        self.color_obstacles = (82, 82, 82)
        self.image.fill(self.color_obstacles)


class Sensor:
    def __init__(self, pos):
        width = height = 3
        pos = pos
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=pos)

    def draw(self):
        pygame.draw.rect(screen, "red", self.rect)


def lines_data():
    pos_start_x = PLAYER.rect.centerx
    pos_start_y = PLAYER.rect.centery

    section_1_end = 90
    section_2_end = 65
    section_3_end_type1 = 80
    section_3_end_type2 = 35

    width_height_player = 9

    return {
        "right": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_1_end, PLAYER.rect.centery)},
        "left": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_1_end, PLAYER.rect.centery)},
        "up": {"pos_start": (pos_start_x, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery-section_1_end)},
        "down": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx, PLAYER.rect.centery+section_1_end)},

        "diagonal-up-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-up-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery-section_2_end)},
        "diagonal-down-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+section_2_end, PLAYER.rect.centery+section_2_end)},
        "diagonal-down-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-section_2_end, PLAYER.rect.centery+section_2_end)},

        "diagonal-up-up-right": {"pos_start": (pos_start_x+width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx+section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-up-up-left": {"pos_start": (pos_start_x-width_height_player, pos_start_y-width_height_player), "pos_end": (PLAYER.rect.centerx-section_3_end_type2, PLAYER.rect.centery-section_3_end_type1)},
        "diagonal-right-right-up": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-right-right-down": {"pos_start": (pos_start_x+width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx+section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-left-left-up": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery-section_3_end_type2)},
        "diagonal-left-left-down": {"pos_start": (pos_start_x-width_height_player, pos_start_y), "pos_end": (PLAYER.rect.centerx-section_3_end_type1, PLAYER.rect.centery+section_3_end_type2)},
        "diagonal-down-down-right": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx+section_3_end_type2, PLAYER.rect.centery+section_3_end_type1)},
        "diagonal-down-down-left": {"pos_start": (pos_start_x, pos_start_y+width_height_player), "pos_end": (PLAYER.rect.centerx-section_3_end_type2, PLAYER.rect.centery+section_3_end_type1)},
    }

def draw_lines_sensors(lines_data):
    color_line = (220, 220, 220)
    for data in lines_data.values():
        pos_end = data["pos_end"]

        pygame.draw.line(screen, color_line, PLAYER.rect.center, pos_end, 2)
    

def create_obstacles():
    # object at the center
    StaticObstacle(
        500,
        500,
        200,
        100,
        obstacles_sprites
    )
    StaticObstacle(
        600,
        200,
        100,
        100,
        obstacles_sprites
    )
    StaticObstacle(
        200,
        600,
        150,
        300,
        obstacles_sprites
    )

    # boundaries window
    StaticObstacle(
        0,
        0,
        1120,
        30,
        obstacles_sprites
    )
    StaticObstacle(
        0,
        0,
        30,
        1024,
        obstacles_sprites
    )
    StaticObstacle(
        1090,
        0,
        30,
        1024,
        obstacles_sprites
    )
    StaticObstacle(
        0,
        994,
        1120,
        30,
        obstacles_sprites
    )

    StaticObstacle(
        700,
        700,
        16,
        16, 
        obstacles_sprites
    )
    StaticObstacle(
        716,
        700,
        16,
        16, 
        obstacles_sprites
    )
    StaticObstacle(
        732,
        700,
        16,
        16, 
        obstacles_sprites
    )


def create_sensor(pos):
    rect = pygame.Rect(pos[0], pos[1], 3, 3)
    return rect


def draw_distance_texts(distance_sensors):
    start_text_x = 100
    start_text_y = 100
    font = pygame.font.SysFont("silomttf", 12)

    for name in distance_sensors:
        img = font.render(f"{name}: {str(distance_sensors[name])}", True, "black")
        screen.blit(img, (start_text_x, start_text_y))

        start_text_y += 15


pygame.init()
screen = pygame.display.set_mode((1120, 1024))
clock = pygame.time.Clock()
running = True

obstacles_sprites = pygame.sprite.Group()
PLAYER = Player(obstacles_sprites)
create_obstacles()
sensor_sprites = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    # drawing all elements
    obstacles_sprites.draw(screen)


    data = lines_data()
    draw_lines_sensors(data)

    distance_sensors = {name: 100 for name in data}
    for name in data:

        start = data[name]["pos_start"]
        end = data[name]["pos_end"]

        for obstacle in obstacles_sprites:
            collision = obstacle.rect.clipline(start, end)
            

            if collision:
                sensor = Sensor(collision[0])
                sensor.draw()

                distance_sensors[name] = np.linalg.norm(
                    np.array([start[0], start[1]]) - np.array([collision[0][0], collision[0][1]])
                )

    
    draw_distance_texts(distance_sensors)

    screen.blit(PLAYER.image, (PLAYER.rect.x, PLAYER.rect.y))
    PLAYER.update()


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
