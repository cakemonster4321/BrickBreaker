import pygame
import os

screen_height = 700
screen_width = 1200
main_run  = True
menu_run  = True
ballspeed_x = 8
ballspeed_y = -8
balls = []
to_remove = []
to_add = []
ball_count = 1
tiles = []
tile_amount = 240
points = 0
health = 3
has_initialized = False

pygame.font.init()
font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 40)
menu_font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 60)

score_text = font.render(f"Your score  {points}",False,(255,255,255))
start_menu_text = menu_font.render(f"Press left or right to start!",False,(255,255,255))
start_text_rect = start_menu_text.get_rect()
start_text_rect.center = (screen_width/2,screen_height/2-50)


end_menu_text2 = menu_font.render(f"Press left or right to continue!",False,(255,255,255))
end_text_rect2 = end_menu_text2.get_rect()
end_text_rect2.center = (screen_width/2,screen_height/2)


end_menu_text1 = menu_font.render(f"GAME  OVER!",False,(255,255,255))
end_text_rect1 = end_menu_text1.get_rect()
end_text_offset = (end_text_rect2.width - end_text_rect1.width) / 2
end_text_rect1.center = (screen_width/2,screen_height/2-50)
