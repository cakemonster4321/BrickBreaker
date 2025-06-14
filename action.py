import config
import random
import pygame
import time

#取與左右上下接觸的座標
#如果圓心在矩形外面，這個點就是矩形的邊緣上最靠近圓心的位置。
#如果圓心在矩形內部，這個點就是圓心本身。
def circle_rect_collide(circle_center, circle_radius, rect):
    closest_x = max(rect.left, min(circle_center[0], rect.right))
    closest_y = max(rect.top, min(circle_center[1], rect.bottom))

    dx = circle_center[0] - closest_x
    dy = circle_center[1] - closest_y

    if dx**2 + dy**2 <= circle_radius**2:
        return True
     
    return False 
def collision(ball,object):
    direction = ""
   
    #dx 正表示 ball 在 object 右邊，負表示在左邊。
    #dy 正表示 ball 在 object 下方，負表示在上方。
    dx = (ball.rect.centerx - object.rect.centerx)
    dy = (ball.rect.centery - object.rect.centery)
    #如果兩個矩形中心點距離 dx 小於 widths，代表水平方向有重疊。
    #widths 就像是從兩物件中心延伸的邊界距離。
    widths = (ball.rect.width + object.rect.width) / 2
    heights = (ball.rect.height + object.rect.height) / 2
    #兩個的一半長度-兩個中心點的長度
    overlap_x = widths - abs(dx)
    overlap_y = heights - abs(dy)
    
    if overlap_x < overlap_y:
        direction = "left" if dx < 0 else "right"
    else:
        direction = "top" if dy < 0 else "bottom"

    #根據撞擊的面決定球的速度方向      
    if direction == "top":
        if ball.speed_x >= 0 and ball.speed_y >= 0:
            ball.speed_x = abs(ball.speed_x)
            ball.speed_y = -abs(ball.speed_y)
            print("a")
        
        if ball.speed_x <= 0 and ball.speed_y >= 0:
            ball.speed_x = -abs(ball.speed_x)
            ball.speed_y = -abs(ball.speed_y)
            print("b")
            
    elif direction == "bottom":
        if ball.speed_y <= 0 and ball.speed_x <= 0:
            ball.speed_y = abs(ball.speed_y)
            ball.speed_x = -abs(ball.speed_x)
            print("e")  
        
        if ball.speed_y <= 0 and ball.speed_x >= 0:
            ball.speed_x = abs(ball.speed_x)
            ball.speed_y = abs(ball.speed_y) 
            print("f")  

    elif direction == "right":        
        if ball.speed_y >= 0 and ball.speed_x <= 0:
            ball.speed_y = abs(ball.speed_y)
            ball.speed_x = abs(ball.speed_x)
            print("c")
    
        if ball.speed_y <= 0 and ball.speed_x <= 0:
            ball.speed_y = -abs(ball.speed_y)
            ball.speed_x = abs(ball.speed_x)
            print("d")  
    
    elif direction == "left":    
        if ball.speed_y >= 0 and ball.speed_x >= 0:
            ball.speed_y = abs(ball.speed_y) 
            ball.speed_x = -abs(ball.speed_x) 
            print("g")  
            
        if ball.speed_y <= 0 and ball.speed_x >= 0:
            ball.speed_y = -abs(ball.speed_y) 
            ball.speed_x = -abs(ball.speed_x) 
            print("h")  
            
    return ball.speed_x,ball.speed_y
#刪除磚塊與特殊磚塊動作
def tile_action(ball,tiles,projectile_cls,ball_cls,ball_image,heal_image,longbar_image,audio):
    config.to_remove = []
    check_bounce_tileBreak(ball,tiles,config.to_remove)
    for tile in config.to_remove:
        if tile in tiles:
            tile.audio.play()
            tile_add_new_ball(tile,ball_cls,ball_image,ball)
            tile_heal(tile,projectile_cls,heal_image)
            tile_longbar(tile,projectile_cls,longbar_image)
            tile_explode(tile)
            config.removed.append(tile)
            tile.fading = True
            tiles.remove(tile)
            config.score_text = score()
            # tile.deleted = True
            
