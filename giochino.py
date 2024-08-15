# IMPORTS
import pygame
import random

# IMPORTO DALLE COSTANTI DI PYGAME da usare come ALIAS/SHORTCUT
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


# INIZIALIZZO
pygame.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf=pygame.Surface((20,10))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect(
            center=
            (
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT),
            )
        )
        self.speed=random.randint(5,20)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Explosion, self).__init__()
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100)).convert()
            self.images.append(img)
        self.index = 0
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.surf = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.index = 0
            self.counter = 0
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf=pygame.image.load("img/player.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        # self.surf=pygame.Surface((75,25))
        # self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()

    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        # KEEP PLAYER ON THE SCREEN
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>SCREEN_WIDTH:
            self.rect.right=SCREEN_WIDTH
        if self.rect.top<=0:
            self.rect.top=0
        if self.rect.bottom>SCREEN_HEIGHT:
            self.rect.bottom=SCREEN_HEIGHT
        

# DEFINISCO VARIABILI
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# CREO LO SCREEN
# crea una surface di 800x600
# NB - la doppia parentesi indica una LISTA

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Crate a custom event for adding a new enemy
ADDENEMY=pygame.USEREVENT+1
pygame.time.set_timer(ADDENEMY,250)

player=Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies=pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
all_sprites=pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True
collision_timer = 0

# Setup the clock for a decent framerate
clock=pygame.time.Clock()

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
        elif event.type==ADDENEMY:
            # create the new enemy and add it to the sprite groups
            new_enemy=Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys=pygame.key.get_pressed() #restituisce un dict con tutti i tasti premuti nella coda degli eventi)
    player.update(pressed_keys)
    enemies.update()
    explosion_group.update()

    # Fill the screen with black
    screen.fill((0,0,0))

    # Draw all spirites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # check if any enemy had collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        pos = player.rect.center
        player.kill()
        explosion = Explosion(pos[0], pos[1])
        explosion_group.add(explosion)
        all_sprites.add(explosion)
        collision_timer = 20

    if collision_timer > 0:
        collision_timer -= 1
    
    if collision_timer == 1:
        running = False

    # # Create a surface and pass in a tuple containing its length and width
    # surf = pygame.Surface((50, 50))

    # # Give the surface a color to separate it from the background
    # surf.fill((0, 0, 0))
    # rect = surf.get_rect()

    # surf_center = (
    #     (SCREEN_WIDTH-surf.get_width())/2,
    #     (SCREEN_HEIGHT-surf.get_height())/2
    # )
    
    # # This line says "Draw surf onto the screen at the center"
    # screen.blit(player.surf,player.rect) #COSA copiare e DOVE copiarla (il suo punto TopLeft)
    pygame.display.flip()
    clock.tick(30)

