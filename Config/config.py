import pygame

ROZLISENIE = (1100, 600)

# Farby
FARBA_POZADIA = pygame.Color(173, 216, 230)
FARBA_SCORE_TEXT = pygame.Color(255, 255, 255)
pygame.init()
FONT_SCORE_TEXT = pygame.font.Font(None, 36)

POLICAJT = pygame.image.load("IMAGES/pol.png")   
AUTO  = pygame.image.load("IMAGES/auto.png")  

STEP = 5  # Pohyb policajta o 5

FPS = 25
