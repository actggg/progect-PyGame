import sys
import pygame
import os


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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)
    red_rocket = load_image('новая_ракета.DNOoL.png', colorkey= (255, 255, 255))
    blue_rocket = load_image('синяя_ракета_без_фона.YwOeA.png', colorkey=(255, 255, 255))
    rect = red_rocket.get_rect()
    clock = pygame.time.Clock()
    running = True
    direction = 'number_1'
    fps = 200
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 20, 30))
        pygame.draw.rect(screen, 'gray', (0, height - 100, width, 100))
        pygame.draw.rect(screen, 'red', (20, height - 80, 130, 60))
        pygame.draw.rect(screen, 'blue', (width - 150, height - 80, 130, 60))
        font = pygame.font.Font(None, 60)
        screen.blit(font.render('A', False, 'black'), (70, height - 75))
        screen.blit(font.render('L', False, 'black'), (805, height - 75))
        if count == width - (30 + rect.width):
            direction = 'number_2'
        if count == 30:
            direction = 'number_1'
        if direction == 'number_1':
            count += 1
        else:
            count -= 1
        screen.blit(red_rocket, (0 + count, 360))
        screen.blit(blue_rocket, (width - rect.width - count, 10))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()