import csv
import sys
from datetime import datetime, timedelta
from time import sleep

import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

from classes import *


def terminate():
    with open('regist.csv', 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        inf = [level, money, experience, ' '.join(my_skin)]
        for num in range(1, 10):
            inf.append(stars['map' + str(num)])
        inf.append(str(player_image_num))
        writer.writerow(inf)
    pygame.quit()
    sys.exit()


def restart():
    with open('regist.csv', 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow('1;0;0;def;0;0;0;0;0;0;0;0;0;0'.split(';'))
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Зловещие подземелья']

    fon = pygame.transform.scale(load_image('заставка.jpg', 'white'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("impact", 40)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 20, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 35
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'yellow',
                     (144, 418, 86, 44))
    pygame.draw.rect(screen, 'yellow',
                     (274, 418, 86, 44))
    font = pygame.font.SysFont("impact", 30)
    screen.blit(font.render(' вход', False, 'black'), (144, 418))
    screen.blit(font.render('выход', False, 'black'), (274, 418))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(144, 221) and y in range(418, 463):
                    return 0
                if x in range(274, 361) and y in range(418, 463):
                    terminate()
        pygame.display.flip()


def load_level(filename):
    filename = "lvls/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '-'), level_map))


def reboot():
    sprite_groups = [all_sprites, tiles_group, player_group, money_group, door_group,
                     monster_group, laser_group, laser_help_group]
    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.kill()


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
                new_player = Player(x, y, player_image, player_group)
            elif level[y][x] == 'M':
                Tile('empty', x, y, tiles_group, all_sprites)
                Monster(x, y, monster_group)
            elif level[y][x] == 'L':
                Tile('empty', x, y, tiles_group, all_sprites)
                Laser_gun(x, y, laser_group, monster_group)
            elif level[y][x] == 'N':
                Tile('empty', x, y, tiles_group, all_sprites)
                Laser(x, y, laser_group, monster_group)
    return new_player, x, y


def play(map):
    global experience
    global money
    pygame.display.set_caption('игра')
    star = 0
    level_map = load_level(map)
    font = pygame.font.SysFont('Consolas', 30)
    player, level_x, level_y = generate_level(load_level(map))
    screen.fill('black')
    running = True
    fps = 60
    clock = pygame.time.Clock()

    def game_over(experience_from_the_level, star=None):
        global experience
        global running
        running = False
        if star:
            if stars[map] < star:
                stars[map] = star
        experience += experience_from_the_level
        if experience_from_the_level == 1:
            menu('win')
            win_music.play()
        else:
            menu('lose')
            death_music.play()

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

    go_up, go_down, go_right, go_left = False, False, False, False
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
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


def menu(lose_or_win=None):
    global level
    global experience
    global energy
    global money
    global player_image
    global player_image_num
    global last_update
    pygame.display.set_caption('меню')
    if experience >= level:
        experience = 0
        level += 1
        energy = 5
        money += 50 * level
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('new lvl!!!', False, 'yellow'), (width // 2 - 150, height // 2 - 50))
        screen.blit(font.render(str(level * 50), False, 'yellow'), (width // 2 - 150, height // 2 + 50))
        pygame.display.flip()
        sleep(2)
    if lose_or_win == 'win':
        win_music.play()
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('WIN!!!', False, 'yellow'), (width // 2 - 120, height // 2 - 50))
        pygame.display.flip()
        sleep(0.5)
    if lose_or_win == 'lose':
        death_music.play()
        font = pygame.font.Font(None, 100)
        fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
        screen.blit(fon, (0, 0))
        screen.blit(font.render('LOOSE!!!', False, 'yellow'), (width // 2 - 120, height // 2 - 50))
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
                if y in range(100, 201):
                    for i in range(1, 4):
                        if x in range(i * 120 - 40, i * 120 + 60):
                            if stars['map' + str(i - 1)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i))
                                return 0
                if y in range(200, 301):
                    for i in range(1, 4):
                        if x in range(i * 120 - 40, i * 120 + 60):
                            if stars['map' + str(i + 2)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i + 3))
                                return 0
                if y in range(300, 401):
                    for i in range(1, 4):
                        if x in range(i * 120 - 40, i * 120 + 60):
                            if stars['map' + str(i + 5)] != 0 and energy >= 1 and no_go_shop:
                                energy -= 1
                                reboot()
                                play('map' + str(i + 6))
                                return 0
                if y in range(height - 40, height) and x in range(width - 40, width):
                    restart()
                if x in range(width // 2 - 50, width // 2 + 50) and y in range(height - 50, height - 20) and no_go_shop:
                    no_go_shop = False
                elif x in range(width // 2 - 50, width // 2 + 50) and y in range(height - 50,
                                                                                 height - 20) and not no_go_shop:
                    no_go_shop = True
                elif x in range(width - 45, width - 15) and y in range(3, 33):
                    no_go_shop_money = False
        if no_go_shop and no_go_shop_money:
            fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (600, 600))
            screen.blit(fon, (0, 0))
            font = pygame.font.SysFont('Consolas', 38)

            clock = pygame.time.Clock()
            pygame.draw.rect(screen, 'black', (0, 0, width, 40))
            fon = font.render(str(money), 10, pygame.Color('yellow'))
            screen.blit(fon, (width - (len(str(money)) + 10) * 12, 0))
            font = pygame.font.Font(None, 60)
            screen.blit(font.render('lvl' + str(level), False, 'yellow'), (0, 0))
            en = load_image('энергия.jpg')
            screen.blit(en, en.get_rect().move(width // 2 - 100, 5))
            res = load_image('рестарт.png')
            pygame.draw.rect(screen, 'yellow',
                             (width - 40, height - 40, 40, 40))
            screen.blit(res, en.get_rect().move(width - 40, height - 40))
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
            for i in range(1, 4):
                for j in range(1, 4):
                    num += 1
                    font = pygame.font.SysFont('Consolas', 100)
                    pygame.draw.rect(screen, 'blue',
                                     (j * 120 - 40, i * 120 - 30, 100, 100))
                    screen.blit(font.render(str(num), False, 'black'), (j * 120 - 40, i * 120 - 30))
                    for x in range(1, stars['map' + str(num)] + 1):
                        screen.blit(star, star.get_rect().move(j * 120 - 30 + (x - 1) * 30, i * 120 + 45))
                    if i != 1 or j != 1:
                        if stars['map' + str(num - 1)] == 0:
                            screen.blit(padlock, padlock.get_rect().move(j * 120 - 40, i * 120 - 30))
            image = load_image('обрезанная монета.png', 'black')
            dog_rect = image.get_rect(
                bottomright=(width - 50, image.get_height() + 2))
            screen.blit(image, dog_rect)
            pygame.draw.rect(screen, 'yellow',
                             (width // 2 - 50, height - 50, 100, 30))
            font = pygame.font.Font(None, 35)
            screen.blit(font.render('shop', False, 'black'), (width // 2 - 45, height - 50))

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
            screen.blit(load_image('персонаж 2 для магазина.jpg', -1),
                        load_image('персонаж 2 для магазина.jpg', -1).get_rect().move(width // 2 - 110,
                                                                                      height // 2 - 80))
            pygame.draw.rect(screen, 'black',
                             (width // 2 + 25, height // 2 - 85, 110, 150), 2)
            screen.blit(load_image('персонаж 4 для магазина.png', 'yellow'),
                        load_image('персонаж 4 для магазина.png', 'yellow').get_rect().move(width // 2 + 30,
                                                                                            height // 2 - 80))
            if 'evil' not in my_skin:
                font = pygame.font.Font(None, 70)
                screen.blit(font.render('200', False, 'black'), (width // 2 - 105, height // 2 + 20))
            else:
                font = pygame.font.Font(None, 45)
                screen.blit(font.render('Одеть', False, 'black'), (width // 2 - 105, height // 2 + 20))
            if 'creep' not in my_skin:
                font = pygame.font.Font(None, 70)
                screen.blit(font.render('800', False, 'black'), (width // 2 + 35, height // 2 + 20))
            else:
                font = pygame.font.Font(None, 45)
                screen.blit(font.render('Одеть', False, 'black'), (width // 2 + 35, height // 2 + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y in range(height // 2 - 85, height // 2 + 65):
                    if x in range(width // 2 - 115, width // 2 - 15):
                        if money >= 200 and player_image_num != 1 and 'evil' not in my_skin:
                            money -= 200
                            player_image = load_image('персонаж 2.jpg')
                            player_image_num = 1
                            no_go_shop = True
                            my_skin.append('evil')
                        elif 'evil' in my_skin:
                            player_image = load_image('персонаж 2.jpg')
                            player_image_num = 1
                            no_go_shop = True
                if y in range(height // 2 - 85, height // 2 + 65):
                    if x in range(width // 2 + 25, width // 2 + 135):
                        if money >= 800 and player_image_num != 2 and 'creep' not in my_skin:
                            money -= 800
                            player_image = load_image('персонаж 3.png')
                            player_image_num = 2
                            no_go_shop = True
                            my_skin.append('creep')
                        elif 'creep' in my_skin:
                            player_image = load_image('персонаж 3.png')
                            player_image_num = 2
                            no_go_shop = True
            pygame.display.flip()


monster_group = pygame.sprite.Group()
data = open('regist.csv', encoding='utf-8').read()
for row in data.split('/n'):
    account = row.split(';')
death_music = pygame.mixer.Sound('data/mario_bros_die.mp3')
win_music = pygame.mixer.Sound('data/super-mario-world-death-on-piano.mp3')
money = int(account[1])
experience = float(account[2])
level = int(account[0])
time = timedelta(seconds=10)
last_update = datetime.now()
FPS = 60
clock = pygame.time.Clock()
my_skin = account[3].split()
stars = {'map1': int(account[4]), 'map2': int(account[5]), 'map3': int(account[6]),
         'map4': int(account[7]), 'map5': int(account[8]), 'map6': int(account[9]),
         'map7': int(account[10]), 'map8': int(account[11]),
         'map9': int(account[12]), 'map0': 3
         }
tile_images
if '0' in account[-1]:
    player_image = load_image('куб.jpeg')
    player_image_num = 0
elif '1' in account[-1]:
    player_image = load_image('персонаж 2.jpg')
    player_image_num = 1
else:
    player_image = load_image('персонаж 3.png')
    player_image_num = 2
tile_width = tile_height = 25
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
laser_help_group = pygame.sprite.Group()
star = 0
energy = 5
tile_width = tile_height = 25
start_screen()
menu()
