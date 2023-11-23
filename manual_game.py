import pygame

pygame.init()
screen = pygame.display.set_mode((950, 950))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)