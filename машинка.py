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
ex = 0

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



def load_level(filename):
    filename = "lvls/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '-'), level_map))


tile_images = {
    'left': pygame.transform.rotate(load_image('право.png'), 180),
    'right': load_image('право.png'),
    'bottom': pygame.transform.rotate(load_image('право.png'), 270),
    'top': pygame.transform.rotate(load_image('право.png'), 90),
    'all': load_image('стена.png'),
    'empty': load_image('тёмнофиолетовый фон.png'),
    'non': load_image('пусто.jpg', 'red'),
    'coin': load_image('звезда для игры.png'),
    'exit': load_image('сундук1.png', -1),
    'портал': load_image('квадрат красивый.jpg')
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
'''
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
        self.image = load_image('квадрат красивый.jpg')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def update(self):
        self.image = pygame.transform.rotate(self.image, 1)

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
    def right(self):
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
door_group = pygame.sprite.Group()

def reboot():
    global all_sprites
    global tiles_group
    global player_group
    global money_group
    global lvl_group
    global door_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    money_group = pygame.sprite.Group()
    lvl_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()

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
            if level[y][x] == 'a':
                Tile('left', x, y)
            if level[y][x] == 'd':
                Tile('right', x, y)
            if level[y][x] == 'w':
                Tile('bottom', x, y)
            if level[y][x] == 's':
                Tile('top', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('all', x, y)
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                new_money = Money('exit', x, y)
            elif level[y][x] == '+':
                Tile('empty', x, y)
                new_money = Money('coin', x, y)
            elif level[y][x] == '-':
                Tile('non', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                door = Door(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y
pygame.display.set_caption('Перемещение героя')
start_screen()
def play(map):
    global ex
    star = 0
    global money
    level_map = load_level(map)
    font = pygame.font.SysFont('Consolas', 30)
    player, level_x, level_y = generate_level(load_level(map))
    #doors = AnimatedSprite(load_image("дверь.png", 'white'), 6, 1, 150, 150)
    screen.fill('black')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = player.pos
                if event.key == pygame.K_UP:
                    if y > 0 and level_map[y - 1][x] not in 'ad#ws':
                        while level_map[y - 1][x] not in 'ad#ws':
                            x, y = x, y - 1
                            player.go(x, y)
                            player.up()
                            if pygame.sprite.spritecollideany(player, money_group):
                                if pygame.sprite.spritecollideany(player, money_group).price == 1:
                                    star += 1
                                else:
                                    money += pygame.sprite.spritecollideany(player, money_group).price
                                pygame.sprite.spritecollideany(player, money_group).kill()
                            if pygame.sprite.spritecollideany(player, door_group):
                                pygame.sprite.spritecollideany(player, door_group).kill()
                                running = False
                                stars[map] = star
                                ex += 1
                                menu()
                if event.key == pygame.K_DOWN:
                    if y < level_y - 1 and level_map[y + 1][x] not in 'ad#ws':
                        while level_map[y + 1][x] not in 'ad#ws':
                            x, y = x, y + 1
                            player.go(x, y)
                            player.image = player_image
                            if pygame.sprite.spritecollideany(player, money_group):
                                if pygame.sprite.spritecollideany(player, money_group).price == 1:
                                    star += 1
                                else:
                                    money += pygame.sprite.spritecollideany(player, money_group).price
                                pygame.sprite.spritecollideany(player, money_group).kill()
                            if pygame.sprite.spritecollideany(player, door_group):
                                pygame.sprite.spritecollideany(player, door_group).kill()
                                running = False
                                stars[map] = star
                                ex += 1
                                menu()
                if event.key == pygame.K_LEFT:
                    if x > 0 and level_map[y][x - 1] not in 'ad#ws':
                        while level_map[y][x - 1] not in 'ad#ws':
                            x, y = x - 1, y
                            player.go(x, y)
                            player.left()
                            if pygame.sprite.spritecollideany(player, money_group):
                                if pygame.sprite.spritecollideany(player, money_group).price == 1:
                                    star += 1
                                else:
                                    money += pygame.sprite.spritecollideany(player, money_group).price
                                pygame.sprite.spritecollideany(player, money_group).kill()
                            if pygame.sprite.spritecollideany(player, door_group):
                                pygame.sprite.spritecollideany(player, door_group).kill()
                                running = False
                                stars[map] = star
                                ex += 1
                                menu()
                if event.key == pygame.K_RIGHT:
                    if x < level_x - 1 and level_map[y][x + 1] not in 'ad#ws':
                        while level_map[y][x + 1] not in 'ad#ws':
                            x, y = x + 1, y
                            player.go(x, y)
                            player.right()
                            if pygame.sprite.spritecollideany(player, money_group):
                                if pygame.sprite.spritecollideany(player, money_group).price == 1:
                                    star += 1
                                else:
                                    money += pygame.sprite.spritecollideany(player, money_group).price
                                pygame.sprite.spritecollideany(player, money_group).kill()
                            if pygame.sprite.spritecollideany(player, door_group):
                                pygame.sprite.spritecollideany(player, door_group).kill()
                                running = False
                                stars[map] = star
                                ex += 1
                                menu()
        door_group.update()

        tiles_group.draw(screen)
        player_group.draw(screen)
        door_group.draw(screen)
        screen.blit(font.render(str(money), True, 'yellow'), (width - 100, 0))

        pygame.display.flip()
    pygame.quit()

stars = {'map1': 0, 'map2': 0, 'map3': 0, 'map4': 0,
         'map5': 0, 'map6': 0, 'map7': 0, 'map8': 0,
         'map9': 0, 'map10': 0, 'map11': 0, 'map12': 0,
         'map13': 0, 'map14': 0, 'map15': 0, 'map16': 0
         }
lvl = 1
energy = 5
def menu():
    global lvl
    global ex
    global energy
    global money
    if ex == lvl:
        ex = 0
        lvl += 1
        energy = 5
        money += 50 * lvl
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('new lvl!!!', False, 'yellow'), (width // 2 - 150, height // 2 - 50))
        screen.blit(font.render(str(lvl * 50), False, 'yellow'), (width // 2 - 150, height // 2 + 50))
        pygame.display.flip()
        sleep(2)

    fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Consolas', 38)

    clock = pygame.time.Clock()
    pygame.draw.rect(screen, 'black',
                     (0, 0, width, 40))
    fon = font.render(str(money), 10, pygame.Color('yellow'))
    screen.blit(fon, (width - len(str(money)) * 38 - 60, 0))
    font = pygame.font.Font(None, 30)
    screen.blit(font.render(str(money), False, 'yellow'), (width, 0))
    font = pygame.font.Font(None, 60)
    screen.blit(font.render('lvl' + str(lvl), False, 'yellow'), (0, 0))
    en = load_image('энергия.jpg')
    screen.blit(en, en.get_rect().move(width // 2 - 100, 5))
    for i in range(1, energy + 1):
        pygame.draw.rect(screen, 'yellow',
                         (width // 2 - 80 + i * 22, 5, 20, 30))
    pygame.draw.rect(screen, 'yellow',
                    (width - 45, 3, 30, 30))
    pygame.draw.line(screen, 'black',
                     [width - 40, 17],
                     [width - 20, 17], 3)
    pygame.draw.line(screen, 'black',
                     [width - 30, 7],
                     [width - 30, 27], 3)
    num = 0
    star = load_image('звезда для меню.png', -1)
    padlock = load_image('замок.webp', -2)
    for i in range(1, 5):
        for j in range(1, 5):
            num += 1
            font = pygame.font.SysFont('Consolas', 70)
            pygame.draw.rect(screen, 'blue',
                             (j * 100 - 40, i * 100 - 30, 75, 75))
            screen.blit(font.render(str(num), False, 'black'), (j * 100 - 40, i * 100 - 30))
            for x in range(1, stars['map' + str(num)] + 1):
                screen.blit(star, star.get_rect().move(j * 100 - 40 + (x - 1) * 25, i * 100 + 20))
            if i != 1 or j != 1:
                if stars['map' + str(num - 1)] == 0:
                    screen.blit(padlock, padlock.get_rect().move(j * 100 - 40, i * 100 - 30))
    image = load_image('обрезанная монета.png', 'black')
    dog_rect = image.get_rect(
        bottomright=(width - len(str(money)) * 10 - 30, image.get_height() + 2))
    screen.blit(image, dog_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y in range(70, 141):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            energy -= 1
                            reboot()
                            play('map' + str(i))
                            return 0
                if y in range(170, 241):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            energy -= 1
                            reboot()
                            play('map' + str(i + 4))
                            return 0
                if y in range(270, 341):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            energy -= 1
                            reboot()
                            play('map' + str(i + 8))
                            return 0
                if y in range(370, 441):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            energy -= 1
                            reboot()
                            play('map' + str(i + 12))
                            return 0
        lvl_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
menu()