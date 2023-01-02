import sys
import pygame
import os
from time import sleep
from pygame.locals import *

pygame.init()
FPS = 50
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
money = 10

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл {fullname}, не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    elif colorkey == -1:
        image.set_colorkey(image.get_at((0, 0)))
    else:
        image.set_colorkey(colorkey)
    return image

def terminate():
    pygame.quit()
    sys.exit()
def start_screen():
    intro_text = []

    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        pygame.display.flip()
        clock.tick(FPS)

def menu():

    intro_text = ['ddsfasfsa', 'dddd', 'ddd']
    font = pygame.font.SysFont('Consolas', 38)

    clock = pygame.time.Clock()
    pygame.draw.rect(screen, 'black',
                     (0, 0, width, 40))
    fon = font.render(str(money), 10, pygame.Color('yellow'))
    screen.blit(fon, (width - len(str(money)) * 38 - 60, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    screen.blit(font.render(str(money), False, 'yellow'), (width, 0))
    '''
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    '''
    pygame.draw.rect(screen, 'yellow',
                     (width - 45, 3, 30, 30))
    pygame.draw.line(screen, 'black',
                     [width - 40, 17],
                     [width - 20, 17], 3)
    pygame.draw.line(screen, 'black',
                     [width - 30, 7],
                     [width - 30, 27], 3)
    for i in range(1, 20):
        Lvl_choose(i * 25, i * 25, i)
    image = load_image('обрезанная монета.png', 'black')
    dog_rect = image.get_rect(
        bottomright=(width - len(str(money)) * 10 - 30, image.get_height() + 2))
    screen.blit(image, dog_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        lvl_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return level_map
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'wall': load_image('кирпичи.jpg'),
    'empty': load_image('земля.jpeg'),
    'non': load_image('пусто.jpg', 'red'),
    'coin': load_image('звезда для игры.png'),
    'exit': load_image('сундук1.png', -1)
}
player_image = load_image('куб.jpeg')
#door_image = load_image('exit.gif')

tile_width = tile_height = 25


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Money(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, money_group)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == 'coin':
                self.price = 1
            else:
                self.price = 10
class Lvl_choose(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, number):
        super().__init__(lvl_group)
        self.pos = (pos_x, pos_y)
        self.image = load_image('квадрат.jpg', 'red')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(door_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
'''
class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group)
        self.image = door_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1])
'''
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1])
    def reight(self):
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, 90)

    def left(self):
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, 270)

    def up(self):
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, 180)

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
lvl_group = pygame.sprite.Group()

def draw(screen, number):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(number), True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                new_money = Money('exit', x, y)
            elif level[y][x] == '+':
                Tile('empty', x, y)
                new_money = Money('coin', x, y)
            elif level[y][x] == ' ':
                Tile('non', x, y)
            #elif level[y][x] == '!':
              #  Tile('empty', x, y)
                #door = Door(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y
pygame.display.set_caption('Перемещение героя')
running = True
start_screen()
menu()
level_map = load_level('map.txt')
font = pygame.font.SysFont('Consolas', 30)
player, level_x, level_y = generate_level(load_level('map.txt'))
#doors = AnimatedSprite(load_image("дверь.png", 'white'), 6, 1, 150, 150)
screen.fill('black')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            x, y = player.pos
            if event.key == pygame.K_UP:
                if y > 0 and level_map[y - 1][x] != '#':
                    while level_map[y - 1][x] != '#':
                        x, y = x, y - 1
                        player.go(x, y)
                        if pygame.sprite.spritecollideany(player, money_group):
                            money += pygame.sprite.spritecollideany(player, money_group).price
                            pygame.sprite.spritecollideany(player, money_group).kill()
                        player.up()
            if event.key == pygame.K_DOWN:
                if y < level_y - 1 and level_map[y + 1][x] != '#':
                    while level_map[y + 1][x] != '#':
                        x, y = x, y + 1
                        player.go(x, y)
                        if pygame.sprite.spritecollideany(player, money_group):
                            money += pygame.sprite.spritecollideany(player, money_group).price
                            pygame.sprite.spritecollideany(player, money_group).kill()
                        player.image = player_image
            if event.key == pygame.K_LEFT:
                if x > 0 and level_map[y][x - 1] != '#':
                    while level_map[y][x - 1] != '#':
                        x, y = x - 1, y
                        player.go(x, y)
                        player.left()
                        if pygame.sprite.spritecollideany(player, money_group):
                            money += pygame.sprite.spritecollideany(player, money_group).price
                            pygame.sprite.spritecollideany(player, money_group).kill()
            if event.key == pygame.K_RIGHT:
                if x < level_x - 1 and level_map[y][x + 1] != '#':
                    while level_map[y][x + 1] != '#':
                        x, y = x + 1, y
                        player.go(x, y)
                        player.reight()
                        if pygame.sprite.spritecollideany(player, money_group):
                            money += pygame.sprite.spritecollideany(player, money_group).price
                            pygame.sprite.spritecollideany(player, money_group).kill()

                            #number += 1
                        #if level_map[y][x] == '+':

            #if level_map[y][x] == 'x':
                #player.kill()

    tiles_group.draw(screen)
    player_group.draw(screen)
    #door_group.draw(screen)
    screen.blit(font.render(str(money), True, (0, 0, 0)), (width - 100, 0))
    pygame.display.flip()
pygame.quit()