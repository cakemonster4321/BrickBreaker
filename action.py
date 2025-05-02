import config
import random
import math
def collision(ball,object):
    direction = ""
    
    # top_mid_coor = ((object.rect.right + object.rect.left)/2,(object.rect.top))
    # bottom_mid_coor = ((object.rect.right + object.rect.left)/2,(object.rect.bottom))
    # left_mid_coor = (object.rect.left,(object.rect.top + object.rect.bottom)/2)
    # right_mid_coor = (object.rect.right,(object.rect.top + object.rect.bottom)/2)
    
    # right_side_dis = math.sqrt((right_mid_coor[0] - ball.rect.center[0])**2 + (right_mid_coor[1] - ball.rect.center[1])**2)
    # left_side_dis = math.sqrt((left_mid_coor[0] - ball.rect.center[0])**2 + (left_mid_coor[1] - ball.rect.center[1])**2)
    # top_side_dis = math.sqrt((top_mid_coor[0] - ball.rect.center[0])**2 + (top_mid_coor[1] - ball.rect.center[1])**2)
    # bot_side_dis = math.sqrt((bottom_mid_coor[0] - ball.rect.center[0])**2 + (bottom_mid_coor[1] - ball.rect.center[1])**2)

    # if (top_side_dis,bot_side_dis) > (right_side_dis,left_side_dis):
    #     direction = "top" if top_side_dis > bot_side_dis else "bottom"
    # else:
    #     direction = "right" if right_side_dis > left_side_dis else "left"    
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

def tile_action():
    pass

def tile_generation(tiles,tile,image,x_pos,y_pos,amount):
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