import pygame
from Config import config
import sys
import random

def move_policeman(x_coordinate, y_coordinate, keys):
    """Funkcia rieši pohyb policajta podľa stlačenia klávies smeru"""
    if keys[pygame.K_LEFT]:
        if x_coordinate > 10:  # Aby policajt nevyšiel za ľavý okraj
            x_coordinate -= config.STEP  # Pohyb policajta vľavo
    elif keys[pygame.K_RIGHT]:
        if x_coordinate < config.ROZLISENIE[0] - config.POLICAJT.get_width() - 10:  # Aby policajt nevyšiel za pravý okraj
            x_coordinate += config.STEP  # Pohyb policajta vpravo
    elif keys[pygame.K_UP]:
        if y_coordinate > 10:  # Aby policajt nevyšiel hore za okraj
            y_coordinate -= config.STEP  # Pohyb policajta nahor
    elif keys[pygame.K_DOWN]:
        if y_coordinate < config.ROZLISENIE[1] - config.POLICAJT.get_height() - 10:  # Aby policajt nevyšiel dole za okraj
            y_coordinate += config.STEP  # Pohyb policajta nadol
    return x_coordinate, y_coordinate

def generate_car(game_res, car_image):
    """Funkcia zabezpečí náhodne vygenerovanie auta na náhodnej pozícii"""
    car_width, car_height = car_image.get_size()
    x = random.randint(0, game_res[0] - car_width)
    y = random.randint(0, game_res[1] - car_height)
    return car_image, (x, y), pygame.mask.from_surface(car_image)
    
def is_collision(mask1, mask2, mask1_coordinate, mask2_coordinate):
    """Funkcia zisti, či nastala kolízia"""
    x_off = mask2_coordinate[0] - mask1_coordinate[0]
    y_off = mask2_coordinate[1] - mask1_coordinate[1]
    if mask1.overlap(mask2, (x_off, y_off)):
        return True
    return False

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(config.ROZLISENIE)
    pygame.display.set_caption("Policajt verzus auta")

    font = config.FONT_SCORE_TEXT
    score = 0

    zvuk = config.ZVUK_KOLIZIE

    policajt = config.POLICAJT
    policajt_mask = pygame.mask.from_surface(policajt)
    x, y = config.ROZLISENIE[0] // 2, config.ROZLISENIE[1] // 2 # Inicializácia pozície policajta

    auto, auto_position, auto_mask = generate_car(config.ROZLISENIE, config.AUTO)

    clock = pygame.time.Clock()

    stala_sa_kolizia = False

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
        window.blit(auto, auto_position)
        
        if is_collision(policajt_mask, auto_mask, (x, y), auto_position):
            if not stala_sa_kolizia:
                stala_sa_kolizia = True
                score += 1
                zvuk.play()
                auto, auto_position, auto_mask = generate_car(config.ROZLISENIE, config.AUTO)
        else:
            stala_sa_kolizia = False

        score_text = font.render(f"Skóre: {score}", True, (config.FARBA_SCORE_TEXT))
        window.blit(score_text, (10, 10))

        pygame.display.update()

        # Spomalenie cyklu
        clock.tick(config.FPS) # Obnova hada - resp.obrázkov