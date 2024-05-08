from random import randint
from pygame import *
from time import time as timer
 
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
 
#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
 
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
 
       #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            global lost
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y < 0:
            self.kill()
 
# После класса Enemy
lost = 0
 
monsters = sprite.Group()
for i in range(5):
    monsters.add(
        Enemy(
            'ufo.png', 
            randint(80, 620), 
            -50, 
            80, 
            50, 
            randint(1,8
                    )
        )
    )
#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
score = 0
goal = 10
max_lost = 5

#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
bullets = sprite.Group()

life = 3


num_fire = 0
rel_time = False
#создание группы спрайтов-астероидов ()
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False

#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                     
                if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезаря

            if e.key == K_ESCAPE:  # restart with 'R' button
                run = False
    

    if not finish:
       #обновляем фон
        window.blit(background,(0,0))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
         
       #производим движения спрайтов
        ship.update()
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        bullets.update()
 
       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(
                'ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5)
            )
            monsters.add(monster)

        if rel_time == True:
            now_time = timer() #считываем время
       
            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки

            #если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

       #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10)) 

        text = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window. blit(text, (10, 20))

        text_lose = font2.render('Lost: ' + str(lost), 1, (255, 255, 255))
        window. blit(text_lose, (10, 50))

 
        display.update()
   #цикл срабатывает каждые 0.05 секунд
    time.delay(50)
