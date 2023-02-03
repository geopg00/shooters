import pygame
import os
pygame.init()

def file_path(fail_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, fail_name)
    return path

FPS = 40
WIN_WIDTH = 900
WIN_HEIGHT = 500

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load(file_path("sky.jpg"))
background = pygame.transform.scale(background,(WIN_WIDTH,WIN_HEIGHT))

class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def fire(self):
        pass

player = Player("rocket.png",425, 400, 70, 70, 5)

play = True
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    if play == True:
        window.blit(background, (0,0))

        player.reset()
        player.update()

    clock.tick(FPS)
    pygame.display.update()