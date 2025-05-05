import pygame
import os
import sys
import config
import action



pygame.init()
screen = pygame.display.set_mode((config.screen_width,config.screen_height))
pygame.display.set_caption("Brick Breaker")

BACKGROUND = pygame.image.load(os.path.join("assets/Background/background.png")).convert_alpha()
BAR = pygame.image.load(os.path.join("assets/Bar/bar.png")).convert_alpha()
BALL = pygame.image.load(os.path.join("assets/Ball/normal_ball.png")).convert_alpha()
TILE = [
    pygame.image.load(os.path.join("assets/Tiles/tile1.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/tile2.png")).convert_alpha()
]
HEALTH = [
    pygame.image.load(os.path.join("assets/Health/full_heart.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Health/half_heart.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Health/empty_heart.png")).convert_alpha()
]
class GameObject:
    
    def __init__(self,image):
        self.image = image
        assert isinstance(self.image, pygame.Surface)
        self.rect = self.image.get_rect()
        
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        
        

class Ball(GameObject):
    def __init__(self,image,x_pos,y_pos,speed_x,speed_y):   
        super().__init__(image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.offset_x = 18
        self.offset_y = 18
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.previous_rect = self.rect.copy()
    def update(self):
        if self.rect.x <= 0:
            self.speed_x = abs(self.speed_x)
        if self.rect.x >= config.screen_width - self.offset_x:
            self.speed_x = -abs(self.speed_x)
        if self.rect.y <= 0:
            self.speed_y = abs(self.speed_y)

        
        self.previous_rect = self.rect.copy()
        
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
 
class health:
    def __init__(self):
        self.image = HEALTH[0] 
        assert isinstance(self.image, pygame.Surface)   
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 640
        self.full_image = HEALTH[0] 
        self.half_image = HEALTH[1] 
        self.empty_image = HEALTH[2]
        self.full_hp = 10
        self.current_hp = self.full_hp
        self.lost_hp = 0
        self.half_heart_count = 0                
        self.empty_heart_count = 0                    
        self.full_heart_count = int(self.current_hp / 2)
    def update(self,screen):
        self.rect.x = 10
        self.right_end = self.rect.x
        self.lost_hp = self.full_hp - self.current_hp
        self.full_heart_count = int(self.current_hp / 2)
        self.empty_heart_count = int(int(self.lost_hp)/2)
        
        if self.current_hp != 0 and self.current_hp % 2 == 1:
            self.half_heart_count = 1
        else:
            self.half_heart_count = 0    
                        
        for _ in range(0,self.full_heart_count):
            screen.blit(self.full_image,(self.right_end,self.rect.y))
            self.right_end += self.rect.width*2/3
        if self.half_heart_count == 1:
            screen.blit(self.half_image,(self.right_end,self.rect.y))
            self.right_end += self.rect.width*2/3
        for _ in range(0,self.empty_heart_count):
            screen.blit(self.empty_image,(self.right_end,self.rect.y))
            self.right_end += self.rect.width*2/3              
            
        if self.current_hp == 0:
            config.main_run = False
            config.tiles.clear()
def main():
    clock = pygame.time.Clock()
    config.balls.append(action.add_balls(BALL,Ball,config.screen_width / 2 - 9,500 - 9, config.ballspeed_x, config.ballspeed_y))
    bar1 = bar(BAR)
    background1 = background(BACKGROUND)
    health1 = health()
    count =0
    
    while config.main_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.main_run = False
                config.menu_run = False
        

        background1.draw(screen)
        userinput = pygame.key.get_pressed()
        
        config.tiles = action.tile_generation(config.tiles,tile,TILE,config.tile_amount)
        
        for ball in config.balls:
            ball.draw(screen)
            ball.update()
                
            if action.circle_rect_collide(ball.rect.center,ball.offset_x/2,bar1.rect):
                print("yes")
                print(ball.rect)
                ball.speed_x,ball.speed_y = action.collision(ball,bar1)
            
            action.delete_balls(ball,health1)
            action.tile_action(ball,config.tiles,Ball,BALL)
            
                
        health1.update(screen)
        action.draw_tiles(screen)   
        bar1.draw(screen)
        bar1.update(userinput)
        
        if config.to_add:
            
            config.balls.extend(config.to_add)
            config.to_add.clear()
        
        
        screen.blit(config.score_text,(990,650))
        
        fps = clock.get_fps()
        fps_text = config.font.render(f"FPS: {fps:.2f}", False, (255, 255, 255))
        screen.blit(fps_text, (800, 650))
        
        
        pygame.display.update()
        
        if not config.has_initialized:
            pygame.time.wait(1500)
            config.has_initialized = True
        
        clock.tick(60)   
    


def menu(): 
    config.menu_run = True
    while config.menu_run:
        screen.fill((195,131,179))
        screen.blit(config.start_menu_text,config.start_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.main_run = False
                config.menu_run = False
            if event.type == pygame.KEYDOWN:
                pygame.time.wait(200)
                main()
        
        while config.menu_run == True and config.main_run == False:
            screen.fill((162,177,255))
            screen.blit(config.end_menu_text1,config.end_text_rect1)
            screen.blit(config.end_menu_text2,config.end_text_rect2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.main_run = False
                    config.menu_run = False
                if event.type == pygame.KEYDOWN:
                    pygame.time.wait(200)
                    config.main_run = True
                    print("yes")
                    break
        
        
        
    
    
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    menu()