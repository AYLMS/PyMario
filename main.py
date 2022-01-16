import sys

import pygame
from PyQt6.QtWidgets import QApplication, QMessageBox

from dialog import get_level


class Player(pygame.sprite.Sprite):
    '''Класс игрока'''
    def __init__(self, data=((0, 0), 'YP_data/Textures/mar.png', (160*8, 90*8))):
        # Переделывай всю физику игрока
        pygame.sprite.Sprite.__init__(self)
        print(data)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40))
        '''Маска для колизий'''
        self.speed_x = 0
        self.speed_y = 0
        '''Спрайты для столкновений бить пж пж пж'''
        '''self.sdown = pygame.Surface((80, 1))
        self.sdr = self.sdown.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40))'''
        self.left = True
        self.cmfcs = False
        self.cl = [False, False, False, False]

    def update(self):
        if self.cmfcs:
            return
        for obj in helpers:
            i, bool = obj.checkcollide()
            self.cl[i] = bool
        '''Движение вправо'''
        if self.cl[1] and self.speed_x > -2:
            self.speed_x += -2
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.speed_x < 10:
                self.speed_x += 2
        '''Движение влево'''
        if self.cl[3] and self.speed_x < 2:
            self.speed_x += 2
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.speed_x > -10:
                self.speed_x += -2
        '''Торможение (Нехрен быть инертным)'''
        if self.cl[2]:
            if pygame.sprite.spritecollide(self, all_obstacles, False):
                self.speed_y += -1
            self.speed_y = 0
        if self.cl[0]:
            self.speed_y = -self.speed_y
        if self.speed_x > 0:
            self.speed_x += -1
        elif self.speed_x < 0:
            self.speed_x += 1
        '''Свободное падение'''
        if not self.cl[2]:
            if self.speed_y < 15:
                self.speed_y += 1
        elif pygame.key.get_pressed()[pygame.K_UP]:
            self.speed_y = -15
        else:
            self.speed_y = 0
        '''Столкновения'''
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

    def move(self, data=(0, 0)):
        dx, dy = data
        self.rect.x += dx
        self.rect.y += dy


class Lrud(pygame.sprite.Sprite):
    def __init__(self, data=((0, 0), (160*8, 90*8), (48, 80), 1)):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), (self.width, self.height), (self.objsx, self.objsy), self.axis = data
        self.speed_x = 0
        self.speed_y = 0
        self.cmfcs = False
        if self.axis == 0:
            self.image = pygame.Surface((46, 1))
            #self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40 - int(self.objsy/2) - 1))
        elif self.axis == 1:
            self.image = pygame.Surface((1, 78))
            #self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40 + int(self.objsx/2), self.y * 80 + 40))
        elif self.axis == 2:
            self.image = pygame.Surface((46, 1))
            #self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40 + int(self.objsy/2) + 1))
        elif self.axis == 3:
            self.image = pygame.Surface((1, 78))
            #self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40 - int(self.objsx/2), self.y * 80 + 40))

    def update(self):
        if not self.cmfcs:
            for obj in players:
                self.speed_x, self.speed_y = obj.speed_x, obj.speed_y
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x

    def checkcollide(self):
        if pygame.sprite.spritecollide(self, all_obstacles, False):
            return self.axis, True
        else:
            return self.axis, False


class Obstacle(pygame.sprite.Sprite):
    '''Класс препядствия'''
    def __init__(self, data=((0, 0), 'YP_data/Textures/mar.png', (160*8, 90*8))):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))
        '''Маска для колизий'''
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, data=(0, 0)):
        dx, dy = data
        self.rect.x += dx
        self.rect.y += dy


class Coin(pygame.sprite.Sprite):
    def __init__(self, data=((0, 0), 'YP_data/Textures/coin.png', (160*8, 90*8))):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))
        '''Маска для колизий'''
        self.mask = pygame.mask.from_surface(self.image)


