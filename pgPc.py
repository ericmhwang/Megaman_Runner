'''
ICS 4U - ISU
Eric Wang, in May 15, 2017
pgPc.py, 'MegaMan VII: Endless Runner'
This program is a mega man-themed endless runner game
'''
# importing all necessary libraries and resources
import pygame, sys, os, random
from pygame.locals import *

# image library that stores the image files that are being loaded within this file
_image_library = {}
hs = 0
file_Name = 'score.txt'

# defining the colour white
WHITE = (255, 255, 255)


# ===========================================================================================
# Functions and Classes Section
# ===========================================================================================


# player class
class player(pygame.sprite.Sprite):
    # initializing all the required elements, including image, sprites, (x,y) positions, delay and hp
    def __init__(self, x, y, py):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('rp1.png')
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y

        # a variable that checks to see if the player is jumping or not
        self.jumping = False

        # a variable that is being used later on to see if the player is on the platform
        self.platform_y = py

        # a variable that is being used later on to apply acceleration while jumping
        self.velocity_index = 0

        # shooting delay to prevent rapid firing
        self.shoot_delay = 100

        # getting the time of pygame's initialization
        self.last_shot = pygame.time.get_ticks()
        self.run_tick = pygame.time.get_ticks()

        # running and jumping frames
        self.running_frame = 0
        self.jumping_frame = 0

        # indicates that the player is alive
        self.living = True
        self.hp = 100

    # a function that changes the player's position and sprites upon user input (key up)
    def do_jump(self):

        # velocity that governs the speed and acceleration of the player while mid air
        global velocity

        # if statement to see if the player is jumping or not
        if self.jumping is True:
            self.rect.bottom += velocity[self.velocity_index]
            self.velocity_index += 1

            # changing the player's y position using the velocity variable
            if self.velocity_index >= len(velocity) - 1:
                self.velocity_index = len(velocity) - 1

            # stopping the jump
            if self.rect.bottom >= self.platform_y:
                self.rect.bottom = self.platform_y
                self.jumping = False
                self.velocity_index = 0

    # update function to continue drawing the sprites of the player
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.run_tick > 55:
            self.run_tick = now

            # drawing running sprites while running
            if self.running_frame < 8 and not self.jumping:
                self.running_frame += 1
                self.image = get_image(running_image[self.running_frame])

            # drawing jumping sprites while jumping
            elif self.jumping_frame < 8 and self.jumping:
                self.jumping_frame += 1
                self.image = get_image(jumping_image[self.jumping_frame])
            elif self.jumping and self.jumping_frame > 8:
                self.image = get_image(jumping_image[9])
            else:
                self.running_frame = 0
                self.jumping_frame = 0
                self.image = get_image(running_image[self.running_frame])

        # if statement to check user input
        if pygame.key.get_pressed()[K_SPACE] and counter < 5:
            self.shooting()
        if pygame.key.get_pressed()[K_UP] and self.jumping is False:
            self.jumping = True
            jump_sound.play()

    # shooting function that adds in player bullets
    def shooting(self):
        global counter
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.y + 30)
            all_sprites.add(bullet)
            bullets.add(bullet)
            counter += 1


# player bullet class
class Bullet(pygame.sprite.Sprite):
    # initializing the bullet as a sprite with all the necessary components
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('b1.png ')
        self.rect = self.image.get_rect()

        # using the current y value of the player and drawing the bullet sprite
        self.rect.bottom = y

        # fixed x position
        self.rect.left = 135

        # speed of the bullet
        self.speedx = 6

        # an index to animate the bullet
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

        # shooting sound effect
        pshooting_sound.play()

    # update function to animate the bullets and continue drawing the bullets
    def update(self):

        # counter to keep track of the number of bullets on screen; max = 5
        global counter

        # bullet movement
        self.rect.x += self.speedx
        now = pygame.time.get_ticks()

        # bullet is removed when it reaches the end of the screen
        if self.rect.left > w:
            self.kill()
            counter -= 1

        # animating bullets
        elif now - self.last_update > 70:
            if self.frame < 7:
                self.last_update = now
                self.frame += 1
                self.image = get_image(bullet_anim[self.frame])
            else:
                self.image = get_image('b9.png')


