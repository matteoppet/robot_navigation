import pygame
from settings import *
from player import Player
from world import World

pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()


PLAYER = Player()

WORLD = World()
WORLD.create_tiles() 
WORLD.create_objects()
sprite_group = WORLD.sprite_group # get the sprite gruop variables


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprite_group.draw(screen) # draw the tiles on the screen

    PLAYER.move()
    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)