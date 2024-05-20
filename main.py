import pygame
from Config import config
import sys

def move_policeman(x_coordinate, y_coordinate, keys):
    """Funkcia rieši pohyb policajta podľa stlačenia klávies smeru"""
    if keys[pygame.K_LEFT]:
        if x_coordinate > 10:  # Aby policajt nevyšiel za ľavý okraj
            x_coordinate -= config.STEP  # Pohyb policajta vľavo
    if keys[pygame.K_RIGHT]:
        if x_coordinate < config.ROZLISENIE[0] - config.POLICAJT.get_width() - 10:  # Aby policajt nevyšiel za pravý okraj
            x_coordinate += config.STEP  # Pohyb policajta vpravo
    if keys[pygame.K_UP]:
        if y_coordinate > 10:  # Aby policajt nevyšiel hore za okraj
            y_coordinate -= config.STEP  # Pohyb policajta nahor
    if keys[pygame.K_DOWN]:
        if y_coordinate < config.ROZLISENIE[1] - config.POLICAJT.get_height() - 10:  # Aby policajt nevyšiel dole za okraj
            y_coordinate += config.STEP  # Pohyb policajta nadol
    return x_coordinate, y_coordinate

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(config.ROZLISENIE)
    pygame.display.set_caption("Policajt verzus auta")

    policajt = config.POLICAJT
    auto = config.AUTO

    x, y = config.ROZLISENIE[0] // 2, config.ROZLISENIE[1] // 2 # Inicializácia pozície policajta

    clock = pygame.time.Clock()

    while True:
        # Ak vypnem okno, musím vypnuť pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Vypnutie pygamu
                sys.exit() # Vypnutie celého programu
        
        keys = pygame.key.get_pressed()
        x, y = move_policeman(x, y, keys)
            
        window.fill(config.FARBA_POZADIA)  # Premazanie obrazovky

        window.blit(policajt, (x, y))
        window.blit(auto, (config.ROZLISENIE[0] // 10, config.ROZLISENIE[1] // 10))

        pygame.display.update()

        # Spomalenie cyklu
        clock.tick(config.FPS) # Obnova hada - resp.obrázkov