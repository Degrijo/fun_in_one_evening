import pygame as pg
from random import choice

pg.init()
win_size = 500
pg.display.set_caption("Cube Game")
win = pg.display.set_mode((win_size+200, win_size))
clock = pg.time.Clock()


class Player:
    free_sides = {'+x': 0, '-x': 0, '+y': 0, '-y': 0, 'is_dang': False}

    def __init__(self, x, y, width, speed, hp, damage, color, ar_of_vis, speed_of_bul=1, rad_of_bul=2):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.hp = hp
        self.damage = damage
        self.bullets = []
        self.kd = [pg.time.get_ticks() for _ in range(4)]  # 0 - target, 1 - dodge, 2 - q, 3 - w
        self.last_move = "-y"
        self.color = color
        self.ar_of_vis = ar_of_vis
        self.speed_of_bul = speed_of_bul
        self.rad_of_bul = rad_of_bul

    def draw(self):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def attack_q(self):
        if pg.time.get_ticks() - self.kd[2] >= 1000:
            self.bullets.append(Bullet(round(self.x + self.width // 2 - self.rad_of_bul), round(self.y + self.width // 2 -
                                       self.rad_of_bul), self.speed_of_bul, self.rad_of_bul, self.last_move))
            self.kd[2] = pg.time.get_ticks()

    def attack_w(self):
        if pg.time.get_ticks() - self.kd[3] >= 1000:
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
            self.kd[3] = pg.time.get_ticks()

    def is_dead(self):
        global enemies
        if self.hp <= 0:
            enemies.pop(enemies.index(self))

    def move(self):
        global enemies
        cant_move = []
        for enemy in enemies:
            if self.last_move == '+x' and enemy.x - self.x == self.width and (-1)*enemy.width < enemy.y - self.y < self.width and '+x' not in cant_move:
                cant_move.append('+x')
                self.free_sides['+x'] -= 1
            elif self.last_move == '-x' and self.x - enemy.x == enemy.width and (-1)*enemy.width < enemy.y - self.y < self.width and '-x' not in cant_move:
                cant_move.append('-x')
                self.free_sides['-x'] -= 1
            elif self.last_move == '+y' and enemy.y - self.y == self.width and (-1)*enemy.width < enemy.x - self.x < self.width and '+y' not in cant_move:
                cant_move.append('+y')
                self.free_sides['+y'] -= 1
            elif self.last_move == '-y' and self.y - enemy.y == enemy.width and (-1)*enemy.width < enemy.x - self.x < self.width and '-y' not in cant_move:
                cant_move.append('-y')
                self.free_sides['-y'] -= 1
        if self.last_move not in cant_move and 0 <= self.x <= win_size - self.width and 0 <= self.y <= win_size - self.width: # self.last_move not in cant_move and
            if self.last_move == '-x':
                self.x -= self.speed
            elif self.last_move == '+x':
                self.x += self.speed
            elif self.last_move == '-y':
                self.y -= self.speed
            elif self.last_move == '+y':
                self.y += self.speed

    def dodge(self):
        global enemies
        if pg.time.get_ticks() - self.kd[1] >= 200:
            self.free_sides = {'+x': 0, '-x': 0, '+y': 0, '-y': 0, 'is_dang': False}
            self.kd[1] = pg.time.get_ticks()
        for enemy in enemies:
            if enemy is not self:
                    for bullet in enemy.bullets:
                        if self.x - self.ar_of_vis <= bullet.x and bullet.x + bullet.rad*2 <= self.x + self.width + \
                            self.ar_of_vis and self.y - self.ar_of_vis <= bullet.y and bullet.y + bullet.rad*2 <=\
                                self.y + self.width + self.ar_of_vis:
                            poz = []
                            if bullet.x + bullet.rad*2 <= self.x:
                                poz = [1, 2, 3]
                            elif bullet.x >= self.x + self.width:
                                poz = [6, 7, 8]
                            elif self.x - bullet.rad*2 < bullet.x < self.x + self.width:
                                poz = [4, 5]
                            if bullet.y + bullet.rad*2 <= self.y:
                                poz = [i for i in [1, 4, 6] if i in poz]
                            elif bullet.y >= self.y + self.width:
                                poz = [i for i in [3, 5, 8] if i in poz]
                            elif self.y - bullet.rad*2 < bullet.y < self.y + self.width:
                                poz = [i for i in [2, 7] if i in poz]

                            if len(poz) is 1:
                                if bullet.direct == '+x':
                                    if poz[0] == 2:
                                        self.free_sides['is_dang'] = True
                                        self.free_sides['-x'] -= 2
                                        self.free_sides['+x'] -= 1
                                    elif poz[0] in [1, 4, 6]:
                                        self.free_sides['-y'] -= 2
                                    elif poz[0] in [3, 5, 8]:
                                        self.free_sides['+y'] -= 2
                                elif bullet.direct == '-x':
                                    if poz[0] == 7:
                                        self.free_sides['is_dang'] = True
                                        self.free_sides['+x'] -= 2
                                        self.free_sides['-x'] -= 1
                                    elif poz[0] in [1, 4, 6]:
                                        self.free_sides['-y'] -= 2
                                    elif poz[0] in [3, 5, 8]:
                                        self.free_sides['+y'] -= 2
                                elif bullet.direct == '+y':
                                    if poz[0] == 4:
                                        self.free_sides['is_dang'] = True
                                        self.free_sides['-y'] -= 2
                                        self.free_sides['+y'] -= 1
                                    elif poz[0] in [1, 2, 3]:
                                        self.free_sides['-x'] -= 2
                                    elif poz[0] in [6, 7, 8]:
                                        self.free_sides['+x'] -= 2
                                elif bullet.direct == '-y':
                                    if poz[0] == 5:
                                        self.free_sides['is_dang'] = True
                                        self.free_sides['+y'] -= 2
                                        self.free_sides['-y'] -= 1
                                    elif poz[0] in [1, 2, 3]:
                                        self.free_sides['-x'] -= 2
                                    elif poz[0] in [6, 7, 8]:
                                        self.free_sides['+x'] -= 2

        if self.x <= 10:
            self.free_sides['-x'] -= 1
        elif win_size - self.x - self.width <= 10:
            self.free_sides['+x'] -= 1
        if self.y <= 10:
            self.free_sides['-y'] -= 1
        elif win_size - self.y - self.width <= 10:
            self.free_sides['+y'] -= 1
        if self.free_sides['is_dang'] is False:
            self.attack(self.target)
        else:
            max_val = max(self.free_sides['+x'], self.free_sides['-x'], self.free_sides['+y'], self.free_sides['-y'])
            if [self.free_sides['+x'], self.free_sides['-x'], self.free_sides['+y'], self.free_sides['-y']].count(max_val) == 1:
                for key in ['+x', '-x', '+y', '-y']:
                    if self.free_sides[key] == max_val:
                        self.last_move = key
                        break
            else:
                ch = []
                for key in ['+x', '-x', '+y', '-y']:
                    if self.free_sides[key] == max_val:
                        ch.append(key)
                self.last_move = choice(ch)
                self.free_sides[self.last_move] += 2
            self.move()

    def attack(self, enemy):
        global enemies
        if self.x + self.width - 1 > round(enemy.x + enemy.width//2 - enemy.rad_of_bul) > self.x + 1 or \
            self.y + self.width - 1 > round(enemy.y + enemy.width//2 - enemy.rad_of_bul) > self.y + 1:
            if self.x + self.width - 1 > round(enemy.x + enemy.width//2 - enemy.rad_of_bul) > self.x + 1:
                if self.y > enemy.y:
                    self.last_move = "-y"
                else:
                    self.last_move = "+y"
            elif self.y + self.width - 1 > round(enemy.y + enemy.width//2 - enemy.rad_of_bul) > self.y + 1:
                if self.x > enemy.x:
                    self.last_move = "-x"
                else:
                    self.last_move = "+x"

            self.attack_q()
        else:
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

    def walk(self):
        pass

    def get_target(self):
        global enemies
        best_ch = []
        for enemy in enemies:
            if enemy is not self:
                if best_ch is []:
                    if ((enemy.x-self.x)**2+(enemy.y-self.y)**2)**1/2 < ((best_ch[0].x-self.x)**2+(best_ch[0].y-self.y)**2)**1/2:
                        best_ch.clear()
                        best_ch.append(enemy)
                    elif ((enemy.x-self.x)**2+(enemy.y-self.y)**2)**1/2 == ((best_ch[0].x-self.x)**2+(best_ch[0].y-self.y)**2)**1/2:
                        best_ch.append(enemy)
                else:
                    best_ch.append(enemy)
        return choice(best_ch)


class Bullet:
    def __init__(self, x, y, speed, rad, direct):
        self.x = x
        self.y = y
        self.speed = speed
        self.rad = rad
        self.direct = direct

    def draw(self):
        pg.draw.circle(win, (0, 255, 0), (self.x, self.y), self.rad)

    def move(self):
        if self.direct == '+x':
            self.x += self.speed
        elif self.direct == '-x':
            self.x -= self.speed
        elif self.direct == '+y':
            self.y += self.speed
        elif self.direct == '-y':
            self.y -= self.speed


def control_bullets(enemies):
    for enemy in enemies:
        if enemy.target not in enemies:  # pg.time.get_ticks() - enemy.kd[0] >= 10000 or
            enemy.target = enemy.get_target()
            enemy.kd[0] = pg.time.get_ticks()
        for bullet in enemy.bullets:
            if 0 <= bullet.x <= win_size - bullet.rad * 2 and 0 <= bullet.y <= win_size - bullet.rad * 2:
                for hero in enemies:
                    if enemy is not hero:
                        if (0 < hero.x - bullet.x < bullet.rad * 2 or hero.x <= bullet.x < hero.x + hero.width) and \
                                (0 < hero.y - bullet.y < bullet.rad * 2 or hero.y <= bullet.y < hero.y + hero.width):
                            hero.hp -= enemy.damage
                            if bullet in enemy.bullets:
                                enemy.bullets.pop(enemy.bullets.index(bullet))
                            hero.is_dead()
                if bullet is not None:
                    bullet.move()
            else:
                enemy.bullets.pop(enemy.bullets.index(bullet))


def text_disp(text, x, y):
    myfont = pg.font.SysFont('Comic Sans MS', 15)
    textsurface = myfont.render(text, False, (0, 0, 0))
    win.blit(textsurface, (x, y))


enemies = [Player(0, 0, 10, 0.5, 50, 5, (255, 0, 0), 20),
           Player(win_size // 2 - 5, 0, 10, 0.5, 50, 5, (255, 146, 0), 20),
           Player(win_size - 10, 0, 10, 0.5, 50, 5, (255, 211, 0), 20),
           Player(0, win_size // 2 - 5, 10, 0.5, 50, 5, (204, 246, 0), 20),
           Player(win_size - 10, win_size // 2 - 5, 10, 0.5, 50, 5, (0, 204, 0), 20),
           Player(0, win_size - 10, 10, 0.5, 50, 5, (11, 97, 164), 20),
           Player(win_size // 2 - 5, win_size - 10, 10, 0.5, 50, 5, (57, 20, 175), 20),
           Player(win_size - 10, win_size - 10, 10, 0.5, 50, 5, (165, 0, 165), 20)]

for enemy in enemies:
    enemy.target = enemy.get_target()

run = True
paused = False
speed_var = 12
while run:
    clock.tick(25*speed_var)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
              paused = not paused
            elif event.key == pg.K_w:
                if speed_var < 30:
                    speed_var += 1
            elif event.key == pg.K_e:
                if speed_var > 1:
                    speed_var -= 1
    if not paused:
        control_bullets(enemies)
        if len(enemies) <= 1:
            if len(enemies) == 1:
                enemies[0].bullets.clear()
            paused = True
        else:
            for enemy in enemies:
                enemy.dodge()
    win.fill((52, 40, 65))
    pg.draw.rect(win, (255, 255, 255), (win_size, 0, 200, win_size))
    y = 50
    for enemy in enemies:
        text_disp("hp:"+str(enemy.hp)+" target", win_size+30, y)
        pg.draw.rect(win, enemy.color, (win_size + 10, y, enemy.width, enemy.width))
        pg.draw.rect(win, enemy.target.color, (win_size + 125, y, enemy.target.width, enemy.target.width))
        y += 50
        enemy.draw()
        for bul in enemy.bullets:
            bul.draw()
    pg.display.update()


pg.quit()
