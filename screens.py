from time import sleep

import pygame


class GN(pygame.sprite.Sprite):
    def __init__(self, filename, size):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = size
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(0 - self.width, self.height/2))
        self.dx = 2
        self.gn = True

    def update(self):
        if self.gn:
            self.rect.x += self.dx
            if self.rect.right >= self.width:
                self.rect.right == self.width
                self.gn = False

    def check(self):
        return self.gn


class Player(pygame.sprite.Sprite):
    def __init__(self, filename, size):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = size
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(self.width/2, self.height/2))
        self.dx = 1

    def update(self):
        self.rect.x += self.dx
        if self.rect.right >= self.width or self.rect.left <= 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.dx = self.dx * -1
            self.rect.x += self.dx


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    size = width, height = 512, 301
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    creatures = pygame.sprite.Group()
    gn = GN('gameover.png', size)
    creatures.add(gn)
    all_sprites.add(gn)
    screen.fill((0, 0, 0))
    running = True
    while running:
        screen.fill((0, 0, 0))
        all_sprites.update()
        creatures.draw(screen)
        pygame.display.flip()
    pygame.quit()