import sys

import pygame
from PyQt6.QtWidgets import QApplication, QMessageBox

from dialog import get_level


class Player(pygame.sprite.Sprite):
    '''Класс игрока'''

    def __init__(self, data=((0, 0), 'YP_data/Textures/mar.png', (160 * 8, 90 * 8), 0)):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height), score = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.x, self.y = self.x * 80 + 40, self.y * 80 + 40
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed_x = 0
        self.speed_y = 0
        self.f1 = pygame.font.Font(None, 36)
        self.score = score
        self.text1 = self.f1.render(f'{self.score}', True, (180, 180, 180))
        self.left = True
        self.cmfcsx = False
        self.cl = [False, False, False, False]
        self.helpers = pygame.sprite.Group()

    def update(self):
        for obj in self.helpers:
            i, bool = obj.checkcollide(all_obstacles)
            self.cl[i] = bool
        '''Движение вправо'''
        if self.cl[1] and not self.cl[3]:
            if self.speed_x > 1:
                self.speed_x = -self.speed_x - 1
            else:
                self.speed_x += -1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.speed_x < 12:
                self.speed_x += 2
            if self.left:
                self.left = False
                self.image = pygame.transform.flip(self.image, True, False)
        '''Help me brother i'm stuck!'''
        if self.cl[0] and self.cl[1] and self.cl[2] and self.cl[3]:
            c = 24 if self.left else -24
            self.rect.x += c
            for obj in self.helpers:
                obj.rect.x += c
        '''Движение влево'''
        if self.cl[3] and not self.cl[1]:
            if self.speed_x < -1:
                self.speed_x = -self.speed_x + 1
            else:
                self.speed_x += 1
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.speed_x > -12:
                self.speed_x += -2
            if not self.left:
                self.left = True
                self.image = pygame.transform.flip(self.image, True, False)
        '''Торможение (Нехрен быть инертным)'''
        if self.cl[0]:
            self.speed_y = -self.speed_y
        if self.speed_x > 0:
            self.speed_x += -1
        elif self.speed_x < 0:
            self.speed_x += 1
        '''Свободное падение'''
        if self.cl[2]:
            self.speed_y = 0
        elif self.speed_y < 20:
            self.speed_y += 1
        if pygame.key.get_pressed()[pygame.K_UP] and (not self.cl[3] and not self.cl[1] and self.cl[2]):
            self.speed_y = -20
        if self.cl[2] and (self.cl[1] or self.cl[3]):
            self.speed_y += -1
        '''Столкновения'''
        if pygame.sprite.groupcollide(players, coins, False, True):
            self.score += 10
            self.text1 = self.f1.render(f'{self.score}', True,
                                        (90, 90, 90))
        screen.blit(self.text1, (15 * 80 + 40, 0))
        if self.rect.centerx >= 10 * 80 and not self.left and self.x <= self.width - 6 * 80:
            for obj in all_shit:
                obj.rect.x += -self.speed_x
        elif self.rect.centerx <= 6 * 80 <= self.x and self.left:
            for obj in all_shit:
                obj.rect.x += -self.speed_x
        else:
            self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.y += self.speed_y
        self.x += self.speed_x
        if self.rect.centery > 9 * 80:
            print('dead inside')
            for obj in all_sprites:
                obj.kill()
        if pygame.sprite.groupcollide(players, flags, False, True):
            print('nextlvl')

    def move(self, data=(0, 0)):
        dx, dy = data
        self.rect.x += dx
        self.rect.y += dy


class Lrud(pygame.sprite.Sprite):
    def __init__(self, data=((0, 0), (160 * 8, 90 * 8), (48, 80), 1, pygame.sprite.Group)):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), (self.width, self.height), (self.objsx, self.objsy), self.axis, self.group = data
        self.speed_x = 0
        self.speed_y = 0
        self.cmfcs = False
        if self.axis == 0:
            self.image = pygame.Surface((46, 1))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40 - int(self.objsy / 2) - 1))
        elif self.axis == 1:
            self.image = pygame.Surface((1, 78))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40 + int(self.objsx / 2), self.y * 80 + 40))
        elif self.axis == 2:
            self.image = pygame.Surface((46, 1))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40, self.y * 80 + 40 + int(self.objsy / 2) + 1))
        elif self.axis == 3:
            self.image = pygame.Surface((1, 78))
            self.rect = self.image.get_rect(center=(self.x * 80 + 40 - int(self.objsx / 2), self.y * 80 + 40))
        # self.image.set_colorkey((0, 0, 0))

    def update(self):
        if self.group:
            for obj in self.group:
                dx, dy = obj.rect.center
                if self.axis == 0:
                    dy = obj.rect.centery - int(self.objsy / 2) - 1
                elif self.axis == 1:
                    dx = obj.rect.centerx + int(self.objsx / 2) + 1
                elif self.axis == 2:
                    dy = obj.rect.centery + int(self.objsy / 2) + 1
                elif self.axis == 3:
                    dx = obj.rect.centerx - int(self.objsx / 2) - 1
            self.rect.center = dx, dy

    def checkcollide(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            return self.axis, True
        else:
            return self.axis, False


class Obstacle(pygame.sprite.Sprite):
    '''Класс препядствия'''

    def __init__(self, data=((0, 0), 'YP_data/Textures/mar.png', (160 * 8, 90 * 8), False, [])):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height), self.need_update, self.cl = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))
        '''Маска для колизий'''
        self.helpers = pygame.sprite.Group()

    def update(self):
        if self.need_update:
            for obj in self.helpers:
                obj.checkcollide(players)