# the first mob class: does nothing, damages the player if they collide with the player
class mobs1(pygame.sprite.Sprite):
    # initializing the mobs as sprites with all the necessary components
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('m1-1.png')
        self.rect = self.image.get_rect()

        # position of the mob, randomizing the x position
        self.rect.bottom = 406
        self.rect.left = random.randrange(800, 3000, 30)

        # speed of the mobs
        self.speedx = -x

        # index for animation
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    # update function that achieves the same job as the previous classes
    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speedx

        # if the mob goes out of bound without colliding, respawns the mob in a random location
        if self.rect.x < 0:
            self.rect.x = random.randrange(800, 2000, 30)

        # animation
        if now - self.last_update > 200:
            self.last_update = now
            if self.frame < 3:
                self.image = get_image(m1_anim[self.frame])
                self.frame += 1
            elif self.frame == 3:
                self.image = get_image(m1_anim[self.frame])
                self.frame = 1


# the second mob class: flying, shoots bullets horizontally
class mobs2(pygame.sprite.Sprite):
    # initializing the mob as a sprite with all the necessary components
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('m2-1.png')
        self.rect = self.image.get_rect()

        # position of the mob
        self.rect.bottom = 350
        self.rect.left = random.randrange(800, 2000)

        # x and y speed of the mob
        self.speedx = -4
        self.speedy = 2

        # index for animation
        self.frame = 0
        self.frameup = 0

        # a variable to delay the firing of the mob's bullet
        self.bs = 0
        self.last_update = pygame.time.get_ticks()
        self.mvmt = pygame.time.get_ticks()
        self.living = True

    # update function that achieves the same job as the previous classes
    def update(self):
        now = pygame.time.get_ticks()

        # if statement for movement of the mob
        if now - self.mvmt > 30:
            self.mvmt = now
            if self.rect.x > 600:
                self.rect.x += self.speedx
            elif self.rect.x <= 600 and self.rect.y >= 380:
                self.speedy = -2
                self.rect.y += self.speedy
            elif self.rect.x <= 600 and 280 < self.rect.y < 380:
                self.rect.y += self.speedy
            elif self.rect.x <= 600 and self.rect.y <= 280:
                self.speedy = 2
                self.rect.y += self.speedy

        # if statement for animation and the bullet firing
        if now - self.last_update > 100:
            self.last_update = now
            if self.rect.x <= 600:
                if self.frame == 0:
                    self.image = get_image(m2_anim[self.frame])
                    self.frameup = 1
                    self.frame += self.frameup
                elif self.frame < 2:
                    self.image = get_image(m2_anim[self.frame])
                    self.frame += self.frameup
                elif self.frame == 2:
                    self.image = get_image(m2_anim[self.frame])
                    self.frameup = -1
                    self.frame += self.frameup
                    if self.bs == 0 or self.rect.y == 390:
                        self.bs = 5
                        b = Bulletm2(self.rect.left, self.rect.bottom)
                        all_sprites.add(b)
                        hbullets.add(b)
                    else:
                        self.bs -= 1


# missile class
class missile(pygame.sprite.Sprite):
    # initializing the missile as a sprite with all the necessary components
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('missile.png')

        # position
        self.height = random.randrange(390, 350, -1)
        self.xpos = random.randrange(1000, 4000, 10)
        self.rect = self.image.get_rect()
        self.rect.bottom = self.height
        self.rect.left = self.xpos

        # speed of the missile
        self.speedx = -8

        # boolean variables to prevent overlapping of the sound effects
        self.sound1 = True
        self.sound2 = True

    # update function that achieves the same job as the previous classes
    def update(self):
        self.rect.x += self.speedx
        if 800 < self.rect.left <= 1200:

            # warning sign for the missile
            screen.blit(get_image('warning.png'), (760, self.rect.centery - 20))
            if self.sound1:
                # sound effect for missile alert
                alert_sound.play(2)
                self.sound1 = False
        elif 0 <= self.rect.right <= 800:
            if self.sound2:
                # sound effect for the missile
                missile_sound.play()

            # adding the booster of the missile
            fire = missile_trace(self.rect.right, self.rect.centery)
            all_sprites.add(fire)
            self.sound2 = False

        # redrawing the missile if out of bound
        elif self.rect.right < 0:
            self.rect.x = random.randrange(1000, 4000, 10)
            self.rect.y = random.randrange(390, 350, -1)
            self.sound1 = True
            self.sound2 = True


