import pygame, os, sys
from pygame.locals import *


_image_library = {}
file_Name = 'score.txt'


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
jumping_image = ['jp1.png', 'jp2.png', 'jp3.png', 'jp4.png', 'jp5.png', 'jp6.png', 'jp7.png', 'jp8.png', 'jp9.png',
                 'jp10.png']
pygame.init()
c=0
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

while True:
    events()
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (128, 0, 128), pygame.Rect(10, 10, 50, 10), 10)
    if c != 9:
        screen.blit(get_image(jumping_image[c]), (10, 10))
        pygame.time.wait(55)
        c +=1
    else:
        screen.blit(get_image(jumping_image[c]), (10, 10))
        pygame.time.wait(55)
        c = 0
    clock.tick(30)
    pygame.display.flip()