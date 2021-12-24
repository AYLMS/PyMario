import pygame


class Board:
    """Класс доски"""

    def __init__(self, filename='YP_data/Levels/level_1.txt'):
        # Открытие файла
        level_txt = open(filename, 'r')
        data = level_txt.read()
        level_txt.close()
        # Создание матрицы уровня
        self.level_map = []
        for row in data.split('\n'):
            self.level_map.append(row)
        self.height, self.width, self.cell_size = (len(self.level_map), len(self.level_map[-1]), 50)
        print(len(self.level_map), len(self.level_map[-1]))
        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[y])):
                if self.level_map[y][x] != '.' or self.level_map[y][x] == '':
                    if self.level_map[y][x] == '@':
                        # self.level_map[y][x] = 0
                        data = ((x, y), 'YP_data/Textures/grass.png', (50, 50))
                        obj = Obstacle(data)
                        all_sprites.add(obj)
                        all_obstacles.add(obj)
                    elif self.level_map[y][x] == '#':
                        # self.level_map[y][x] = 1
                        data = (x, y), 'YP_data/Textures/box.png', (50, 50)
                        obj = Obstacle(data)
                        all_sprites.add(obj)
                        all_obstacles.add(obj)
                else:
                    # self.level_map[y][x] = -1
                    data = (x, y), 'YP_data/Textures/grass.png', (50, 50)
                    obj = Obstacle(data)
                    all_sprites.add(obj)
                    all_obstacles.add(obj)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.polygon(screen, (192, 64, 192),
                                    [(self.cell_size * x, self.cell_size * y),
                                     (self.cell_size * (x + 1), self.cell_size * y),
                                     (self.cell_size * (x + 1), self.cell_size * (y + 1)),
                                     (self.cell_size * x, self.cell_size * (y + 1))], 1)


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(self, data=((0, 6), 'YP_data/Textures/mar.png', (160 * 5, 90 * 5))):
        pygame.sprite.Sprite.__init__(self)
        print(data)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x * 50 + 25, self.y * 50 + 25))
        self.speed_x = 0
        self.speed_y = 0

    """Движение игрока"""

    def update(self):
        """Стрелка вверх"""
        # Нужно нормально проделать условие прыжка-падения
        if pygame.key.get_pressed()[pygame.K_UP] and self.speed_y == 0:
            self.speed_y += -8
        elif self.speed_y != 0 and self.speed_y < 5:
            self.speed_y += 1
        """Стрелка вниз"""
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            pass
        """Стрелка вправо"""
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.speed_x < 5:
            self.speed_x += 1
        elif self.speed_x > 0:
            self.speed_x += -1
        """Стрелка влево"""
        if pygame.key.get_pressed()[pygame.K_LEFT] and self.speed_x > -5:
            self.speed_x += -1
        elif self.speed_x < 0:
            self.speed_x += 1
        """Перемещение игрока"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def ask_speed(self):
        return (self.speed_x, self.speed_y)


class Camera:
    """Класс камеры"""

    def __init__(self, data=()):
        pass

    def move(self, data=(object, (0, 0))):
        object, (dx, dy) = data
        object.rect.x += -dx
        object.rect.y += -dy


class Enemy(pygame.sprite.Sprite):
    """Класс противника"""
    pass


class Obstacle(pygame.sprite.Sprite):
    """Класс препядствия"""

    def __init__(self, data=((0, 0), 'YP_data/Textures/mar.png', (160 * 5, 90 * 5))):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y), filename, (self.width, self.height) = data
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(self.x * self.width + self.width / 2, self.y * self.height + self.height / 2))


class Interface:
    """Класс интерфейса"""
    pass


pygame.init()
"""Переменные"""
width, height = size = 160 * 5, 90 * 5
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# Прямо ваапще все спрайты
all_sprites = pygame.sprite.Group()
# Спрайты препятсвий
all_obstacles = pygame.sprite.Group()
# Спрайты врагов
# Спрайт игрока
pl = Player()
all_sprites.add(pl)
"""Предустановки к игровому циклу"""
# Подгрузка уровня и создание доски
board = Board()
# СОздание камеры
cam = Camera()
screen.fill((192, 192, 255))
running = True
"""Игровой цикл"""
while running:
    # Установка частоты обновления
    clock.tick(60)
    """Цикл действий"""
    for event in pygame.event.get():
        """Выход из игры"""
        if event.type == pygame.QUIT:
            running = False
    """Отрисовка объектов"""
    screen.fill((192, 192, 255))
    # board.render(screen)
    all_sprites.draw(screen)
    pl.update()
    for sprite in all_obstacles:
        cam.move((sprite, pl.ask_speed()))
    pygame.display.flip()
"""Конец игрового цикла"""
pygame.quit()
