import pygame
import os
from random import randint
pygame.init()

def file_path(fail_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, fail_name)
    return path

FPS = 40
WIN_WIDTH = 900
WIN_HEIGHT = 500
WHITE = (255,255,255)
RED = (210,0,0)
GREEN = (0, 210,0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.music.load(file_path("music.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound(file_path("win.wav"))
music_lose = pygame.mixer.Sound(file_path("lose.wav"))
music_shoot = pygame.mixer.Sound(file_path("fair.wav"))
music_bum = pygame.mixer.Sound(file_path("bum.wav"))
music_pass = pygame.mixer.Sound(file_path("pass.wav"))


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
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(file_path("pngwing.com.png"), self.rect.centerx, self.rect.top, 10, 10, 6)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()

class Enemy(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        global missed_enemis
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIN_WIDTH - self.rect.width)
            self.speed = randint(1,4)
            missed_enemis += 1

player = Player("rocket.png",425, 400, 70, 70, 10)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


for i in range(8):
    enemy = Enemy(file_path("aliens.png"),randint(0, WIN_WIDTH - 90),0, 90, 90, randint(1,4))
    enemies.add(enemy)

missed_enemis = 0
killed_enemis = 0
font = pygame.font.SysFont("areal", 25)
font2 = pygame.font.SysFont("areal", 50)
txt_missed = font.render("Пропущенно: "+ str(missed_enemis),True, WHITE)
txt_killed = font.render("Вбито: "+ str(killed_enemis),True, WHITE)

play = True
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                music_shoot.play()
                player.fire()

    if play == True:
        window.blit(background, (0,0))
        
        txt_missed = font.render("Пропущенно: "+ str(missed_enemis),True, WHITE)
        txt_killed = font.render("Вбито: "+ str(killed_enemis),True, WHITE)

        window.blit(txt_missed,(5,5))
        window.blit(txt_killed,(5,32))

        player.reset()
        player.update()

        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()

        collide_bullets = pygame.sprite.groupcollide( enemies, bullets, False, True)
        if collide_bullets:
            for enemy in collide_bullets:
                music_bum.play()
                killed_enemis += 1
                enemy.rect.bottom = 0
                enemy.rect.x = randint(0, WIN_WIDTH - enemy.rect.width)
                enemy.speed = randint(1,4)
            
        if missed_enemis >= 1 or pygame.sprite.spritecollide(player, enemies, False):
            pygame.mixer.music.stop()
            music_lose.play()
            play = False
            txt_lose = font2.render("YOU LOSE", True, RED)
            window.blit(txt_lose, (360, 250))
            pygame.mixer.music.stop()


        if killed_enemis == 3:
            pygame.mixer.music.stop()
            music_win.play()
            play = False
            txt_win = font2.render("YOU WIN", True, GREEN)
            window.blit(txt_win,(360, 250))


    clock.tick(FPS)
    pygame.display.update()