import pygame
import os
import sys
import config
import action



pygame.init()
screen = pygame.display.set_mode((config.screen_width,config.screen_height))
pygame.display.set_caption("Brick Breaker")

BACKGROUND = pygame.image.load(os.path.join("assets/Background/background.png"))
BAR = pygame.image.load(os.path.join("assets/Bar/bar.png"))
BALL = pygame.image.load(os.path.join("assets/Ball/ball.png"))
TILE = [
    pygame.image.load(os.path.join("assets/Tiles/tile1.png")),
    pygame.image.load(os.path.join("assets/Tiles/tile2.png"))
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
        self.speed_x = 10
        self.speed_y = -10
        self.offset_x = 18
        self.offset_y = 18
        self.rect.x = config.screen_width / 2 - (self.offset_x/2)
        self.rect.y = 500 - (self.offset_y/2)
        self.float_x = self.rect.x
        self.float_y = self.rect.y
        self.player_pos = pygame.math.Vector2(self.rect.x,self.rect.y)
        self.previous_rect = self.rect.copy()
        self.step = 1
    def update(self):
        self.player_pos = pygame.math.Vector2(self.rect.x,self.rect.y)
        if self.rect.x <= 0:
            self.speed_x = abs(self.speed_x)
        if self.rect.x >= config.screen_width - self.offset_x:
            self.speed_x = -abs(self.speed_x)
        if self.rect.y <= 0:
            self.speed_y = abs(self.speed_y)
        if self.rect.y >= config.screen_height - self.offset_y:
            self.speed_y = -abs(self.speed_y)
        
        self.previous_rect = self.rect.copy()
        
        self.step = int((max(abs(self.speed_x),abs(self.speed_y)))/10)
        if self.step == 0:
            self.step = 1
        self.float_x += self.speed_x / self.step
        self.float_y += self.speed_y / self.step
        self.rect.x = self.float_x
        self.rect.y = self.float_y
            
        
        

        

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
        self.rect.x = config.screen_width / 2 - (self.offset_x/2)
        self.rect.y = 600 - (self.offset_y/2)
        self.speed = 15
    def update(self,userinput):
        if userinput[pygame.K_LEFT] and not userinput[pygame.K_RIGHT]:
            self.rect.x -= self.speed
        if userinput[pygame.K_RIGHT] and not userinput[pygame.K_LEFT]:
            self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= config.screen_width - self.offset_x:
            self.rect.x = config.screen_width - self.offset_x
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
    clock = pygame.time.Clock()
    ball1 = ball(BALL)
    background1 = background(BACKGROUND)
    bar1 = bar(BAR)
    
    
    while config.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.run = False
        
                
        background1.draw(screen)
        userinput = pygame.key.get_pressed()
        
        ball1.draw(screen)
        bar1.draw(screen)
        bar1.update(userinput)
        
        config.tiles = action.tile_generation(config.tiles,tile,TILE,config.tile_amount)
        
        if action.circle_rect_collide(ball1.rect.center,ball1.offset_x/2,bar1.rect):
            ball1.speed_x,ball1.speed_y = action.collision(ball1,bar1)
            
        ball1.update()
        action.tile_action(ball1,config.tiles,screen)
        screen.blit(config.score_text,(990,650))
    
        
        pygame.display.update()
        
        if not config.has_initialized:
            pygame.time.wait(2000)
            config.has_initialized = True
        
        clock.tick(60)   
    pygame.quit()
    sys.exit()


def menu(): 
    config.run = True
    while config.run:
        screen.fill((195,131,179))
        screen.blit(config.menu_text,config.menu_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.run = False
            if event.type == pygame.KEYDOWN:
                pygame.time.wait(500)
                main()
    
    
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    menu()