# missile trace class
class missile_trace(pygame.sprite.Sprite):
    # initializing the missile as a sprite with all the necessary components
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('fire1.png')
        self.rect = self.image.get_rect()

        # x and y position obtained from the missile's current location
        self.rect.left = x
        self.rect.centery = y
        self.speedx = -8

        # index for animation of the trace
        self.ii = 0
        self.last_update = pygame.time.get_ticks()

    # another update function for animation
    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speedx
        if now - self.last_update > 200:
            self.last_update = now
            if self.ii < 3:
                self.image = get_image(missile_anim[self.ii])
                self.ii += 1
            elif self.ii >= 3:
                self.image = get_image(missile_anim[3])


# spike class: the player dies right away if collided
class spikes(pygame.sprite.Sprite):
    # initializing the spike as a sprite with all the necessary components
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('spikes1.png')
        self.xpos = random.randrange(1000, 1400, 40)
        self.rect = self.image.get_rect()
        self.rect.bottom = 402
        self.rect.left = self.xpos
        self.speedx = -4

    # another updating for movement
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.rect.x = random.randrange(1000, 1600, 40)


# second mob's bullet class
class Bulletm2(pygame.sprite.Sprite):
    # initializing the bullets as sprites with all the necessary components
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('db1.png')
        self.rect = self.image.get_rect()

        # x and y position obtained from the current coordinate of the second mob
        self.rect.bottom = y
        self.rect.left = x

        # speed of the bullet
        self.speedx = -5

        # index and counters for animation
        self.frame = 0
        self.frameup = 0
        self.last_update = pygame.time.get_ticks()

        # sound effect
        m2shooting_sound.play()

    # yet another update class for animation, and the movement of the bullet
    def update(self):
        self.rect.left += self.speedx
        now = pygame.time.get_ticks()

        # deleting any out of bound bullets
        if self.rect.y >= 412:
            self.kill()

        # you may fire when ready, of course, there is a delay
        elif now - self.last_update > 200:
            self.last_update = now
            if self.frame == 0:
                self.image = get_image(m2b_anim[self.frame])
                self.frameup = 1
                self.frame += self.frameup
            elif self.frame == 1:
                self.image = get_image(m2b_anim[self.frame])
                self.frame += self.frameup
            elif self.frame == 2:
                self.image = get_image(m2b_anim[self.frame])
                self.frameup = -1
                self.frame += self.frameup


# KABOOOM class; this class is called whenever a mob or the player dies
class explosion(pygame.sprite.Sprite):
    # initializing the explosion as sprites with all the necessary components
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('e1.png'), (23, 23))
        self.rect = self.image.get_rect()

        # getting the x and y position from the sprites that are exploding
        self.rect.centerx = x
        self.rect.top = y

        # index for animation
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    # update for animation only
    def update(self):
        now = pygame.time.get_ticks()

        # delay before moving on to the next frame
        if now - self.last_update > 90:
            self.last_update = now
            if self.frame < 16:
                self.image = get_image(ep_anim[self.frame])
                self.frame += 1

            # deletes the explosion sprite after going through all animation images
            elif self.frame == 16:
                self.image = get_image(ep_anim[self.frame])
                self.frame = 0
                self.kill()


# function that checks if the escape button is pressed
def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


# function that safely loads the image and stores it in the library
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


# function that blits the background onto the screen, and loops them whenever it reaches the end
def bg_scrolling(img, ss):
    global bgx
    xval = bgx % img.get_rect().width
    screen.blit(img, (xval - img.get_rect().width, 100))
    if xval < w:
        screen.blit(img, (xval, 100))
    bgx -= ss
    return bgx


# function that detects collisions between the player and other classes, and keep track of the player's health as
# well as the inflicted damage
def collision_detect(class1, class2, dmg):
    if pygame.sprite.spritecollide(class1, class2, True) and class1.living:
        class1.hp -= dmg

        # if your hp reaches 0, you die!
        if class1.hp <= 0:
            all_sprites.add(explosion(class1.rect.centerx, class1.rect.y))
            class1.living = False
            death_sound.play()
            class1.kill()


# a function to draw texts on the screen easily
def draw_text(surf, text, size, x, y):
    # setting the font and rednering them for a better quality
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()

    # x and y position and outputting the text
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Start menu screen
def game_intro():
    intro = True

    # music for the intro section
    intro_sound.play(-1)

    # while loop that waits until the user presses the return button
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if pygame.key.get_pressed()[K_RETURN]:
            intro_sound.stop()
            intro = False

        # drawing images on the screen and the texts to explain the game
        screen.fill((0, 0, 0))
        screen.blit(get_image('introimg.png'), (100, 80))
        draw_text(screen, ":ENDLESS RUNNER", 30, w / 2, 350)
        draw_text(screen, "Instruction: Press Space to Shoot, Press Arrow Up to Jump!", 18, w / 2, 400)
        draw_text(screen, "Press Enter to Start", 30, w / 2, 450)

        # pygame display function to properly display the objects
        pygame.display.flip()
        CLOCK.tick(FPS)


