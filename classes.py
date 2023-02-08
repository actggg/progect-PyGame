import pygame

from load_image import load_image
from tile_images import tile_images

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
tile_width = tile_height = 25


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Money(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'coin':
            self.price = 1
        else:
            self.price = 10


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('квадрат красивый.jpg')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def update(self):
        self.image = pygame.transform.rotate(self.image, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_image, *group):
        super().__init__(*group)
        self.player_image = player_image
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def right(self):
        self.image = self.player_image
        self.image = pygame.transform.rotate(self.image, 90)

    def left(self):
        self.image = self.player_image
        self.image = pygame.transform.rotate(self.image, 270)

    def up(self):
        self.image = self.player_image
        self.image = pygame.transform.rotate(self.image, 180)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('монстр.png', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.coff = 1

    def update(self):
        self.rect.x += self.coff
        if self.rect.x - 50 == self.pos[0] or self.rect.x == self.pos[0]:
            self.coff *= -1
            self.image = pygame.transform.flip(self.image, True, False)


class Laser_gun(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(group[0])
        self.group_for_help = group[-1]
        self.image = load_image('лазер актив.png', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.coff = 3
        self.laser = True
        self.las = None

    def update(self):
        if self.laser and self.coff <= 0:
            self.laser = False
            self.image = load_image('лазер актив.png', -1)
            self.las = Laser_gun_helper(self.rect.x, self.rect.y, self.group_for_help)
        elif not self.laser and self.coff <= 0:
            self.laser = True
            self.image = load_image('лазер пассив.png', -1)
            if self.las:
                self.las.kill()
        else:
            self.laser = False
        self.rect.x += self.coff
        if self.laser:
            pygame.draw.rect(screen, 'yellow',
                             (0, self.rect.y, self.rect.x, self.rect.y), 8)
        if self.rect.x - width + 25 >= self.pos[0] or self.rect.x == self.pos[0]:
            self.coff *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            if self.coff == -1.5:
                self.image = load_image('лазер пассив.png', -1)
            else:
                self.image = load_image('лазер актив.png', -1)


class Laser_gun_helper(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('лазер.png', -1)
        self.rect = self.image.get_rect().move(0 + pos_x - width, pos_y + 8)
        self.pos = (tile_width * pos_x, tile_height * pos_y)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(group[0])
        self.group_for_helper = group
        self.image = load_image('пушка верх мини.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.laser = Laser_help(pos_x, pos_y, self.group_for_helper)
        self.las = None
        self.count = 0

    def update(self):
        self.count += 1
        if self.count % 50 == 1:
            self.laser.kill()
            self.laser = False
        if self.count % 50 == 49:
            self.laser = Laser_help(self.pos[0] // tile_width, self.pos[1] // tile_height, self.group_for_helper)


class Laser_help(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('лазер верт.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x + 11, tile_height * (pos_y + 1))
        self.pos = (tile_width * pos_x, tile_height * pos_y)
