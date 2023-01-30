import sys
import pygame
import os
from time import sleep
from datetime import datetime, timedelta

pygame.init()
time = timedelta(seconds=10)
last_update = datetime.now()
FPS = 50
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
money = 0
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
    fon = pygame.transform.scale(load_image('заставка.jpg', 'white'), (500, 500))
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
    'leftt': pygame.transform.rotate(load_image('иглы.png'), 90),
    'rightt': pygame.transform.rotate(load_image('иглы.png'), 270),
    'topp': load_image('иглы.png', 'red'),
    'bottomm': pygame.transform.rotate(load_image('иглы.png', 'red'), 180),
    'all': load_image('стена.png'),
    'empty': load_image('тёмнофиолетовый фон.png'),
    'non': load_image('пусто.jpg', 'red'),
    'coin': load_image('звезда для игры.png'),
    'exit': load_image('сундук1.png', -1),
    'портал': load_image('квадрат красивый.jpg'),
    'диск': load_image('диск.png', -1),
    'телепорт': load_image('портал.jpg', -1)
}
player_image = load_image('куб.jpeg')
player_image_num = 0
#door_image = load_image('exit.gif')

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
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def right(self):
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, 90)

    def left(self):
        self.image = player_image
        self.image = pygame.transform.rotate(self.image, 270)

    def up(self):
        self.image = player_image
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
        super().__init__(*group)
        self.image = load_image('лазер актив.png', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.coff = 3
        self.laser = True
        self.las = None


    def update(self):
        global laser_help_group
        if self.laser and self.coff <= 0:
            self.laser = False
            self.image = load_image('лазер актив.png', -1)
            self.las = Laser_gun_helper(self.rect.x, self.rect.y)
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
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group)
        self.image = load_image('лазер.png', -1)
        self.rect = self.image.get_rect().move(0 + pos_x - width, pos_y + 8)
        self.pos = (tile_width * pos_x, tile_height * pos_y)

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('пушка верх мини.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.laser = Laser_help(pos_x, pos_y, monster_group)
        self.las = None
        self.count = 0
    def update(self):
        self.count += 1
        if self.count % 50 == 1:
            self.laser.kill()
            self.laser = False
        if self.count % 50 == 49:
            self.laser = Laser_help(self.pos[0] // tile_width, self.pos[1] // tile_height, monster_group)
            print(1)

class Laser_help(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('лазер верт.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x + 11, tile_height * (pos_y + 1))
        self.pos = (tile_width * pos_x, tile_height * pos_y)

'''
    def update(self):
        self.count += 1
        if self.count % 25 == 0:
            self.laser = Laser_help(self.pos[0], self.pos[1], monster_group)
            sleep(222)
        if self.count % 25 == 1:
            self.laser.kill()

class Laser_help(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = load_image('лазер верт.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
'''
'''
    def update(self):
        global laser_help_group
        if self.laser and self.coff <= 0:
            self.laser = False
            self.las = Laser_gun_helper(self.rect.x, self.rect.y)
        elif not self.laser and self.coff <= 0:
            self.laser = True
            if self.las:
                self.las.kill()
        else:
            self.laser = False
        if self.laser:
            pygame.draw.rect(screen, 'yellow',
                             (0, self.rect.y, self.rect.x, self.rect.y), 8)
        if self.rect.x - width + 25 >= self.pos[0] or self.rect.x == self.pos[0]:
            self.coff *= -1
            self.image = pygame.transform.flip(self.image, True, False)

class Laser_helper(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group)
        self.image = load_image('лазер верт.png', -1)
        self.rect = self.image.get_rect().move(0 + pos_x - width, pos_y + 8)
        self.pos = (tile_width * pos_x, tile_height * pos_y)
        self.coff = 3
'''

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
lvl_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
laser_help_group = pygame.sprite.Group()

def reboot():
    global all_sprites
    global tiles_group
    global player_group
    global money_group
    global lvl_group
    global door_group
    global monster_group
    global laser_help_group
    global laser_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    money_group = pygame.sprite.Group()
    lvl_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()
    laser_help_group = pygame.sprite.Group()

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
            if level[y][x] == '*':
                Tile('empty', x, y, tiles_group, all_sprites)
                Tile('диск', x, y, tiles_group, all_sprites)
            if level[y][x] == '1':
                Tile('empty', x, y, tiles_group, all_sprites)
                Tile('телепорт', x, y, tiles_group, all_sprites)
            if level[y][x] == 'a':
                Tile('left', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'd':
                Tile('right', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'w':
                Tile('bottom', x, y, tiles_group, all_sprites)
            elif level[y][x] == 's':
                Tile('top', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'f':
                Tile('leftt', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'h':
                Tile('rightt', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'g':
                Tile('bottomm', x, y, tiles_group, all_sprites)
            elif level[y][x] == 't':
                Tile('topp', x, y, tiles_group, all_sprites)
            elif level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('all', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'x':
                Tile('empty', x, y, tiles_group, all_sprites)
                Money('exit', x, y, tiles_group, money_group)
            elif level[y][x] == '+':
                Tile('empty', x, y, tiles_group)
                Money('coin', x, y, tiles_group, money_group)
            elif level[y][x] == '-':
                Tile('non', x, y, tiles_group)
            elif level[y][x] == '!':
                Tile('empty', x, y, tiles_group, all_sprites)
                Door(x, y, door_group)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group)
            elif level[y][x] == 'M':
                Tile('empty', x, y, tiles_group, all_sprites)
                Monster(x, y, monster_group)
            elif level[y][x] == 'L':
                Tile('empty', x, y, tiles_group, all_sprites)
                Laser_gun(x, y, laser_group)
            elif level[y][x] == 'N':
                Tile('empty', x, y, tiles_group, all_sprites)
                Laser(x, y, laser_group)
    return new_player, x, y
pygame.display.set_caption('Перемещение героя')
start_screen()
star = 0
def play(map):
    global ex
    global money
    star = 0
    level_map = load_level(map)
    font = pygame.font.SysFont('Consolas', 30)
    player, level_x, level_y = generate_level(load_level(map))
    screen.fill('black')
    running = True
    fps = 60
    clock = pygame.time.Clock()
    def game_over(exp, star=None):
        global ex
        global running
        running = False
        if star:
            if stars[map] < star:
                stars[map] = star
        ex += exp
        if exp == 1:
            menu('win')
        else:
            menu('lose')

    def teleport(x, y):
        if level_map[y][x] in '1':
            for coord_y in range(level_y):
                for coord_x in range(level_x):
                    if level_map[coord_y][coord_x] == '1':
                        if coord_y != y or coord_x != x:
                            return 25 * (coord_x + 1), 25 * coord_y
    def check_move():
        if not go_up and not go_down and not go_right and not go_left:
            return True
        return False
    def give_money():
        global money
        star = 0
        if pygame.sprite.spritecollideany(player, money_group):
            if pygame.sprite.spritecollideany(player, money_group).price == 1:
                star += 1
            else:
                money += pygame.sprite.spritecollideany(player, money_group).price
            pygame.sprite.spritecollideany(player, money_group).kill()
        return star
    go_up = False
    go_down = False
    go_right = False
    go_left = False
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = player.pos
                if event.key == pygame.K_UP:
                    if y > 0 and level_map[y - 1][x] not in 'ad#wsN':
                        x, y = x, y - 1
                        if check_move():
                            go_up = True
                            player.up()
                if event.key == pygame.K_DOWN:
                    if y < level_y - 1 and level_map[y + 1][x] not in 'ad#wsN':
                        x, y = x, y + 1
                        if check_move():
                            go_down = True
                            player.image = player_image
                if event.key == pygame.K_LEFT:
                    if x > 0 and level_map[y][x - 1] not in 'ad#wsN':
                        print(1)
                        x, y = x - 1, y
                        if check_move():
                            go_left = True
                            player.left()
                if event.key == pygame.K_RIGHT:
                    if x < level_x - 1 and level_map[y][x + 1] not in 'ad#wsN':
                        x, y = x + 1, y
                        if check_move():
                            go_right = True
                            player.right()
        if pygame.sprite.spritecollideany(player, monster_group):
            game_over(0.5)
            return 0
        x, y = player.pos
        if go_right:
            x, y = player.pos
            if count == 25:
                count = 0
                player.pos = (player.rect.x // tile_width, player.rect.y // tile_height)
                if level_map[y][x + 2] in 'ad#wsN':
                    go_right = False
            else:
                count += 5
                if level_map[y][x + 1] in 'ftgh*' or pygame.sprite.spritecollideany(player, monster_group):
                    game_over(0.5)
                    return 0
                player.go(5, 0)
        if go_left:
            if count == 25:
                count = 0
                player.pos = (player.rect.x // tile_width, player.pos[1])
                if level_map[y][x - 2] in 'ad#wsN':
                    go_left = False
            else:
                count += 5
                if level_map[y][x - 1] in 'ftgh*' or pygame.sprite.spritecollideany(player, monster_group):
                    game_over(0.5)
                    return 0
                player.go(-5, 0)
        if go_up:
            if count == 25:
                count = 0
                player.pos = (player.rect.x // tile_width, player.rect.y // tile_height)
                if level_map[y - 2][x] in 'ad#wsN':
                    go_up = False
            else:
                count += 5
                if level_map[y - 1][x] in 'ftgh*' or pygame.sprite.spritecollideany(player, monster_group):
                    game_over(0.5)
                    return 0
                player.go(0, -5)
        elif go_down:
            if count == 25:
                count = 0
                player.pos = (player.rect.x // tile_width, player.rect.y // tile_height)
                if level_map[y + 2][x] in 'ad#wsN':
                    go_down = False
            else:
                count += 5
                if level_map[y + 1][x] in 'ftgh*' or pygame.sprite.spritecollideany(player, monster_group):
                    game_over(0.5)
                    return 0
                player.go(0, 5)
        x, y = player.pos
        star += give_money()
        if pygame.sprite.spritecollideany(player, door_group):
            pygame.sprite.spritecollideany(player, door_group).kill()
            game_over(1, star)
            return 0
        if teleport(x, y):
            player.rect.x, player.rect.y = teleport(x, y)
            player.pos = (player.rect.x // tile_width, player.rect.y // tile_height)
            go_right, go_down, go_left, go_up = False, False, False, False
        door_group.update()
        monster_group.update()
        laser_group.update()
        tiles_group.draw(screen)
        laser_group.draw(screen)
        laser_help_group.draw(screen)
        door_group.draw(screen)
        monster_group.draw(screen)
        player_group.draw(screen)
        screen.blit(font.render(str(money), True, 'yellow'), (width - 100, 0))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

stars = {'map1': 1, 'map2': 1, 'map3': 1, 'map4': 1,
         'map5': 1, 'map6': 0, 'map7': 0, 'map8': 0,
         'map9': 0, 'map10': 0, 'map11': 0, 'map12': 0,
         'map13': 0, 'map14': 0, 'map15': 0, 'map16': 0, 'map0': 3
         }
lvl = 1
energy = 4
def menu(lose_or_win=None):
    global lvl
    global ex
    global energy
    global money
    global player_image
    global player_image_num
    global last_update
    print(ex)
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
    if lose_or_win == 'win':
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('WIN!!!', False, 'yellow'), (width // 2 - 120, height // 2 - 50))
        pygame.display.flip()
        sleep(0.5)
    if lose_or_win == 'lose':
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('LOSER!!!', False, 'yellow'), (width // 2 - 120, height // 2 - 50))
        pygame.display.flip()
        sleep(0.5)

    no_go_shop = True
    no_go_shop_money = True
    while True:
        if datetime.now() - last_update > time:
            last_update = datetime.now()
            if energy != 5:
                energy += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if y in range(70, 141):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            if stars['map' + str(i - 1)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i))
                                return 0
                if y in range(170, 241):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            if stars['map' + str(i + 3)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i + 4))
                                return 0
                if y in range(270, 341):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            if stars['map' + str(i + 7)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i + 8))
                                return 0
                if y in range(370, 441):
                    for i in range(1, 5):
                        if x in range(i * 100 - 40, i * 100 + 30):
                            if stars['map' + str(i + 11)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i + 12))
                                return 0
                if x in range(width // 2 - 50, width // 2 + 50) and y in range(height - 50, height - 20) and no_go_shop:
                    no_go_shop = False
                elif x in range(width // 2 - 50, width // 2 + 50) and y in range(height - 50, height - 20) and not no_go_shop:
                    no_go_shop = True
                elif x in range(width - 45, width - 15) and y in range(3, 33):
                    no_go_shop_money = False
        if no_go_shop and no_go_shop_money:
            fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
            screen.blit(fon, (0, 0))
            font = pygame.font.SysFont('Consolas', 38)

            clock = pygame.time.Clock()
            pygame.draw.rect(screen, 'black',
                             (0, 0, width, 40))
            fon = font.render(str(money), 10, pygame.Color('yellow'))
            screen.blit(fon, (width - len(str(money)) * 38 - 38 * 2, 0))
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
                bottomright=(width - 50, image.get_height() + 2))
            screen.blit(image, dog_rect)
            pygame.draw.rect(screen, 'yellow',
                             (width // 2 - 50, height - 50, 100, 30))
            font = pygame.font.Font(None, 35)
            screen.blit(font.render('shop', False, 'black'), (width // 2 - 45, height - 50))

            lvl_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        elif not no_go_shop_money:
            money += 10
            no_go_shop_money = True
        else:
            pygame.draw.rect(screen, 'yellow',
                             (width // 2 - 140, height // 2 - 100, 300, 200))
            pygame.draw.rect(screen, 'black',
                             (width // 2 - 115, height // 2 - 85, 110, 150), 2)
            screen.blit(load_image('персонаж 2 для магазина.jpg', -1), load_image('персонаж 2 для магазина.jpg', -1).get_rect().move(width // 2 - 110, height // 2 - 80))
            if player_image_num != 1:
                font = pygame.font.Font(None, 70)
                screen.blit(font.render('200', False, 'black'), (width // 2 - 105, height // 2 + 20))
            pygame.draw.rect(screen, 'black',
                             (width // 2 + 25, height // 2 - 85, 110, 150), 2)
            screen.blit(load_image('персонаж 4 для магазина.png', 'yellow'),
                        load_image('персонаж 4 для магазина.png', 'yellow').get_rect().move(width // 2 + 30,
                                                                                      height // 2 - 80))
            if player_image_num != 2:
                font = pygame.font.Font(None, 70)
                screen.blit(font.render('800', False, 'black'), (width // 2 + 35, height // 2 + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y in range(height // 2 - 85, height // 2 + 65):
                    if x in range(width // 2 - 115, width // 2 - 15):
                        if money >= 200 and player_image_num != 1:
                            money -= 200
                            player_image = load_image('персонаж 2.jpg')
                            player_image_num = 1
                            no_go_shop = True
                if y in range(height // 2 - 85, height // 2 + 65):
                    if x in range(width // 2 + 25, width // 2 + 135):
                        if money >= 800 and player_image_num != 2:
                            money -= 800
                            player_image = load_image('персонаж 3.png')
                            player_image_num = 2
                            no_go_shop = True
            pygame.display.flip()
menu()