import sys
import pygame
import os

fail = input()
fullname = os.path.join('pillow', fail)
if not os.path.isfile(fullname):
    print(f'Файл {fullname}, не найден')
    sys.exit()
pygame.init()
FPS = 50
size = width, height = 650, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def load_image(name, colorkey=None):
    fullname = os.path.join('pillow', name)
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
    fon = pygame.transform.scale(load_image('фон.jpg', 'white'), (650, 650))
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
    filename = "pillow/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'wall': load_image('текстуры.webp'),
    'empty': load_image('пустые поля.webp'),
    'exit': load_image('сундук1.png')
}
player_image = load_image('герой.png')

tile_width = tile_height = 50


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target, x, y):
        self.dx = -x
        self.dy = -y

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def go(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(1, len(level) + 1):
        for x in range(1, len(level[y - 1]) + 1):
            if level[y-1][x-1] == '.':
                Tile('empty', x-1, y-1)
            elif level[y-1][x-1] == '#':
                Tile('wall', x-1, y-1)
            elif level[y-1][x-1] == 'x':
                Tile('exit', x-1, y-1)
            elif level[y-1][x-1] == '@':
                Tile('empty', x-1, y-1)
                new_player = Player(x-1, y-1)
    return new_player, x, y

def rework_lvl(filename, do):
    filename = "pillow/" + filename
    # читаем уровень, убирая символы перевода строки

    if do == 'up':
        with open(filename, 'r', encoding='utf-8') as mapFile:
            data = mapFile.readlines()

        with open(filename, 'w', encoding='utf-8') as mapFile:
            for line in data[1:]:
                mapFile.write(line)
            mapFile.write(data[0])
pygame.display.set_caption('Перемещение героя')
running = True
screen.fill(pygame.Color('black'))
camera = Camera()
start_screen()
level_map = load_level(fail)
player, level_x, level_y = generate_level(load_level(fail))
camera_x, camera_y = 0, 0
while running:
    screen.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            x, y = player.pos
            if event.key == pygame.K_UP:
                if y + camera_y > 0 and level_map[y - 1 + camera_y][x + camera_x] != '#':
                    camera_y -= 1
                    camera.update(player, 0, -50)
                    for sprite in all_sprites:
                        camera.apply(sprite)
            if event.key == pygame.K_DOWN:
                if y + camera_y < level_y and level_map[y + 1 + camera_y][x + camera_x] != '#':
                    camera_y += 1
                    camera.update(player, 0, 50)
                    for sprite in all_sprites:
                        camera.apply(sprite)
            if event.key == pygame.K_LEFT:
                if x + camera_x > 0 and level_map[y + camera_y][x - 1 + camera_x] != '#':
                    camera_x -= 1
                    camera.update(player, -50, 0)
                    for sprite in all_sprites:
                        camera.apply(sprite)
            if event.key == pygame.K_RIGHT:
                if x + camera_x < level_x and level_map[y + camera_y][x + camera_x + 1] != '#':
                    camera_x += 1
                    camera.update(player, 50, 0)
                    for sprite in all_sprites:
                        camera.apply(sprite)
                print(y + camera_y, x + camera_x)
            print(y + camera_y, x + camera_x)
    #camera.update(player)
    # обновляем положение всех спрайтов
    #for sprite in all_sprites:
        #camera.apply(sprite)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()