import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


class Player(pygame.sprite.Sprite):
    def __init__(self):

        pos = (100, 100)
        size = (20, 20)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)

        self.image.fill("green")

    def update(self):
        keys = pygame.key.get_pressed()
        velocity = 1

        if keys[pygame.K_UP]:
            self.rect.y -= velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += velocity
        if keys[pygame.K_LEFT]:
            self.rect.x -= velocity   

    def sensor(self):
        self.start_pos = (PLAYER.rect.centerx+10, PLAYER.rect.centery)
        self.end_pos = (self.start_pos[0]+200, self.start_pos[1])

        pygame.draw.line(screen, "black", self.start_pos, self.end_pos, width=2)

    def collide_sensor(self, obstacles):
        collisions = {}
        for obstacle in obstacles:
            colliding = obstacle.rect.clipline(self.start_pos, self.end_pos)
            if colliding:
                distance = np.linalg.norm(
                    np.array([*self.start_pos]) - np.array([*colliding[0]])
                )
                collisions[distance] = colliding[0]

        min_distance_key = min(collisions)
        pygame.draw.circle(screen, "red", (collisions[min_distance_key]), radius=3)


obstacle_sprites_group = pygame.sprite.Group()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)


list_obstacle = [
    {"size": (30, 30), "pos": (200, 100), "group": obstacle_sprites_group},
    {"size": (30, 30), "pos": (250, 100), "group": obstacle_sprites_group},
    {"size": (30, 30), "pos": (300, 100), "group": obstacle_sprites_group}
]
for obstacle in list_obstacle:
    Obstacle(
        size=obstacle["size"],
        pos=obstacle["pos"],
        group=obstacle["group"]
    )


PLAYER = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    for sprite in obstacle_sprites_group:
        pygame.draw.rect(screen, "white", sprite.rect)

    PLAYER.sensor()
    PLAYER.collide_sensor(obstacle_sprites_group)
    screen.blit(PLAYER.image, (PLAYER.rect.x, PLAYER.rect.y))
    PLAYER.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()