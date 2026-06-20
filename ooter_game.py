from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("pygame window")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
font.init()
font_2 = font.Font(None,36)

BIG_font = font.Font(None, 80)
win = BIG_font.render('YOU WIN!',True, (255,0,0))
lose = BIG_font.render('YOU LOSE!', True,(255,0,0))
# mixer.music.load('space.ogg')
# mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

image_hero = 'rocket.png'
image_enemy = 'ufo.png'
image_bullet = 'bullet.png'
image_asteroid = 'asteroid.png'

life = 3
points = 0
lost = 0
MAX_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width -80)
            self.rect.y = 0 
            lost += 1

class Asteroid(GameSprite):
   def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width -80)
            self.rect.y = 0 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            

ship = Player(image_hero, 5, win_height -100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    ufo = Enemy(image_enemy,randint(80,win_width -80), -40, 80, 50,randint(1,5)  )
    monsters.add(ufo)

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Asteroid(image_asteroid,randint(30,win_width -30), -40, 80, 50,randint(1,7)  )
    asteroids.add(asteroid)

bullets = sprite.Group()

game = True
finish = False
rel_time = False
num_fire = 0 
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire > 5 and rel_rime == False:
                    last_time = timer()
                    rel_time = True

    
    if not finish:
        window.blit(background,(0, 0))
        text = font_2.render('Счет: '+ str(points),1,(255,255,255))
        window.blit(text,(10,20))
        text_2 = font_2.render('Пропущено: '+ str(lost),1,(255,255,255))
        window.blit(text_2,(10,50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()
        asteroids.draw(window)
        bullets.draw(window)
        monsters.draw(window)

        #перезарядкО
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload  = font_2.render('жди, перезарядкО...',1, (155,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True) 
        
        for i in collides:
            points += 1 
            ufo = Enemy(image_enemy,randint(80,win_width -80), -40, 80, 50,randint(1,5)  )
            monsters.add(ufo)


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship,asteroids, False):
            sprite.spritecollide(ship,monsters, True)
            sprite.spritecollide(ship,asteroids, True)
            life -= 1

        if life == 0 or lost >= 3:
            finish = True
            window.blit(lose,(200,200))
            

        if points >= 10:
            finish = True
            window.blit(win,(200,200))

            # text_lose = BIG_font.render('Пропущенно:'+str(lost),1,(255,255,255))
            # window.blit(text_lose,(10,50))
        
    display.update()
    time.delay(50)