class Coin(pygame.sprite.Sprite):
    def __init__(self, data=((0, 0), 'YP_data/Textures/coin.png', (80, 80))):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))
        '''Маска для колизий'''
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 180)



class Mushroom(pygame.sprite.Sprite):
    def __init__(self, data=((0, 0), 'YP_data/Textures/mushroom.png', (80, 80), False)):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height), self.left = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))


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


class EndScreen(pygame.sprite.Sprite):
    def __init__(self, filename, size):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = size
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.width / 2, self.height / 2))


class Flag(pygame.sprite.Sprite):
    def __init__(self, data):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))
        print('opaaa')


def LoadLvL(lvl=1, score=0):
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
                data = ((x, y), 'YP_data/Textures/grass.png', (80, 80), False, [])
                obj = Obstacle(data)
                all_sprites.add(obj)
                all_obstacles.add(obj)
                all_shit.add(obj)
            elif lvl_map[y][x] == '@':
                '''подзагрузил игрока'''
                data = ((x, y), 'YP_data/Textures/mar.png', (80 * len(lvl_map[-1]), 80 * len(lvl_map)), score)
                pl = Player(data)
                players.add(pl)
                all_entities.add(pl)
                all_sprites.add(pl)
                for i in range(4):
                    data = ((x, y), (80 * len(lvl_map[-1]), 80 * len(lvl_map)), (48, 80), i, players)
                    helper = Lrud(data)
                    pl.helpers.add(helper)
                    all_sprites.add(helper)
            elif lvl_map[y][x] == '#':
                data = ((x, y), 'YP_data/Textures/box.png', (80, 80), False, [])
                obj = Obstacle(data)
                all_obstacles.add(obj)
                all_sprites.add(obj)
                all_shit.add(obj)
            elif lvl_map[y][x] == '?':
                data = ((x, y), 'YP_data/Textures/box.png', (80, 80), True, [False, False, False, False])
                obj = Obstacle(data)
                data = ((x, y), (80 * len(lvl_map[-1]), 80 * len(lvl_map)), (48, 80), 2, all_obstacles)
                helper = Lrud(data)
                obj.helpers.add(helper)
                all_sprites.add(helper)
                all_obstacles.add(obj)
                all_sprites.add(obj)
                all_shit.add(obj)
            elif lvl_map[y][x] == 'C':
                data = ((x, y), 'YP_data/Textures/coin.png', (80, 80))
                coin = Coin(data)
                all_sprites.add(coin)
                coins.add(coin)
                all_shit.add(coin)
            elif lvl_map[y][x] == 'F':
                data = ((x, y), 'YP_data/Textures/flag.png', (80, 80))
                f = Flag(data)
                all_sprites.add(f)
                all_obstacles.add(f)
                flags.add(f)
                all_shit.add(f)
            elif lvl_map[y][x] == 'm':
                data = ((x, y), 'YP_data/Textures/mushroom.png', (80, 80), False)
                obj = Mushroom(data)
                all_sprites.add(obj)
                all_entities.add(obj)
                all_shit.add(obj)
    return lvl


pygame.init()
'''Переменные'''
app = QApplication(sys.argv)
current_lvl, min_lvl, mx_lvl = 1, 1, 2
lvl = get_level(app, current_lvl, min_lvl, mx_lvl)
while not lvl:
    QMessageBox.warning(None, 'Ошибка', 'Вы не выбрали уровень')
    lvl = get_level(app, current_lvl, min_lvl, mx_lvl)
width, height = size = 160 * 8, 90 * 8
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
# Спрайты монет и подобного фуфла
coins = pygame.sprite.Group()
flags = pygame.sprite.Group()
all_shit = pygame.sprite.Group()
'''Предустановки к игровому циклу'''
# Подгрузка уровня
LoadLvL(lvl)
# СОздание камеры
'''cam = Camera()'''
screen.fill((192, 192, 255))
running = True
end = False
'''Игровой цикл'''
fps_counter = 0
while running:
    # Установка частоты обновления
    clock.tick(60)
    fps_counter += 1
    '''Цикл действий'''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if end:
                lvl = LoadLvL(1, 0)
                end = False
                break
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
    all_sprites.update()
    for obj in players:
        score = obj.score
    if fps_counter % 10 == 0:
        for coin in coins:
            coin.rotate()
    if not all_sprites:
        end = True
        es = EndScreen("YP_data/Textures/endscreen.png", (16 * 80, 9 * 80))
        all_sprites.add(es)
        all_entities.add(es)
    if not flags and end == False:
        if lvl < 2:
            lvl = LoadLvL(lvl + 1, score)
        else:
            print(f'Пройдена игра, ваш счет: {score}')
    pygame.display.flip()
'''Конец игрового цикла'''
pygame.quit()
