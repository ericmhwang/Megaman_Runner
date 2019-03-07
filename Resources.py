import pygame, sys, os
from pygame.locals import *


class player():
    def __init__(self, x, y, py):
        self.x = x
        self.y = y
        self.jumping = False
        self.platform_y = py
        self.velocity_index = 0
        self.check = True


    def do_jump(self):
        global velocity

        if self.jumping:
            self.y += velocity[self.velocity_index]
            self.velocity_index += 1
            self.check = True
            if self.velocity_index >= len(velocity) - 1:
                self.velocity_index = len(velocity) - 1
                self.check = False
            if self.y >= self.platform_y:
                self.y = self.platform_y
                self.jumping = False
                self.velocity_index = 0
                self.check = True


def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def keys(player):
    keys = pygame.key.get_pressed()
    if keys[K_UP] and player.jumping == False:
        player.jumping = True


def bg_scrolling(img, ss):
    global bgx
    rel_x = bgx % img.get_rect().width
    screen.blit(img, (rel_x - img.get_rect().width, 100))
    if rel_x < w:
        screen.blit(img, (rel_x, 100))
    bgx -= ss
    return bgx