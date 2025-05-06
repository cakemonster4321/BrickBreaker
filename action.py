import config
import random
import pygame

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
   
    dx = (ball.rect.centerx - object.rect.centerx)
    dy = (ball.rect.centery - object.rect.centery)
    widths = (ball.rect.width + object.rect.width) / 2
    heights = (ball.rect.height + object.rect.height) / 2

    overlap_x = widths - abs(dx)
    overlap_y = heights - abs(dy)

    if overlap_x < overlap_y:
        direction = "left" if dx < 0 else "right"
    else:
        direction = "top" if dy < 0 else "bottom"

            
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

def tile_action(ball,tiles,ball_cls,ball_image):
    to_remove = []
    tile_break = False
    tile_break = check_bounce_tileBreak(ball,tiles,to_remove)
    for tile in to_remove:
        if tile in tiles:
            x, y = tile.rect.center
            tiles.remove(tile)
    # if tile_break:
        # new_ball = add_balls(ball_image, ball_cls, x, y, ball.speed_x+1, ball.speed_y)
        # config.to_add.append(new_ball)

def check_bounce_tileBreak(ball,tiles,to_remove):
    ball_range = ball.rect.inflate(50,50)
    hit = False
    for tile in reversed((tiles)):
        if not ball_range.colliderect(tile.rect):
            continue
        if not circle_rect_collide(ball.previous_rect.center,ball.offset_x/2,tile.rect) and circle_rect_collide(ball.rect.center,ball.offset_x/2,tile.rect):
            ball.speed_x,ball.speed_y = collision(ball,tile)
            config.score_text = score()
            to_remove.append(tile)
            hit =  True
    return hit
            
            
def tile_generation(tiles,tile,image,amount):
    x_pos = 0
    y_pos = 0
    assert isinstance(tiles,list)
    assert isinstance(image,list)
    if len(tiles) == 0:
        for _ in range(0,amount):
            num = random.randint(0,1)
            tiles.append(tile(image[num],x_pos,y_pos))
            x_pos += 30
            
            if x_pos == config.screen_width:
                y_pos += 30
                x_pos = 0
    return tiles

def score():
    config.points += 1
    config.score_text = config.font.render(f"Your score : {config.points}",False,(255,255,255))
    
    return config.score_text

def draw_score(screen):
    screen.blit(config.score_text,(720,660))

def draw_total_score(screen):
    config.total_points_text = config.menu_font.render(f"You got {config.points}",False,(255,255,255))
    screen.blit(config.total_points_text,config.total_points_rect)
    
def add_balls(image,cls,x_pos,y_pos,speed_x,speed_y):
    return cls(image,x_pos,y_pos,speed_x,speed_y)

def refill_ball(image,ball_cls,userinput,bar1):
    if not config.balls and config.has_initialized:
        config.balls.append(add_balls(image,ball_cls,bar1.rect.center[0]-image.get_width()/2,
        500-image.get_height(),0,0 ))
        config.ball_refilled = True
    if len(config.balls) == 1 and config.ball_refilled:
        shoot_ball(userinput)
    config.ball_refilled = False        
        
def shoot_ball(userinput):

    for ball in config.balls:
        if ball.speed_x != 0 and ball.speed_y != 0:
            break
        elif userinput[pygame.K_LEFT]:
            ball.speed_x = -config.ballspeed_x
            ball.speed_y = config.ballspeed_y
            # print("yes")
        elif userinput[pygame.K_RIGHT]:
            ball.speed_x = config.ballspeed_x
            ball.speed_y = config.ballspeed_y

def delete_balls(ball,health):
    if ball.rect.y >= config.screen_height:
        if ball in config.balls:
            config.balls.remove(ball)
            take_damage(health)

def take_damage(health):
    health.current_hp -= 1

def draw_tiles(screen):
    for tile in config.tiles:
        tile.draw(screen)

def game_stat_end():
    config.main_run = False
    config.tiles.clear()
    config.balls.clear()
    config.ball_refilled = False
    config.has_initialized = False
    
def get_fps(clock,screen):
    fps = clock.get_fps()
    fps_text = config.font.render(f"FPS: {fps:.2f}", False, (255, 255, 255))
    screen.blit(fps_text, (720, 630))
# def block_add_ball(tile,ballspeed_x,ballspeed_y,cls):
#     config.ball_count += 1
#     add_balls(config.balls,config.ball_count,cls,config.BALL)

    


    
    
    
    
    