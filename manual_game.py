import pygame

pygame.init()
screen = pygame.display.set_mode((950, 950))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # position player
        self.x = 100
        self.y = 100

        # width and height player
        self.width = 20
        self.height = 20

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y += 2
        if keys[pygame.K_DOWN]:
            self.y -= 2
        if keys[pygame.K_LEFT]:
            self.x += 2
        if keys[pygame.K_RIGHT]:
            self.x -= 2


PLAYER = Player()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    PLAYER.move()
    screen.blit(PLAYER.image, (PLAYER.x, PLAYER.y))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)