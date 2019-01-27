import pygame as pg
from random import choice

pg.init()
win_size = 500
pg.display.set_caption("Cube Game")
win = pg.display.set_mode((win_size, win_size))
clock = pg.time.Clock()


class Player:
    def __init__(self, x, y, width, speed, hp, damage, color, ar_of_vis, speed_of_bul=1, rad_of_bul = 2):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.hp = hp
        self.damage = damage
        self.bullets = []
        self.kd = [pg.time.get_ticks() for _ in range(2)]
        self.last_move = "-y"
        self.color = color
        self.ar_of_vis = ar_of_vis
        self.speed_of_bul = speed_of_bul
        self.rad_of_bul = rad_of_bul

    def draw(self):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def attack_q(self):
        if pg.time.get_ticks() - self.kd[0] >= 1000:
            self.bullets.append(Bullet(round(self.x + self.width // 2), round(self.y + self.width // 2), self.speed_of_bul, self.rad_of_bul, self.last_move))
            self.kd[0] = pg.time.get_ticks()

    def attack_w(self):
        if pg.time.get_ticks() - self.kd[1] >= 1000:
            if "x" in self.last_move:
                if "-" in self.last_move:
                    self.x -= 30
                else:
                    self.x += 30
            else:
                if "-" in self.last_move:
                    self.y -= 30
                else:
                    self.y += 30
            self.kd[1] = pg.time.get_ticks()

    def is_dead(self):
        global enemies, run
        if self.hp <= 0:
            enemies.pop(enemies.index(self))

    def dodge(self):
        global enemies
        free_sides = ['+x', '-x', '+y', '-y']  # mechanic of dodge
        for enemy in enemies:
            if enemy is not self:
                if enemy.bullets is not []:
                    for bullet in enemy.bullets:
                        if self.ar_of_vis[0] <= abs(self.y+self.width-bullet.y) <= self.ar_of_vis[1]:
                            print("ok1-ok1")
                            if self.y > bullet.y and bullet.direct == '+y':
                                print("ok1-ok1-ok1")
                                free_sides.pop(free_sides.index('-y'))
                            elif self.y < bullet.y and bullet.direct == '-y':
                                print("ok1-ok1-ok1")
                                free_sides.pop(free_sides.index('+y'))
                        if self.ar_of_vis[0] <= abs(self.x+self.width-bullet.x) <= self.ar_of_vis[1]:
                            print("ok2-ok2")
                            if self.x > bullet.x and bullet.direct == '+x':
                                print("ok2-ok2-ok2")
                                free_sides.pop(free_sides.index('-x'))
                            elif self.x < bullet.x and bullet.direct == '-x':
                                print("ok2-ok2-ok2")
                                free_sides.pop(free_sides.index('+x'))
                else:
                    self.attack()

        print(free_sides)
        if len(free_sides) is 0:
            pass
        elif len(free_sides) is 4:
            self.attack()
        else:
            side = choice(free_sides)
            tick = pg.time.get_ticks()
            if 'x' in side:
                if '+' in side:
                        self.x += self.speed
                else:
                        self.x -= self.speed
            else:
                if '+' in side:
                        self.y += self.speed
                else:
                        self.y -= self.speed

    def attack(self):
        global enemies
        for enemy in enemies:
            if enemy is not self:
                if abs(self.x - enemy.x) > enemy.width // 2 and abs(self.y - enemy.y) > enemy.width // 2:
                    if abs(self.x - enemy.x) > abs(self.y - enemy.y):
                        if self.y < enemy.y:
                            self.y += self.speed
                            self.last_move = "+y"
                        else:
                            self.y -= self.speed
                            self.last_move = "-y"
                    else:
                        if self.x < enemy.x:
                            self.x += self.speed
                            self.last_move = "+x"
                        else:
                            self.x -= self.speed
                            self.last_move = "-x"
                else:
                    if abs(self.x - enemy.x) <= enemy.width // 2:
                        if self.y > enemy.y:
                            self.last_move = "-y"
                        else:
                            self.last_move = "+y"
                    elif abs(self.y - enemy.y) <= enemy.width // 2:
                        if self.x > enemy.x:
                            self.last_move = "-x"
                        else:
                            self.last_move = "+x"

                    self.attack_q()

    def walk(self):
        pass


class Bullet:
    def __init__(self, x, y, speed, rad, direct):
        self.x = x
        self.y = y
        self.speed = speed
        self.rad = rad
        self.direct = direct

    def draw(self):
        pg.draw.circle(win, (0, 255, 0), (self.x, self.y), self.rad)


enemies = [Player(win_size//2, win_size//5, 10, 0.5, 50, 5, (0, 0, 255), [2, 20]),
           Player(win_size//2, win_size - win_size//5, 10, 0.5, 50, 5, (255, 0, 0), [2, 5])]
run = True
while run:
    clock.tick(300)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    for enemy in enemies:
        for bullet in enemy.bullets:
            if 0 <= bullet.x <= win_size - bullet.rad*2 and 0 <= bullet.y <= win_size - bullet.rad*2:
                for hero in enemies:
                    if enemy is not hero:
                        if abs(hero.x - bullet.x) < hero.width and abs(hero.y - bullet.y) < hero.width:
                            hero.hp -= enemy.damage
                            enemy.bullets.pop(enemy.bullets.index(bullet))
                            hero.is_dead()
                if bullet is not None:
                    if 'x' in bullet.direct:
                        if '+' in bullet.direct:
                            bullet.x += bullet.speed
                        else:
                            bullet.x -= bullet.speed
                    else:
                        if '+' in bullet.direct:
                            bullet.y += bullet.speed
                        else:
                            bullet.y -= bullet.speed
            else:
                enemy.bullets.pop(enemy.bullets.index(bullet))
    if len(enemies) is 2:
        enemies[0].dodge()
        enemies[1].attack()
    else:
        enemies[0].attack()
    print(enemies[0].hp)
    win.fill((255, 255, 255))
    for enemy in enemies:
        enemy.draw()
        for bul in enemy.bullets:
            bul.draw()
    pg.display.update()


pg.quit()
