import config
import random
def collision(ball,object):
    direction = "left"
    if ball.previous_rect.bottom <= object.rect.top:
        direction = "top"
    elif ball.previous_rect.top >= object.rect.bottom:
        direction = "bottom"
    elif ball.previous_rect.right <= object.rect.left:
        direction = "left"
    elif ball.previous_rect.left >= object.rect.right:
        direction = "right"
        
    if ball.speed_x > 0 and ball.speed_y > 0 and direction == "top":
        ball.speed_x = abs(ball.speed_x)
        ball.speed_y = -abs(ball.speed_y)
        print("a")
    if ball.speed_x < 0 and ball.speed_y > 0 and direction == "top":
        ball.speed_x = -abs(ball.speed_x)
        ball.speed_y = -abs(ball.speed_y)
        print("b")
        
    if ball.speed_y > 0 and ball.speed_x < 0 and direction == "right":
        ball.speed_y = abs(ball.speed_y)
        ball.speed_x = abs(ball.speed_x)
        print("c")

    #side
    if ball.speed_y < 0 and ball.speed_x < 0 and direction == "right":
        ball.speed_y = -abs(ball.speed_y)
        ball.speed_x = abs(ball.speed_x)
        print("d")  
    #bottom
    if ball.speed_y < 0 and ball.speed_x < 0 and direction == "bottom":
        ball.speed_y = abs(ball.speed_y)
        ball.speed_x = -abs(ball.speed_x)
        print("e")  
        
    if ball.speed_y < 0 and ball.speed_x > 0 and direction == "bottom":
        ball.speed_x = abs(ball.speed_x)
        ball.speed_y = abs(ball.speed_y) 
        print("f")  
         
    if ball.speed_y > 0 and ball.speed_x > 0 and direction == "left" and ball.rect.bottom > object.rect.top:
        ball.speed_y = abs(ball.speed_y) 
        ball.speed_x = -abs(ball.speed_x) 
        print("g")  
    if ball.speed_y < 0 and ball.speed_x > 0 and direction == "left" and ball.rect.top > object.rect.bottom:
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