# ======================================================================================================
# Variable and initialization section
# ======================================================================================================

# matches the font name for easier access when writing text
font_name = pygame.font.match_font('arial')

# initializes pygame and the mixer (sound)
pygame.init()
pygame.mixer.init()
CLOCK = pygame.time.Clock()

# first player instance
p = player(100, 402, 402)

# score variable; killing the first mob = +5, killing the flying mob = + 10, every second = +1 pts
score = 0

# calling classes to initialize them
fm = mobs2()  # flying mob
missileVar = missile()  # missile
sp = spikes()  # spikes

# creating empty sprite groups to store all the sprites:

all_sprites = pygame.sprite.Group()  # all sprites list
bullets = pygame.sprite.Group()  # player bullet sprite list
hbullets = pygame.sprite.Group()  # second mob's bullet sprite list
all_enemies = pygame.sprite.Group()  # all enemies (the two mobs) to check the collision
oneshot = pygame.sprite.Group()  # missile and spikes, the player dies instantly
m1 = pygame.sprite.Group()  # two mobs' sprites group to randomize the spawn
m2 = pygame.sprite.Group()

# assigning sprites and adding them into the appropriate lists
for i in range(6):  # 6 mobs allowed for the first mob
    m = mobs1(2)
    all_sprites.add(m)
    all_enemies.add(m)
    m1.add(m)
all_sprites.add(p)
all_sprites.add(fm)
all_sprites.add(missileVar)
all_sprites.add(sp)
oneshot.add(missileVar)
oneshot.add(sp)
m2.add(fm)
all_enemies.add(fm)

# initializing the screen
w, h = 800, 600
screen = pygame.display.set_mode((w, h))

# lists that contain animation image paths

# player's sprite images
running_image = ['rp1.png', 'rp2.png', 'rp3.png', 'rp4.png', 'rp5.png', 'rp6.png', 'rp7.png', 'rp8.png', 'rp9.png',
                 'rp10.png']
jumping_image = ['jp1.png', 'jp2.png', 'jp3.png', 'jp4.png', 'jp5.png', 'jp6.png', 'jp7.png', 'jp8.png', 'jp9.png',
                 'jp10.png']
bullet_anim = ['b2.png', 'b3.png', 'b4.png', 'b5.png', 'b6.png', 'b7.png', 'b8.png', 'b9.png']

# the first mob's animation
m1_anim = ['m1-2.png', 'm1-3.png', 'm1-4.png', 'm1-5.png']

# the second mob's animation
m2_anim = ['m2-1.png', 'm2-2.png', 'm2-3.png', 'm2-4.png']

# bullet animation for the second mob
m2b_anim = ['db1.png', 'db2.png', 'db3.png']

# explosion animation images
ep_anim = ['e1.png', 'e2.png', 'e3.png', 'e4.png', 'e5.png', 'e6.png', 'e7.png', 'e8.png', 'e9.png', 'e10.png',
           'e11.png', 'e12.png', 'e13.png', 'e14.png', 'e15.png', 'e16.png', 'e17.png']

# missile tracing images
missile_anim = ['fire1.png', 'fire2.png', 'fire3.png', 'fire4.png']

# velocity list that contains nothing
velocity = []

# adding decimal values to simulate the gravity
for i in range(0, 35):
    velocity.append((i / 2.0) - 8.5)

