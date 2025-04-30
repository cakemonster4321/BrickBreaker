import pygame
import random
def collision_x(ball,object):
    if ball.rect.x > object.rect.x and ball.speed_x > 0:
        ball.speed_x = abs(ball.speed_x)
    elif ball.rect.x > object.rect.x and ball.speed_x < 0:
        ball.speed_x = -abs(ball.speed_x)
    return ball.speed_x

def collision_y(ball,object):
    if ball.rect.y < object.rect.y:
        ball.speed_y = -abs(ball.speed_y)
    if ball.rect.y > object.rect.y:
        ball.speed_y = abs(ball.speed_y)
    return ball.speed_y
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
            if x_pos == 1200:
                y_pos += 30
                x_pos = 0
    return tiles