import pygame
import os
import sys
import random
from action import collision,tile_generation



pygame.init()
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Brick Breaker")

BACKGROUND = pygame.image.load(os.path.join("assets/background.png"))
BAR = pygame.image.load(os.path.join("assets/bar.png"))
BALL = pygame.image.load(os.path.join("assets/ball.png"))
TILE = [
    pygame.image.load(os.path.join("assets/tile1.png")),
    pygame.image.load(os.path.join("assets/tile2.png"))
]
class GameObject:
    
    def __init__(self,image):
        self.image = image
        assert isinstance(self.image, pygame.Surface)
        self.rect = self.image.get_rect()
        
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        
        

class ball(GameObject):
    def __init__(self,image):   
        super().__init__(image)
        self.speed_x = 5
        self.speed_y = -15
        self.offset_x = 20
        self.offset_y = 20
        self.rect.x = screen_width / 2 - (self.offset_x/2)
        self.rect.y = 600 - (self.offset_y/2)
        self.player_pos = pygame.math.Vector2(self.rect.x,self.rect.y)
    def update(self):
        self.player_pos = pygame.math.Vector2(self.rect.x,self.rect.y)
        if self.rect.x <= 0:
            self.speed_x = abs(self.speed_x)
        if self.rect.x >= screen_width - self.offset_x:
            self.speed_x = -abs(self.speed_x)
        if self.rect.y <= 0:
            self.speed_y = abs(self.speed_y)
        if self.rect.y >= screen_height - self.offset_y:
            self.speed_y = -abs(self.speed_y)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
            
        
        

        

class tile(GameObject):
    def __init__(self,image,x_pos,y_pos):
        super().__init__(image)
        self.rect.x = x_pos
        self.rect.y = y_pos
    
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        

class bar(GameObject):
    def __init__(self,image):
        super().__init__(image)
        self.offset_x = 86
        self.offset_y = 16
        self.rect.x = screen_width / 2 - (self.offset_x/2)
        self.rect.y = 600 - (self.offset_y/2)
        self.speed = 10
    def update(self,userinput):
        if userinput[pygame.K_LEFT] and not userinput[pygame.K_RIGHT]:
            self.rect.x -= self.speed
        if userinput[pygame.K_RIGHT] and not userinput[pygame.K_LEFT]:
            self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= screen_width - self.offset_x:
            self.rect.x = screen_width - self.offset_x
    def draw(self,screen):
            screen.blit(self.image,(self.rect.x,self.rect.y))

class background:
    x = 0
    y = 0
    def __init__(self,image):
            self.x = self.x
            self.y = self.y
            self.image = image
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
    
def main():
    global points, death_count,gamespeed,tiles,tile_x_pos,tile_y_pos
    run = True
    clock = pygame.time.Clock()
    tiles = []
    gamespeed = 15
    font = pygame.font.Font(os.path.join("assets/font", "ARCADECLASSIC.TTF"), 30)
    tile_x_pos = 0
    tile_y_pos = 0
    background1 = background(BACKGROUND)
    ball1 = ball(BALL)
    bar1 = bar(BAR)
    tile_amount = 240
    
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        background1.draw(screen)
        userinput = pygame.key.get_pressed()
        tiles = tile_generation(tiles,tile,TILE,tile_x_pos,tile_y_pos,tile_amount)
        
        for tile_piece in tiles:
            if ball1.rect.colliderect(tile_piece):
                ball1.speed_x,ball1.speed_y = collision(ball1,tile_piece)
            tile_piece.draw(screen)

        
        ball1.draw(screen)
        bar1.draw(screen)
        
        if ball1.rect.colliderect(bar1.rect):
            ball1.speed_x,ball1.speed_y = collision(ball1,bar1)
            
        
        ball1.update()
        bar1.update(userinput)
        
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()


# def score()
def menu(): 
    pass

if __name__ == "__main__":
    main()