#以上一偵的rect來判斷是否撞擊
def check_bounce_tileBreak(ball,tiles,to_remove):
    ball_range = ball.rect.inflate(50,50)
    for tile in tiles:
        #如果膨脹後的rect沒有碰到 continue
        if not ball_range.colliderect(tile.rect):
            continue
        #碰到後 判斷 上一偵的rect沒碰到磚塊 現在的rect碰到磚塊 就判斷從哪裡的(collision) 得到新的球速度, 將磚塊加入待刪除
        if not circle_rect_collide(ball.previous_rect.center,ball.offset_x/2,tile.rect) and circle_rect_collide(ball.rect.center,ball.offset_x/2,tile.rect):
            ball.speed_x,ball.speed_y = collision(ball,tile)
            to_remove.append(tile)
            
#一開始設想會有多種pattern, 暫時擱置, 磚塊打完就下一回合 進入tile_pattern 生成磚塊組            
def tile_generation(tiles,tile,image,screen,audio):
    pattern = random.randint(0,0)
    draw_round(screen)
    assert isinstance(tiles,list)
    assert isinstance(image,list)
    if len(tiles) == 0:
        if config.round != 1:
            config.balls.clear()
            config.tick += 50
        config.round_text = round()
        tile_pattern(pattern,tiles,tile,image,audio) 
        audio[3].play()
        config.round += 1
        
    return tiles
#判斷普通與特殊磚塊的生成機率
def tile_type():
    num = random.randint(0,20)
    type = "normal"
    if num > 6:
        type = "normal"
    elif num == 0:
        type = "heal"
    elif num > 0 and num < 5:
        type = "new_ball"
    elif num == 5:
        type = "explode"
    elif num == 6:
        type = "longbar"
    return type


def draw_score(screen):
    screen.blit(config.score_text,(700,config.screen_height - 40))
    
def draw_round(screen):
    screen.blit(config.round_text,(700, config.screen_height - 80))
    

def draw_total_score(screen):
    config.total_points_text = config.menu_font.render(f"You got {config.points}",False,(255,255,255))
    screen.blit(config.total_points_text,config.total_points_rect)
#新增球的工廠函數   
def add_balls(image,cls,x_pos,y_pos,speed_x,speed_y,if_original):
    return cls(image,x_pos,y_pos,speed_x,speed_y,if_original)
#如果沒有金球就補一個
def refill_ball(image,ball_cls,bar1):
    original_count = 0
    for ball in config.balls:
        if ball.original_ball:
            original_count += 1
            
    if not original_count and config.has_initialized:
        config.balls.append(add_balls(image[0],ball_cls,bar1.rect.center[0]-image[0].get_width()/2,
        config.screen_height - 100 -image[0].get_height(),0,0,True))  
        
#得到新球後可以決定從左還是右邊射出     
def shoot_ball(userinput):

    for ball in config.balls:
        if ball.original_ball and ball.speed_x == 0 and ball.speed_y == 0:
            if userinput[pygame.K_LEFT]:
                ball.speed_x = -config.ballspeed_x
                ball.speed_y = config.ballspeed_y
            if userinput[pygame.K_RIGHT]:
                ball.speed_x = config.ballspeed_x
                ball.speed_y = config.ballspeed_y
#球超過下邊界就會被刪除
def delete_balls(ball,health,audio):
    if ball.rect.y >= config.screen_height:
        if ball in config.balls:
            config.balls.remove(ball)
            take_damage(health,ball,audio)
#金球被刪除會扣血
def take_damage(health,ball,audio):
    if ball.original_ball:
        audio.play()
        health.current_hp -= 1

def draw_tiles(screen):
    for tile in config.tiles:
        tile.update()
        tile.draw(screen)
    for tile in config.removed:
        tile.update()
        tile.draw(screen)

#遊戲結束時初始化與清除所有變數
def game_stat_end(audio):
    audio[4].play()
    config.main_run = False
    config.tiles.clear()
    config.balls.clear()
    config.projectiles.clear()
    config.score = 1
    config.round = 1
    config.ball_refilled = False
    config.has_initialized = False
    
#新增球的特殊磚塊
def tile_add_new_ball(tile,ball_cls,ball_image,ball):
    if tile.type == "new_ball":
        new_momentum_x = random.randint(-1,2)
        new_momentum_y = random.randint(-1,2)
        new_ballspeed_x = ball.speed_x + new_momentum_x
        new_ballspeed_y = ball.speed_y + new_momentum_y
        if new_ballspeed_x == 0 or new_ballspeed_y == 0:
            new_ballspeed_x = random.randint(3,5)
            new_ballspeed_y = random.randint(3,5)
        image_num = random.randint(1,3)
        config.balls.append(add_balls(ball_image[image_num],ball_cls,tile.rect.center[0],tile.rect.center[1],new_ballspeed_x,new_ballspeed_y,False))
