# Create your own shooter
from time import time as time_counter
from pygame import *
from random import randint
font.init()
score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 10:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < 700 - 80:
            self.rect.x += self.speed

    def fire(self, j, i):
        new_boom = Bullet("kaboom.png", self.rect.centerx-7+j, self.rect.top+30, 15, 50, 15-i)
        bullets.add(new_boom)

    def fire_bullet(self, j, i):
        new_bullet = Bullet("bullet.png", self.rect.centerx+j, self.rect.top-i, 15, 50, 15)
        bullets.add(new_bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("rocket.png", 350, 400, 65, 96, 10)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(0, 620), 50, 100, 65, randint(1, 3))
    enemies.add(enemy)

bullets = sprite.Group()

window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"),(700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")
explosion_sound = mixer.Sound("explosion.ogg")

clock = time.Clock()
game = True
finish = False
life = 3
reload = False
num_bullets = 40

while game:
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()

        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()


        score_stat = font.SysFont("Arail", 30).render("Score: " + str(score), 1, (255, 255, 255))
        lost_stat = font.SysFont("Arail", 30).render("Missed: " + str(lost), 1, (255, 255, 255))
        life_stat = font.SysFont("Arail", 30).render("Lives: " + str(life), 1, (255, 255, 255))
        bullet_stat = font.SysFont("Arail", 30).render("Ammo: " + str(num_bullets), 1, (255, 255, 255))
        window.blit(score_stat, (10, 10))
        window.blit(lost_stat, (10, 40))
        window.blit(life_stat, (10, 70))
        window.blit(bullet_stat, (10, 100))


        if not reload:
            collides_en = sprite.spritecollide(player, enemies, True)
            if collides_en:
                life -= 1
                reload = True
                event_time = time_counter()
                new_enemy = Enemy("ufo.png", randint(80, 620), 50, 100, 65, randint(1, 3))
                enemies.add(new_enemy)

        
        if reload:
            reload_text = font.SysFont("Arail", 20).render(
                "STOP",
                1,
                (255, 30, 50)
            )
            window.blit(reload_text, (300, 400))
            new_time = time_counter()
            if new_time - event_time >= 1:
                reload = False


        if lost > 10 or life <= 0:
            finish = True
            lost_text = font.SysFont(None, 60).render("YOU LOSE!", 1, (255, 0, 0))
            window.blit(lost_text, (220, 200))
            mixer.music.stop()
        
        if score >= 100:
            finish = True
            lost_text = font.SysFont(None, 60).render("YOU WIN!", 1, (20, 50, 250))
            window.blit(lost_text, (220, 200))
            mixer.music.stop()
        

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for collide in collides:
            score += 1
            explosion_sound.play()
            new_enemy = Enemy("ufo.png", randint(0, 620), 50, 100, 65, randint(1, 3))
            enemies.add(new_enemy)


    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            # joke, to fix change "!= 4" to "> 3-"
            if (key.get_pressed()[K_r]) and num_bullets >= 3-1 and not finish and not reload:
                player.fire_bullet(j=-37,i=5)
                player.fire(j=0,i=-5)
                player.fire_bullet(j=25,i=5)
                num_bullets -= 3
                fire_sound.play()
            elif e.key == K_SPACE and not finish and not reload:
                player.fire_bullet(j=-6,i=30)
                num_bullets -= 1
                fire_sound.play()
                if num_bullets <= 0:
                    event_time = time_counter()
                    num_bullets += 40
                    reload = True


    clock.tick(60)
    display.update()