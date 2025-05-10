import pygame
import os

screen_height = 700
screen_width = 930
main_run  = True
menu_run  = True
ballspeed_x = 3
ballspeed_y = -3
projectile_speed_x = 0
projectile_speed_y = 3
balls = []
projectiles = []
to_remove = []
removed = []
to_add = []
tiles = []
tile_row = 5
tile_column = 9
points = 0
has_initialized = False
game_over = False
ball_refilled = False
round = 1
if_now_called = False
long_bar = False
end_time = 0
alpha = 255

pygame.font.init()
font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 35)
menu_font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 60)
logo_font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 80)


score_text = font.render(f"Your score : {points}",False,(255,255,255))

logo_menu_text = logo_font.render(f"BRICK BREAKER",False,(0,0,0))
logo_menu_rect = logo_menu_text.get_rect()
logo_menu_rect.center = (screen_width/2,screen_height/2-100)

start_menu_text = menu_font.render(f"Press left or right to start!",False,(255,255,255))
start_text_rect = start_menu_text.get_rect()
start_text_rect.center = (screen_width/2,screen_height/2+100)


end_menu_text2 = menu_font.render(f"Press left or right to continue !",False,(255,255,255))
end_text_rect2 = end_menu_text2.get_rect()
end_text_rect2.center = (screen_width/2,screen_height/2)


end_menu_text1 = menu_font.render(f"GAME OVER !",False,(255,255,255))
end_text_rect1 = end_menu_text1.get_rect()
end_text_offset = (end_text_rect2.width - end_text_rect1.width) / 2
end_text_rect1.center = (screen_width/2,screen_height/2-50)

total_points_text = menu_font.render(f"You got {points}",False,(255,255,255))
total_points_rect = total_points_text.get_rect()
total_points_rect.center = (screen_width/2,screen_height/2+150)

round_text = font.render(f"Round : {round}",False,(255,255,255))
round_text_rect = round_text.get_rect()


