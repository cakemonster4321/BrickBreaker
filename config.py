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
pygame.font.init()
font = pygame.font.Font(os.path.join("assets/font", "ARCADECLASSIC.TTF"), 30)
score_text = score_text = font.render(f"Your score  {points}",True,(255,255,255))

