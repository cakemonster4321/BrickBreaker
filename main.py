import pygame
import os
import sys
import config
import action



pygame.init()
screen = pygame.display.set_mode((config.screen_width,config.screen_height))
pygame.display.set_caption("Brick Breaker")

BACKGROUND = pygame.image.load(os.path.join("assets/Background/background.png")).convert_alpha()
BAR = [
    pygame.image.load(os.path.join("assets/Bar/bar.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Bar/longbar.png")).convert_alpha()
]
BALL = [
    pygame.image.load(os.path.join("assets/Ball/normal_ball.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Ball/red_ball.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Ball/purple_ball.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Ball/green_ball.png")).convert_alpha()
]
TILE = [
    pygame.image.load(os.path.join("assets/Tiles/normal_tile1.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/normal_tile2.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/normal_tile3.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/normal_tile4.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/normal_tile5.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/heal_tile.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/new_ball_tile.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/explode_tile.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/longbar_tile.png")).convert_alpha()

]
HEALTH = [
    pygame.image.load(os.path.join("assets/Health/full_heart.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Health/half_heart.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Health/empty_heart.png")).convert_alpha()
]
PROJECTILE = [
    pygame.image.load(os.path.join("assets/Other/health_projectile.png")).convert_alpha(), 
    pygame.image.load(os.path.join("assets/Other/bar_projectile.png")).convert_alpha()
]

class GameObject:
    
    def __init__(self,image):
        self.image = image
        assert isinstance(self.image, pygame.Surface)
        self.rect = self.image.get_rect()
        
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        
        

class Ball(GameObject):
    def __init__(self,image,x_pos,y_pos,speed_x,speed_y,if_original):   
        super().__init__(image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.offset_x = image.get_width()
        self.offset_y = image.get_height()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.previous_rect = self.rect.copy()
        self.original_ball = if_original
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
    def __init__(self,image,x_pos,y_pos,type):
        super().__init__(image)
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.type = type
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        

class bar(GameObject):
    def __init__(self,image):
        super().__init__(image)
        self.offset_x = self.image.get_width()
        self.offset_y = self.image.get_height()
        self.rect.x = config.screen_width / 2 - (self.offset_x/2)
        self.rect.y = 600 - (self.offset_y/2)
        self.speed = 10
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
            
        if self.current_hp <= 0 and config.main_run:
            print(self.current_hp)
            action.game_stat_end()
            
class Projectile(GameObject):
    def __init__(self,image,pos_x,pos_y,speed_x,speed_y,type):
        super().__init__(image)
        self.image = image
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.type = type
    def update(self,bar_rect,health_obj,bar):
        if self.rect.colliderect(bar_rect):
            if self.type == "heal":
                if health_obj.current_hp >= health_obj.full_hp:
                    health_obj.current_hp = health_obj.current_hp
                else: 
                    health_obj.current_hp += 1
                config.projectiles.remove(self)
        
            if self.type == "longbar":
                config.long_bar = True
                config.projectiles.remove(self)
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
            
        
        
            
    
def main():
    clock = pygame.time.Clock()
    bar1 = bar(BAR[0])
    config.balls.append(action.add_balls(BALL[0],Ball,bar1.rect.center[0]-BALL[0].get_width()/2,550 - BALL[0].get_height()/2, 0, 0,True))
    background1 = background(BACKGROUND)
    health1 = health()
    config.points = 0
    config.has_initialized = True
    
    while config.main_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.main_run = False
                config.menu_run = False
        

        background1.draw(screen)
        userinput = pygame.key.get_pressed()
        action.shoot_ball(userinput)
        config.tiles = action.tile_generation(config.tiles,tile,TILE,screen)
        
        for ball in config.balls:
            ball.draw(screen)
            ball.update()
                
            if action.circle_rect_collide(ball.rect.center,ball.offset_x/2,bar1.rect):
                print("yes")
                print(ball.rect)
                ball.speed_x,ball.speed_y = action.collision(ball,bar1)
            
            action.delete_balls(ball,health1)
            action.tile_action(ball,config.tiles,Projectile,Ball,BALL,PROJECTILE[0],PROJECTILE[1])
        action.projectile_update(screen,bar1.rect,health1,bar1)
        health1.update(screen)
        action.draw_tiles(screen)   
        bar1.draw(screen)
        bar1.update(userinput)
        
        if config.to_add:
            config.balls.extend(config.to_add)
            config.to_add.clear()
        
        action.long_bar(bar1,BAR[0],BAR[1])

        
        action.refill_ball(BALL,Ball,bar1)
        
        action.draw_score(screen)
        
        action.get_fps(clock,screen)

        pygame.display.update()
        
        clock.tick(120)   
    


def menu(): 
    config.menu_run = True
    while config.menu_run:
        screen.fill((203,189,173))
        screen.blit(config.logo_menu_text,config.logo_menu_rect)
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
            screen.fill((0,0,0))
            screen.blit(config.end_menu_text1,config.end_text_rect1)
            screen.blit(config.end_menu_text2,config.end_text_rect2)
            action.draw_total_score(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.main_run = False
                    config.menu_run = False
                if event.type == pygame.KEYDOWN:
                    pygame.time.wait(200)
                    config.main_run = True
                    break
        
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    menu()