class Camera:
    '''Класс камеры'''
    def __init__(self, data=()):
        self.needmove_x, self.needmove_y = False, False

    def move(self, data=(object, (0, 0))):
        object, (dx, dy) = data
        if self.needmove_x:
            object.rect.x += -dx
        if self.needmove_y:
            object.rect.y += -dy


def LoadLvL(lvl=1):
    lvlname = f'YP_data/Levels/level_{lvl}.txt'
    print('Очистка прошлого уровня')
    for el in all_sprites:
        el.kill()
    print('Загрузка уровня')
    with open(lvlname, 'r') as level_txt:
        data = level_txt.read()
    lvl_map = []
    for row in data.split('\n'):
        addrow = list(row)
        lvl_map.append(addrow)
    for y in range(len(lvl_map)):
        for x in range(len(lvl_map[y])):
            if lvl_map[y][x] == '.':
                data = ((x, y), 'YP_data/Textures/grass.png', (80, 80))
                lvl_map[y][x] = data
                obj = Obstacle(data)
                all_sprites.add(obj)
            elif lvl_map[y][x] == '@':
                '''подзагрузил игрока'''
                data = ((x, y), 'YP_data/Textures/mar.png', (160 * 8, 90 * 8))
                pl = Player(data)
                players.add(pl)
                all_entities.add(pl)
                all_sprites.add(pl)
                for i in range(4):
                    data = ((x, y), (160*8, 90*8), (48, 80), i)
                    helper = Lrud(data)
                    helpers.add(helper)
                    all_sprites.add(helper)
                lvl_map[y][x] = data
            elif lvl_map[y][x] == '#':
                data = ((x, y), 'YP_data/Textures/box.png', (80, 80))
                lvl_map[y][x] = data
                obj = Obstacle(data)
                all_obstacles.add(obj)
                all_sprites.add(obj)
            elif lvl_map[y][x] == 'C':
                data = ((x, y), 'YP_data/Textures/coin.png', (36, 60))
                lvl_map[y][x] = data
                coin = Coin(data)
                all_sprites.add(coin)
                coins.add(coin)


pygame.init()
'''Переменные'''
app = QApplication(sys.argv)
current_lvl, min_lvl, mx_lvl = 1, 1, 2
lvl = get_level(app, current_lvl, min_lvl, mx_lvl)
while not lvl:
    QMessageBox.warning(None, 'Ошибка', 'Вы не выбрали уровень')
    lvl = get_level(app, current_lvl, min_lvl, mx_lvl)
width, height = size = 160*8, 90*8
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# Прямо ваапще все спрайты
all_sprites = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
# Спрайты сущностей
all_entities = pygame.sprite.Group()
# Спрайты врагов
# Спрайт игрока
players = pygame.sprite.Group()
helpers = pygame.sprite.Group()
# Спрайты монет и подобного фуфла
coins = pygame.sprite.Group()
all_shit = pygame.sprite.Group()
'''Предустановки к игровому циклу'''
# Подгрузка уровня
LoadLvL(lvl)
# СОздание камеры
'''cam = Camera()'''
screen.fill((192, 192, 255))
running = True
'''Игровой цикл'''
while running:
    # Установка частоты обновления
    clock.tick(60)
    '''Цикл действий'''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for obj in players:
                    if obj.cmfcs:
                        for el in helpers:
                            el.cmfcs = False
                        obj.cmfcs = False
                    else:
                        for el in helpers:
                            el.cmfcs = True
                        obj.cmfcs = True
            if event.key == pygame.K_5:
                if lvl != 2:
                    lvl += 1
                LoadLvL(lvl)
            if event.key == pygame.K_4:
                if lvl != 1:
                    lvl += -1
                LoadLvL(lvl)
        '''Выход из игры'''
        if event.type == pygame.QUIT:
            running = False
    '''Отрисовка объектов'''
    screen.fill((192, 192, 255))
    # Спрайты
    all_sprites.draw(screen)
    all_entities.update()
    helpers.update()
    '''for obj in all_obstacles:
        obj.move((-10, 0))'''
    pygame.display.flip()
'''Конец игрового цикла'''
pygame.quit()