# loading music and sound effects, and the background picture
pygame.mixer.music.load('IWBTB OST MEGAMAN.wav')
intro_sound = pygame.mixer.Sound('Mega_Man_7_OST_Stage_Select.wav')
jump_sound = pygame.mixer.Sound('js.wav')
death_sound = pygame.mixer.Sound('deathsound.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pshooting_sound = pygame.mixer.Sound('shoot.wav')
m2shooting_sound = pygame.mixer.Sound('m2shoot.wav')
missile_sound = pygame.mixer.Sound('missilelunch.wav')
alert_sound = pygame.mixer.Sound('alert.wav')
bkgd = get_image("bg.png")
s1 = get_image("s1bg.png")

# Frames per second
FPS = 120

# background scrolling variables
bgx = 0
bgx1 = 0
counter = 0  # bullet
difficulty = 0
mob1speed = 2
running = True
restart = False

# variable for counting the score
scoring = 0

# outputting intro screen
game_intro()

# once the intro is over, it plays the music and goes into the game loop
pygame.mixer.music.play(loops=-1)

# ==============================================================================================
# The game loop
# ==============================================================================================
while running:

    # if the player is alive, initialize objects on screen and checks for collisions
    if p.living:
        now = pygame.time.get_ticks()

        # score count, increases every second
        if now - scoring >= 1000:
            scoring = now
            score += 1

        # event function to check if the exit button is pressed
        events()

        # filling the screen with the colour black
        screen.fill((0, 0, 0))

        # player jump function to make the player jump
        p.do_jump()

        # scrolling background
        rel_x = bgx1 % s1.get_rect().width
        screen.blit(s1, (rel_x - s1.get_rect().width, 100))
        if rel_x < w:
            screen.blit(s1, (rel_x, 100))
        bgx1 -= 3

        # scrolling background using the function
        bg_scrolling(bkgd, 4)

        # all the update functions get updated here
        all_sprites.update()

        # collision check with the player bullets and enemies (first mob)
        if difficulty == 7:
            mob1speed += 1
            difficulty = 0
        hits1 = pygame.sprite.groupcollide(m1, bullets, True, True)
        for hit in hits1:
            difficulty += 1
            # respawns the mob
            m = mobs1(mob1speed)

            # increases the score
            score += 5

            # explosion sound effect
            explosion_sound.play()

            # calling explosion class and adding it to the all sprites list
            expl = explosion(hit.rect.x, hit.rect.y - 10)
            all_sprites.add(expl)
            all_sprites.add(m)
            all_enemies.add(m)
            m1.add(m)

            # subtraction needed to keep the bullet limit
            counter -= 1

        # collision check with the player bullets and enemies (second mob), same as above
        hits2 = pygame.sprite.groupcollide(m2, bullets, True, True)
        for hita in hits2:
            expl = explosion(hita.rect.x, hita.rect.y)
            m = mobs2()
            score += 10
            explosion_sound.play()
            all_sprites.add(m)
            all_sprites.add(expl)
            all_enemies.add(m)
            m2.add(m)
            counter -= 1

        # collision detection with the player and the obstacles and mobs
        collision_detect(p, all_enemies, 20)
        collision_detect(p, hbullets, 30)
        collision_detect(p, oneshot, 100)

        # drawing all the sprites onto the screen
        all_sprites.draw(screen)

        # outputting the score and the health
        draw_text(screen, "Score:" + str(score), 20, w / 2, 10)
        draw_text(screen, "Health:" + str(p.hp), 20, 200, 10)
        draw_text(screen, "Current High: " + str(hs), 20, 650, 10)

    # if the player is dead, outputs the game over screen.
    elif not p.living and not restart:
        events()
        screen.blit(get_image('go.png'), (200, 200))

        # restarting if the user inputs r
        draw_text(screen, "Press r to restart", 25, w / 2, 405)
        draw_text(screen, "Score: " + str(score), 40, w / 2, 440)
        if pygame.key.get_pressed()[K_r]:
            restart = True
            if hs < score:
                hs = score
    # reinitializing the values
    elif not p.living and restart:
        p.living = True
        p.hp = 100
        score = 0
        counter = 0
        difficulty = 0
        mob1speed = 2
        fm = mobs2()  # flying mob
        missileVar = missile()  # missile
        sp = spikes()  # spikes

        # emptying the sprite group and reinputting the sprites
        all_sprites.empty()
        all_enemies.empty()
        bullets.empty()
        hbullets.empty()
        oneshot.empty()
        m1.empty()
        m2.empty()

        # reinput
        for i in range(6):
            m = mobs1(2)
            all_sprites.add(m)
            all_enemies.add(m)
            m1.add(m)
        all_sprites.add(p)
        all_sprites.add(fm)
        all_sprites.add(missileVar)
        all_sprites.add(sp)
        oneshot.add(missileVar)
        oneshot.add(sp)
        m2.add(fm)
        all_enemies.add(fm)
        restart = False
    pygame.display.flip()
    CLOCK.tick(FPS)
