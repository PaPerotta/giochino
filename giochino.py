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
pygame.font.init()

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

# Definisco variabili per gestire lo score
score = 0
score_increment = 1

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
all_sprites=pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Setup the clock for a decent framerate
clock=pygame.time.Clock()

# Set up the font object
font = pygame.font.Font(None, 24)

# Main loop
while running:
    score += score_increment
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

    # Fill the screen with black
    screen.fill((0,0,0))

    # Draw all spirites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # check if any enemy had collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running=False

    # Draw the score to the screen
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (700, 10))
    
    # # This line says "Draw surf onto the screen at the center"
    # screen.blit(player.surf,player.rect) #COSA copiare e DOVE copiarla (il suo punto TopLeft)
    pygame.display.flip()
    clock.tick(30)

