import pygame as pg

pg.init()
win_size = 500
pg.display.set_caption("Cube Game")
win = pg.display.set_mode((win_size, win_size))
clock = pg.time.Clock()


class Player:
    def __init__(self, x, y, width, speed, hp, damage, color):
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

    def draw(self):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def attack_q(self):
        if pg.time.get_ticks() - self.kd[0] >= 500:
            self.bullets.append(Bullet(round(self.x + self.width // 2), round(self.y + self.width // 2), 1, 2, self.last_move))
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

    def control_bullets(self):
        for bul in self.bullets:
            bul.control(self)

    def is_dead(self):
        global me, enemies, run
        if self.hp <= 0:
            if self is me:
                run = False
            else:
                enemies.pop(enemies.index(self))


class Bullet:
    def __init__(self, x, y, speed, rad, direct):
        self.x = x
        self.y = y
        self.speed = speed
        self.rad = rad
        self.direct = direct

    def draw(self):
        pg.draw.circle(win, (0, 255, 0), (self.x, self.y), self.rad)

    def control(self, obj):
        if self.x >= win_size or self.x + self.rad * 2 <= 0 or self.y >= win_size or self.y + self.rad * 2 <= 0:
            obj.bullets.pop(obj.bullets.index(self))
            return
        else:
            if "x" in self.direct:
                if "-" in self.direct:
                    self.x -= self.speed
                else:
                    self.x += self.speed
            else:
                if "-" in self.direct:
                    self.y -= self.speed
                else:
                    self.y += self.speed
            global me, enemies
            if obj is me:
                for enemy in enemies:
                    if enemy.x <= self.x <= enemy.x + enemy.width and enemy.y <= self.y <= enemy.y + enemy.width:
                        obj.bullets.pop(obj.bullets.index(self))
                        enemy.hp -= obj.damage
                        enemy.is_dead()
                        return
            else:
                if me.x <= self.x <= me.x + me.width and me.y <= self.y <= me.y + me.width:
                    obj.bullets.pop(obj.bullets.index(self))
                    me.hp -= obj.damage
                    me.is_dead()
                    return


def bot():
    global enemies, me
    for enemy in enemies:
        if abs(enemy.x - me.x) > me.width//2 and abs(enemy.y - me.y) > me.width//2:
            if abs(enemy.x - me.x) > abs(enemy.y - me.y):
                if enemy.y < me.y:
                    enemy.y += enemy.speed
                    enemy.last_move = "+y"
                else:
                    enemy.y -= enemy.speed
                    enemy.last_move = "-y"
            else:
                if enemy.x < me.x:
                    enemy.x += enemy.speed
                    enemy.last_move = "+x"
                else:
                    enemy.x -= enemy.speed
                    enemy.last_move = "-x"
        else:
            if abs(enemy.x - me.x) <= me.width // 2:
                if enemy.y > me.y:
                    enemy.last_move = "-y"
                else:
                    enemy.last_move = "+y"
            elif abs(enemy.y - me.y) <= me.width // 2:
                if enemy.x > me.x:
                    enemy.last_move = "-x"
                else:
                    enemy.last_move = "+x"

            enemy.attack_q()


me = Player(win_size//2, win_size - win_size//5, 10, 0.5, 50, 5, (255, 0, 0))
enemies = [Player(win_size//2, win_size//5, 10, 0.5, 50, 5, (0, 0, 255))]
run = True
while run:
    clock.tick(300)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    me.control_bullets()
    for enemy in enemies:
        enemy.control_bullets()
    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT] and me.x < win_size - me.width:
        me.x += me.speed
        me.last_move = "+x"
    elif keys[pg.K_LEFT] and me.x > 0:
        me.x -= me.speed
        me.last_move = "-x"
    elif keys[pg.K_DOWN] and me.y < win_size - me.width:
        me.y += me.speed
        me.last_move = "+y"
    elif keys[pg.K_UP] and me.y > 0:
        me.y -= me.speed
        me.last_move = "-y"

    if keys[pg.K_q]:
        me.attack_q()
    elif keys[pg.K_w]:
        me.attack_w()

    bot()

    win.fill((255, 255, 255))
    me.draw()
    for bul in me.bullets:
        bul.draw()
    for enemy in enemies:
        enemy.draw()
        for bul in enemy.bullets:
            bul.draw()
    pg.display.update()


pg.quit()
