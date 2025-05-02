import pygame
import os

screen_height = 700
screen_width = 1200
run  = True
gamespeed = 15
tiles = []
tile_amount = 240
points = 0
health = 3
has_initialized = False

pygame.font.init()
font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 40)
menu_font = pygame.font.Font(os.path.join("assets/font", "PixelPurl.TTF"), 60)

score_text = font.render(f"Your score  {points}",True,(255,255,255))
menu_text = menu_font.render(f"Press any left / right to Start!",True,(255,255,255))
menu_text_rect = menu_text.get_rect()
menu_text_rect.center = (screen_width/2,screen_height/2+50)

