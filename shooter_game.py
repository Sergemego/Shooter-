#Создай собственный Шутер!
from pygame import *
from random import randint

lost = 0

class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
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
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
       self.rect.y -= self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

font.init()
font2 = font.Font(None, 36)

text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

player = Player('rocket.png', 5, win_height - 80, 4)
monsters = sprite.Group()
bullets = sprite.Group()
clock = time.Clock()
FPS = 120
run = True
finish = False

score = 0


for i in range(1, 6):
   monster = Enemy('ufo.png', -40, 80, 1)
   monsters.add(monster)



while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               #fire.ogg.play()
               player.fire()

   if not finish:    
       window.blit(background,(0, 0))         
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 20))   
       text_score = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
       window.blit(text_score, (10, 50))       


       player.update()
       monsters.update()
       bullets.update()



       player.reset()
       monsters.draw(window)
       bullets.draw(window)



       collides = sprite.groupcollide(
           monsters, bullets, True, True
       )  
       for c in collides:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 1)
           monsters.add(monster)
           


 
       display.update()

clock.tick(FPS)