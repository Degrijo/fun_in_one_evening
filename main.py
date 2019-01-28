import pygame as pg
from random import choice

pg.init()
win_size = 500
pg.display.set_caption("Cube Game")
win = pg.display.set_mode((win_size, win_size))
clock = pg.time.Clock()


class Player:
    def __init__(self, x, y, width, speed, hp, damage, color, ar_of_vis, speed_of_bul=1, rad_of_bul=2):
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

    def move(self):
        if "x" in self.last_move and 0 <= self.x <= win_size - self.width:
            if "-" in self.last_move:
                self.x -= self.speed
            else:
                self.x += self.speed
        elif "y" in self.last_move and 0 <= self.y <= win_size - self.width:
            if "-" in self.last_move:
                self.y -= self.speed
            else:
                self.y += self.speed

    def dodge(self):
        global enemies, free_sides, start_tick
        if pg.time.get_ticks() - start_tick >= 400:
            free_sides = {'+x': 0, '-x': 0, '+y': 0, '-y': 0}  # should call in period of the time
            start_tick = pg.time.get_ticks()
        for enemy in enemies:  # mb need to do addiction from own bullets
            if enemy is not self:
                    for bullet in enemy.bullets:
                        if self.ar_of_vis[0] <= abs(self.y+self.width-bullet.y) <= self.ar_of_vis[1]:
                            if self.y > bullet.y and bullet.direct == '+y':
                                free_sides['-y'] -= 2
                                free_sides['+y'] -= 1
                            elif self.y < bullet.y and bullet.direct == '-y':
                                free_sides['+y'] -= 2
                                free_sides['-y'] -= 1
                        if self.ar_of_vis[0] <= abs(self.x+self.width-bullet.x) <= self.ar_of_vis[1]:
                            if self.x > bullet.x and bullet.direct == '+x':
                                free_sides['-x'] -= 2
                                free_sides['+x'] -= 1
                            elif self.x < bullet.x and bullet.direct == '-x':
                                free_sides['+x'] -= 2
                                free_sides['-x'] -= 1

        if self.x <= 10:
            free_sides['-x'] -= 3
        elif win_size - self.x - self.width <= 10:
            free_sides['+x'] -= 3
        if self.y <= 10:
            free_sides['-y'] -= 3
        elif win_size - self.y - self.width <= 10:
            free_sides['+y'] -= 3
        print(free_sides)
        if list(free_sides.values()) == [0, 0, 0, 0]:
            return
        else:
            if list(free_sides.values()).count(max(free_sides.values())) == 1:
                for key in free_sides.keys():
                    if free_sides[key] == max(free_sides.values()):
                        self.last_move = key
                        break
            else:
                ch = []
                for key in free_sides.keys():
                    if free_sides[key] == max(free_sides.values()):
                       ch.append(key)
                self.last_move = choice(ch)
            free_sides[self.last_move] += 0.1
            self.move()

    def attack(self):
        global enemies
        for enemy in enemies:
            if enemy is not self:
                if abs(self.x - enemy.x) > enemy.width // 2 and abs(self.y - enemy.y) > enemy.width // 2:
                    if abs(self.x - enemy.x) > abs(self.y - enemy.y):
                        if self.y < enemy.y:
                            self.last_move = "+y"
                            self.move()
                        else:
                            self.last_move = "-y"
                            self.move()
                    else:
                        if self.x < enemy.x:
                            self.last_move = "+x"
                            self.move()
                        else:
                            self.last_move = "-x"
                            self.move()
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


enemies = [Player(win_size//2, win_size//5, 10, 0.5, 50, 5, (0, 0, 255), [2, 7]),
           Player(win_size//2, win_size - win_size//5, 10, 0.5, 50, 5, (255, 0, 0), [3, 6])]
start_tick = pg.time.get_ticks()
free_sides = {'+x': 0, '-x': 0, '+y': 0, '-y': 0}

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
    if len(enemies) == 2:
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
