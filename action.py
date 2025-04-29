import pygame

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

def tile_generation():
    pass