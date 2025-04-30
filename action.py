import pygame
import random
def collision(ball,object):
    right = abs(object.rect.right - ball.rect.left)
    left = abs(object.rect.left - ball.rect.right)
    top = abs(object.rect.top - ball.rect.bottom)
    bottom = abs(object.rect.bottom - ball.rect.top)
    
    if min(right,left) < min(top,bottom):
        direction = "right" if left > right else "left"
    else :
        direction = "bottom" if bottom < top else "top"
        
    if ball.speed_x > 0 and ball.speed_y > 0 and direction == "top":
        ball.speed_x = abs(ball.speed_x)
        ball.speed_y = -abs(ball.speed_y)
    if ball.speed_x < 0 and ball.speed_y > 0 and direction == "top":
        ball.speed_x = -abs(ball.speed_x)
        ball.speed_y = -abs(ball.speed_y)
        
    if ball.speed_y > 0 and ball.speed_x < 0 and direction == "right":
        ball.speed_y = abs(ball.speed_y)
        ball.speed_x = abs(ball.speed_x)
    #side
    if ball.speed_y < 0 and ball.speed_x < 0 and direction == "right":
        ball.speed_y = -abs(ball.speed_y)
        ball.speed_x = abs(ball.speed_x)  
    #bottom
    if ball.speed_y < 0 and ball.speed_x < 0 and direction == "bottom":
        ball.speed_y = abs(ball.speed_y)
        ball.speed_x = -abs(ball.speed_x)
        
    if ball.speed_y < 0 and ball.speed_x > 0 and direction == "bottom":
        ball.speed_x = abs(ball.speed_x)
        ball.speed_y = abs(ball.speed_y) 
         
    if ball.speed_y > 0 and ball.speed_x > 0 and direction == "left":
        ball.speed_y = abs(ball.speed_y) 
        ball.speed_x = -abs(ball.speed_x) 
    if ball.speed_y < 0 and ball.speed_x > 0 and direction == "left":
        ball.speed_y = -abs(ball.speed_y) 
        ball.speed_x = -abs(ball.speed_x) 
    
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
            if x_pos == 300:
                y_pos += 30
                x_pos = 0
    return tiles