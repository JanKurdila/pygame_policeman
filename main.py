import pygame
from Config import config
import sys

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(config.ROZLISENIE)
    pygame.display.set_caption("Policajt verzus auta")

    policajt = config.POLICAJT
    auto = config.AUTO

    clock = pygame.time.Clock()

    while True:
        # Ak vypnem okno, musím vypnuť pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Vypnutie pygamu
                sys.exit() # Vypnutie celého programu
            
        window.fill(config.FARBA_POZADIA) # Premazanie obrazovky
        window.blit(policajt, (config.ROZLISENIE[0]//2, config.ROZLISENIE[1]//2))
        window.blit(auto, (config.ROZLISENIE[0]//10, config.ROZLISENIE[1]//10))

        pygame.display.update()

        # Spomalenie cyklu
        clock.tick(config.FPS) # Obnova hada - resp.obrázkov