import pygame
from player import Player
from world import World
from boundaries import create_boundaries, sprite_group_boundaries

pygame.init()
screen = pygame.display.set_mode((1120, 992))
clock = pygame.time.Clock()


WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group
sprite_group_objects = WORLD.sprite_group_objects
PLAYER = Player()

create_boundaries()
sprite_group_bound = sprite_group_boundaries

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprite_group.draw(screen)

    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
    PLAYER.move()
    

    for sprite in sprite_group_boundaries:
        pygame.draw.polygon(screen, "white", sprite.points)



    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)



# CONTINUE WITH ALL THE TUNNELS