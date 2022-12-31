import sys
import pygame
import os

pygame.init()
FPS = 50
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

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
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'wall': load_image('кирпичи.jpg'),
    'empty': load_image('земля.jpeg'),
    'coin': load_image('монета.jpg'),
    'exit': load_image('сундук1.png', -1)
}
player_image = load_image('герой (4).png')

tile_width = tile_height = 50


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

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 10,
                                               tile_height * self.pos[1] + 10)

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()

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
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y

pygame.display.set_caption('Перемещение героя')
running = True
start_screen()
level_map = load_level('map.txt')
player, level_x, level_y = generate_level(load_level('map.txt'))
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
                            pygame.sprite.spritecollideany(player, money_group).kill()
            if event.key == pygame.K_DOWN:
                if y < level_y - 1 and level_map[y + 1][x] != '#':
                    while level_map[y + 1][x] != '#':
                        x, y = x, y + 1
                        player.go(x, y)
                        if pygame.sprite.spritecollideany(player, money_group):
                            pygame.sprite.spritecollideany(player, money_group).kill()
            if event.key == pygame.K_LEFT:
                if x > 0 and level_map[y][x - 1] != '#':
                    while level_map[y][x - 1] != '#':
                        x, y = x - 1, y
                        player.go(x, y)
                        if pygame.sprite.spritecollideany(player, money_group):
                            pygame.sprite.spritecollideany(player, money_group).kill()
            if event.key == pygame.K_RIGHT:
                if x < level_x - 1 and level_map[y][x + 1] != '#':
                    while level_map[y][x + 1] != '#':
                        x, y = x + 1, y
                        player.go(x, y)
                        if pygame.sprite.spritecollideany(player, money_group):
                            pygame.sprite.spritecollideany(player, money_group).kill()
                        #if level_map[y][x] == '+':

            #if level_map[y][x] == 'x':
                #player.kill()
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()