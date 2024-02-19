import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # position player
        self.x = 975
        self.y = 150

        # width and height player
        self.width = 20
        self.height = 20

        self.image = self._return_image(side="left") # default image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.image = self._return_image(side="front")
            self.y += 2
            self.rect.y += 2
        if keys[pygame.K_UP]:
            self.image = self._return_image(side="back")
            self.y -= 2
            self.rect.y -= 2
        if keys[pygame.K_RIGHT]:
            self.image = self._return_image(side="right")
            self.x += 2
            self.rect.x += 2
        if keys[pygame.K_LEFT]:
            self.image = self._return_image(side="left")
            self.x -= 2
            self.rect.x -= 2

    def ai_move(self, action):
        if action == 0:
            self.image = self._return_image(side="back")
            self.y -= 2
            self.rect.y -= 2
        elif action == 1:
            self.image = self._return_image(side="front")
            self.y += 2
            self.rect.y += 2
        elif action == 2:
            self.image = self._return_image(side="right")
            self.x += 2
            self.rect.x += 2
        elif action == 3:
            self.image = self._return_image(side="left")
            self.x -= 2
            self.rect.x -= 2

    def _return_image(self, side=""):
        if side == "left": return pygame.image.load("../../assets/images/player/player_left.png")
        elif side == "right": return pygame.image.load("../../assets/images/player/player_right.png")
        elif side == "front": return pygame.image.load("../../assets/images/player/player_front.png")
        elif side == "back": return pygame.image.load("../../assets/images/player/player_back.png")