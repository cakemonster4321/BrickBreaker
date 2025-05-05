import config
import random


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
        if ball.speed_x > 0 and ball.speed_y > 0:
            ball.speed_x = abs(ball.speed_x)
            ball.speed_y = -abs(ball.speed_y)
            print("a")
        
        if ball.speed_x < 0 and ball.speed_y > 0:
            ball.speed_x = -abs(ball.speed_x)
            ball.speed_y = -abs(ball.speed_y)
            print("b")
            
    elif direction == "bottom":
        if ball.speed_y < 0 and ball.speed_x < 0:
            ball.speed_y = abs(ball.speed_y)
            ball.speed_x = -abs(ball.speed_x)
            print("e")  
        
        if ball.speed_y < 0 and ball.speed_x > 0:
            ball.speed_x = abs(ball.speed_x)
            ball.speed_y = abs(ball.speed_y) 
            print("f")  

    elif direction == "right":        
        if ball.speed_y > 0 and ball.speed_x < 0:
            ball.speed_y = abs(ball.speed_y)
            ball.speed_x = abs(ball.speed_x)
            print("c")
    
        if ball.speed_y < 0 and ball.speed_x < 0:
            ball.speed_y = -abs(ball.speed_y)
            ball.speed_x = abs(ball.speed_x)
            print("d")  
    
    elif direction == "left":    
        if ball.speed_y > 0 and ball.speed_x > 0:
            ball.speed_y = abs(ball.speed_y) 
            ball.speed_x = -abs(ball.speed_x) 
            print("g")  
            
        if ball.speed_y < 0 and ball.speed_x > 0:
            ball.speed_y = -abs(ball.speed_y) 
            ball.speed_x = -abs(ball.speed_x) 
            print("h")  
            
    return ball.speed_x,ball.speed_y

def tile_action(ball,tiles,cls,ball_image):
    config.to_remove = []
    check_bounce(ball,tiles)
            
    # add_balls(ball_image,cls,tile.rect.center[0],tile.rect.center[1],0,-config.ballspeed_y)
    # config.ball_count += 1

    for tile in config.to_remove:
        tiles.remove(tile)

def check_bounce(ball,tiles):
    ball_range = ball.rect.inflate(50,50)
    for tile in reversed((tiles)):
        if not ball_range.colliderect(tile.rect):
            continue
        if not circle_rect_collide(ball.previous_rect.center,ball.offset_x/2,tile.rect) and circle_rect_collide(ball.rect.center,ball.offset_x/2,tile.rect):
            ball.speed_x,ball.speed_y = collision(ball,tile)
            config.score_text = score()
            config.to_remove.append(tile)
            
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
    config.score_text = config.font.render(f"Your score  {config.points}",False,(255,255,255))
    
    return config.score_text

def add_balls(image,cls,x_pos,y_pos,speed_x,speed_y):
    config.to_add.append(cls(image,x_pos,y_pos,speed_x,speed_y))

def delete_balls(ball,health):
    if ball.rect.y >= config.screen_height - ball.rect.height:
        config.balls.remove(ball)
        take_damage(health)

def take_damage(health):
    health.current_hp -= 1

def draw_tiles(screen):
    for tile in config.tiles:
        tile.draw(screen)

# def block_add_ball(tile,ballspeed_x,ballspeed_y,cls):
#     config.ball_count += 1
#     add_balls(config.balls,config.ball_count,cls,config.BALL)
def clean_to_add():
    config.to_add.clear()
    


    
    
    
    
    