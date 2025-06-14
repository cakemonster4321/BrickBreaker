import pygame
import os
import sys
import config
import action


# 初始化 pygame 套件，然後建立遊戲視窗、標題、背景等
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
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
    pygame.image.load(os.path.join("assets/Tiles/longbar_tile.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/tile_hit.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets/Tiles/tile_hit1.png")).convert_alpha()
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
AUDIO = [
    pygame.mixer.Sound(os.path.join("assets/Audio/Normal_tile.wav")),
    pygame.mixer.Sound(os.path.join("assets/Audio/border.wav")),
    pygame.mixer.Sound(os.path.join("assets/Audio/heal.wav")),
    pygame.mixer.Sound(os.path.join("assets/Audio/round.wav")),
    pygame.mixer.Sound(os.path.join("assets/Audio/lost.wav")),
    pygame.mixer.Sound(os.path.join("assets/Audio/hurt.wav"))
]

class GameObject:
    
    def __init__(self,image):
        self.image = image
        # assert 讓傳進來的圖片，資料型態只能是pygame.Surface
        assert isinstance(self.image, pygame.Surface)
        self.rect = self.image.get_rect()
        
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        
        

class Ball(GameObject):
    def __init__(self,image,x_pos,y_pos,speed_x,speed_y,if_original):   
        super().__init__(image)
        # 自己物件本身現在的速度
        self.speed_x = speed_x
        self.speed_y = speed_y
        # 這裡的變數是用來判斷物件是否有超出螢幕 (針對畫圖的部分)
        self.offset_x = image.get_width()
        self.offset_y = image.get_height()
        # 初始化球體的x跟y的座標
        self.rect.x = x_pos
        self.rect.y = y_pos
        # 上一幀的矩形位置，copy就是把矩形複製一份
        self.previous_rect = self.rect.copy()
        # 新增的球不會扣血
        self.original_ball = if_original
    # 負責球體的更新，判斷不要超過螢幕邊框，更新球體位置
    def update(self):
        if self.rect.x <= 0:
            AUDIO[1].play()
            self.speed_x = abs(self.speed_x)
        if self.rect.x >= config.screen_width - self.offset_x:
            AUDIO[1].play()
            self.speed_x = -abs(self.speed_x)
        if self.rect.y <= 0:
            AUDIO[1].play()
            self.speed_y = abs(self.speed_y)

        
        self.previous_rect = self.rect.copy()
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        

            
        
        

        
#磚頭的類別
class tile(GameObject):
    def __init__(self,image,x_pos,y_pos,type,audio):
        super().__init__(image)
        self.image = image.copy()
        self.rect.x = x_pos
        self.rect.y = y_pos
         # 磚頭有不同種類 (一般、補血、爆炸、加新球、加長桿子)
        self.type = type
        # 設定 alpha 也是 pygame 的東西
        self.alpha = 255
        # 判斷要不要變透明
        self.fading = False
        self.deleted = False
        self.audio = audio
        self.audio.set_volume(0.2)
    # 判斷動畫更新，如果磚頭被打到的話會開始慢慢消失
    def update(self):
        # 若正在消失且在被移除的陣列裡面
        if self.fading == True and self in config.removed:
            self.image = TILE[10]
            self.alpha = max(0, self.alpha - 15)
            self.image.set_alpha(self.alpha)
        if self.alpha <= 0 and self in config.removed:
            config.removed.remove(self)
            
            
    
    def draw(self,screen): 
        screen.blit(self.image,(self.rect.x,self.rect.y))
            

        
# 平台的類別
class bar(GameObject):
    def __init__(self,image):
        super().__init__(image)
        # 這裡的變數是用來判斷物件是否有超出螢幕 (針對畫圖的部分)
        self.offset_x = self.image.get_width()
        self.offset_y = self.image.get_height()
        self.rect.x = config.screen_width / 2 - (self.offset_x/2)
        self.rect.y = 650 - (self.offset_y/2)
        self.speed = 10
    # 處理按下方向鍵後，桿子的移動，讓桿子的圖片呈現不要超出邊框
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
        screen.fill((53,40,90))
# 血量類別
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
        self.full_hp = 6
        # 初始化目前的血量為滿血
        self.current_hp = self.full_hp
        # 此變數是損失的血量 (起始化為0)
        self.lost_hp = 0
        # 畫畫用
        self.half_heart_count = 0                
        self.empty_heart_count = 0                    
        self.full_heart_count = int(self.current_hp / 2)
    # 處理血量的呈現 (此處用拼接呈現)
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
            action.game_stat_end(AUDIO)
