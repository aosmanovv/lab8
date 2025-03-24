#Imports
import pygame, sys
import random
from pygame.locals import *
import random, time

#Initialzing
pygame.init()

#Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
LEVEL = 1
SCORE = 30

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


#Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")
class Block(pygame.sprite.Sprite):
    def __init__(self,x=-40,y=-40,color=WHITE ):
        super().__init__()
        self.x=x
        self.y=y
        self.color=color
        self.rect = pygame.Rect(self.x,self.y,40,40)
        self.rect.topleft = (x, y)
    def newPos(self,a,b):
        self.x=a
        self.y=b
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        #print("draw")
        pygame.draw.rect(DISPLAYSURF, self.color, pygame.Rect(self.x+1, self.y+1, 38, 38))


class Player(pygame.sprite.Sprite):
    def __init__(self,x=200,y=200,color=(255,255,0)):
        super().__init__()
        self.dir=0
        self.x=x
        self.y=y
        self.rect = pygame.Rect(self.x,self.y,40,40)
        self.rect.topleft = (x, y)
        self.color=color
    def newPos(self,a,b):
        self.x=a
        self.y=b
        self.rect.topleft = (self.x, self.y)

    def direction(self):
        pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_UP]:
        #self.rect.move_ip(0, -5)
        #if pressed_keys[K_DOWN]:
        #self.rect.move_ip(0,5)

        if pressed_keys[K_LEFT] and self.dir!=1:
            self.dir=3
        if pressed_keys[K_UP] and self.dir!=2:
            self.dir=0
        if pressed_keys[K_RIGHT] and self.dir!=3:
            self.dir=1
        if pressed_keys[K_DOWN] and self.dir!=0:
            self.dir=2
        print(self.dir)
    def draw(self):
        #print("draw")
        pygame.draw.rect(DISPLAYSURF, self.color, pygame.Rect(self.x+1, self.y+1, 38, 38))

#Setting up Sprites
P1 = Player(200,200,WHITE)

F1 = Block(240,240,RED)

#Creating Sprites Groups
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
food = pygame.sprite.Group()
players = pygame.sprite.Group()
blocks_list=[]

players.add(P1)
all_sprites.add(P1)
food.add(F1)
all_sprites.add(F1)


#Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
STEP = pygame.USEREVENT + 1
pygame.time.set_timer(STEP, max(1000-LEVEL*70,300))

#Game Loop
while True:

    #Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == STEP:

            for i in range(len(blocks_list)-1,0,-1):
                blocks_list[i].newPos(blocks_list[i-1].x,blocks_list[i-1].y)
                print(blocks_list[i].rect)
            if (len(blocks_list)>0):
                blocks_list[0].newPos(P1.x,P1.y)
            if (P1.dir==0):
                P1.newPos(P1.x,P1.y-40)
            if (P1.dir==1):
                P1.newPos(P1.x+40,P1.y)
            if (P1.dir==2):
                P1.newPos(P1.x,P1.y+40)
            if (P1.dir==3):
                P1.newPos(P1.x-40,P1.y)








    #Moves and Re-draws all Sprites
    P1.direction()


    #To be run if collision occurs between Player and Enemy
    print(blocks_list)
    if pygame.sprite.spritecollideany(P1, food):
        #print("loll")
        SCORE+=1
        LEVEL=int(SCORE/4+1)
        pygame.time.set_timer(STEP, max(1000-(LEVEL*90),100))
        new_block=Block()
        blocks.add(new_block)
        all_sprites.add(new_block)
        blocks_list=blocks_list+[new_block]
        for sprite in food:
            while pygame.sprite.spritecollide(sprite, players ,False) or pygame.sprite.spritecollideany(P1, blocks):
                sprite.newPos(random.randint(0,9)*40,random.randint(0,9)*40)

    if pygame.sprite.spritecollideany(P1, blocks) or P1.x>380 or P1.x<0 or P1.y>380 or P1.y<0:
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (10,200))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    #coins-player collision
    """if pygame.sprite.spritecollideany(P1, coins):
        COINS+=1
        ColCoins=pygame.sprite.spritecollide(P1,coins,False)
        for i in ColCoins:
            i.move()"""


    DISPLAYSURF.fill(BLACK)
    scores = font_small.render(str(SCORE), True, WHITE)
    level = font_small.render(str(LEVEL), True, WHITE)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(level, (SCREEN_WIDTH-20,10))

    for entity in all_sprites:
        #print(entity.rect)
        entity.draw()
    pygame.display.update()
    FramePerSec.tick(FPS)
