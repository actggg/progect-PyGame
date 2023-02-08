import pygame

from load_image import load_image

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
