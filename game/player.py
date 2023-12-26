import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # position player
        self.x = 100
        self.y = 100

        # width and height player
        self.width = 32
        self.height = 32

        self.image = pygame.image.load("../assets/images/player/player_front.png") # default image
        self.rect = pygame.Rect(100, 100, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.image = pygame.image.load("../assets/images/player/player_front.png")
            self.y += 2
            self.rect.y += 2
        if keys[pygame.K_UP]:
            self.image = pygame.image.load("../assets/images/player/player_back.png")
            self.y -= 2
            self.rect.y -= 2
        if keys[pygame.K_RIGHT]:
            self.image = pygame.image.load("../assets/images/player/player_right.png")
            self.x += 2
            self.rect.x += 2
        if keys[pygame.K_LEFT]:
            self.image = pygame.image.load("../assets/images/player/player_left.png")
            self.x -= 2
            self.rect.x -= 2

    def ai_move(self, action):
        if action == 0:
            self.image = pygame.image.load("../assets/images/player/player_back.png")
            self.y -= 2
            self.rect.y -= 2
        elif action == 1:
            self.image = pygame.image.load("../assets/images/player/player_front.png")
            self.y += 2
            self.rect.y += 2
        elif action == 2:
            self.image = pygame.image.load("../assets/images/player/player_right.png")
            self.x += 2
            self.rect.x += 2
        elif action == 3:
            self.image = pygame.image.load("../assets/images/player/player_left.png")
            self.x -= 2
            self.rect.x -= 2

    def reset(self):
        self.x = self.y = 100
        self.rect.x = self.rect.y = 100

        return self.x, self.y