#回復血量的特殊磚塊       
def tile_heal(tile,projectile_cls,image):
    if tile.type == "heal":
        config.projectiles.append(projectile_cls(image,tile.rect.center[0],tile.rect.center[1],config.projectile_speed_x,config.projectile_speed_y,"heal"))
#讓桿子變大的特殊磚塊      
def tile_longbar(tile,projectile_cls,image):
    if  tile.type == "longbar":
        config.projectiles.append(projectile_cls(image,tile.rect.center[0],tile.rect.center[1],config.projectile_speed_x,config.projectile_speed_y,"longbar"))

def score():
    config.points += 1
    config.score_text = config.font.render(f"Your score : {config.points}",False,(255,255,255))
    
    return config.score_text

def round():
    config.round_text = config.font.render(f"Round : {config.round}",False,(255,255,255))
    return config.round_text

def get_fps(clock,screen):
    fps = clock.get_fps()
    fps_text = config.font.render(f"FPS: {fps:.2f}", False, (255, 255, 255))
    screen.blit(fps_text, (760, 15))

def projectile_update(screen,bar_rect,health_obj):
    for projectile in config.projectiles:
        projectile.update(bar_rect,health_obj)
        projectile.draw(screen)
        
#讓桿子變長10秒，如果還沒結束就加到10秒       
def long_bar(bar,bar_image,longbar_image):
    bar.offset_x = bar_image.get_width()
    bar.offset_y = bar_image.get_height()
    old_bar_centerx = bar.rect.center[0]
    old_bar_centery = bar.rect.center[1]
    if config.long_bar and not config.if_now_called:
        config.long_bar = True
        config.if_now_called = True
        config.end_time = time.time() + 10
        
    if time.time() < config.end_time:
        old_bar_centerx = bar.rect.center[0]
        old_bar_centery = bar.rect.center[1]
        bar.image = longbar_image
        bar.rect = longbar_image.get_rect()
        bar.rect.center =(old_bar_centerx,old_bar_centery)
        bar.offset_y = longbar_image.get_height()
        bar.offset_x = longbar_image.get_width()
        if config.longbar_multiple_hit >= 2:
            print(config.longbar_multiple_hit)
            config.end_time += (10-(config.end_time - time.time()))
            #回到只打中一次的hit
            config.longbar_multiple_hit = 1
    else:
        config.long_bar = False
        config.if_now_called = False
        config.longbar_multiple_hit = 1
        bar.image = bar_image
        bar.rect = bar_image.get_rect()
        bar.rect.center =(old_bar_centerx,old_bar_centery)
#實際生成磚塊組進陣列裡 
def tile_pattern(pattern,tiles,tile_cls,image,audio):
    if pattern == 0:
        x_start_pos = 65
        y_start_pos = 55
        x_pos = x_start_pos
        y_pos = y_start_pos
        gap = 10
        for i in range(0,config.tile_row):
            for j in range(0,config.tile_column):
                type = tile_type()
                if type == "heal":        
                    tiles.append(tile_cls(image[5],x_pos,y_pos,type,audio[0]))
                elif type == "new_ball":
                    tiles.append(tile_cls(image[6],x_pos,y_pos,type,audio[0]))
                elif type == "explode":
                    tiles.append(tile_cls(image[7],x_pos,y_pos,type,audio[0]))
                elif type == "longbar":
                    tiles.append(tile_cls(image[8],x_pos,y_pos,type,audio[0]))
                else:
                    tiles.append(tile_cls(image[i],x_pos,y_pos,type,audio[0]))
                x_pos += (image[0].get_width() + gap)
            x_pos = x_start_pos
            y_pos += image[0].get_height() + 10
#爆炸的特殊磚塊 
def tile_explode(tile):
    if tile.type == "explode":
        explosion_rect = tile.rect.inflate(tile.image.get_width(),tile.image.get_height())
        for other_tile in config.tiles:
            if explosion_rect.colliderect(other_tile) and other_tile != tile:
                config.to_remove.append(other_tile)
                

                
    

    
    
    
    

    


    
    
    
    
    