# 投射物的類別 (如愛心、長桿等道具 (會垂直往下的那些))            
class Projectile(GameObject):
    def __init__(self,image,pos_x,pos_y,speed_x,speed_y,type):
        super().__init__(image)
        self.image = image
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        # 一樣有不同種類的投射物
        self.type = type
    def update(self,bar_rect,health_obj):
        # 矩形的碰撞檢測，偵測撞到桿子後會有的行為
        if self.rect.colliderect(bar_rect):
            if self.type == "heal":
                if health_obj.current_hp >= health_obj.full_hp:
                    health_obj.current_hp = health_obj.current_hp
                else: 
                    health_obj.current_hp += 1
                    AUDIO[2].play()
                config.projectiles.remove(self)
        
            if self.type == "longbar":
                AUDIO[3].play()
                config.long_bar = True
                config.longbar_multiple_hit *= 2
                config.projectiles.remove(self)
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
            
        
        
            
    
def main():
    #初始化round, points
    config.points = 0
    config.round = 1
    # 建立幀率的物件
    clock = pygame.time.Clock()
    bar1 = bar(BAR[0])
     # config 是存放變數的地方，在裡面的球的陣列加入一顆最一開始的球，最後設True是因為他是最一開始的球
    config.balls.append(action.add_balls(BALL[0],Ball,bar1.rect.center[0]-BALL[0].get_width()/2,config.screen_height/2 - BALL[0].get_height()/2, 0, 0,True))
    background1 = background(BACKGROUND)
    health1 = health()
    config.has_initialized = True
    
    while config.main_run:
        for event in pygame.event.get():
            # 如果要退出的話 (按下esc退出)
            if event.type == pygame.QUIT:
                config.main_run = False
                config.menu_run = False
        
        # 畫圖+抓玩家輸入
        background1.draw(screen)
        userinput = pygame.key.get_pressed()
        # 最一開始操控左右可以決定一開始射球的方向
        action.shoot_ball(userinput)
        config.tiles = action.tile_generation(config.tiles,tile,TILE,screen,AUDIO)
        # 更新球的圖片與位置
        for ball in config.balls:
            ball.draw(screen)
            ball.update()
            # 這邊是圓形的碰撞，把球的半徑跟圓心與桿子傳入函數，判斷有沒有碰撞，若有碰撞則執行以下程式    
            if action.circle_rect_collide(ball.rect.center,ball.offset_x/2,bar1.rect):
                AUDIO[1].play()
                #根據碰撞的方向決定速度 回傳的會是球的新速度x,y 
                ball.speed_x,ball.speed_y = action.collision(ball,bar1)
            #刪除球
            action.delete_balls(ball,health1,AUDIO[5])
            #特殊磚頭被碰到後的行為
            action.tile_action(ball,config.tiles,Projectile,Ball,BALL,PROJECTILE[0],PROJECTILE[1],AUDIO)
        # 更新投射物
        action.projectile_update(screen,bar1.rect,health1)
        # 更新血量
        health1.update(screen)
        action.draw_tiles(screen)   
        bar1.draw(screen)
        bar1.update(userinput)
        # 如果要加球的話，把to_add(待增加)拼接到原本的球陣列上
        if config.to_add:
            config.balls.extend(config.to_add)
            config.to_add.clear()
        # 把原本的桿子變長桿子
        action.long_bar(bar1,BAR[0],BAR[1])

        # 球沒了會重生一顆球 (original 金球)
        action.refill_ball(BALL,Ball,bar1)
        # 畫出分數
        action.draw_score(screen)
        # 畫出 fps
        action.get_fps(clock,screen)

        pygame.display.update()
        
        # 設定fps  
        clock.tick(config.tick)  
    


def menu(): 
    config.menu_run = True
    while config.menu_run:
        # 初始化選單要有的東西
        screen.fill((203,189,173))
        screen.blit(config.logo_menu_text,config.logo_menu_rect)
        screen.blit(config.start_menu_text,config.start_text_rect)
        pygame.display.update()
        # 判斷有沒有要退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.main_run = False
                config.menu_run = False
            if event.type == pygame.KEYDOWN:
                # 按下開始後等0.2秒會進入main()
                pygame.time.wait(200)
                main()
        # 輸掉的 menu 會出現在這
        # 輸的時候判斷會成功，會進入 gameOver menu
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
                # 按下任何按鈕可以再開始一局
                if event.type == pygame.KEYDOWN:
                    pygame.time.wait(200)
                    config.main_run = True
                    break
        
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    menu()