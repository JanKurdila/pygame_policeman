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
    pygame.mixer.init()

    window = pygame.display.set_mode(config.ROZLISENIE)
    pygame.display.set_caption("Policajt verzus auta")

    font = config.FONT_SCORE_TEXT
    score = 0
    zvuk_kolizie = config.ZVUK_KOLIZIE

    policajt = config.POLICAJT
    policajt_mask = pygame.mask.from_surface(policajt)
    x, y = config.ROZLISENIE[0] // 2, config.ROZLISENIE[1] // 2 # Inicializácia pozície policajta

    auto, auto_position, auto_mask = generate_car(config.ROZLISENIE, config.AUTO)

    clock = pygame.time.Clock()

    trvanie_hry = config.TRVANIE_HRY
    start_time = pygame.time.get_ticks()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = max(0, (trvanie_hry - elapsed_time) // 1000)

        if elapsed_time >= trvanie_hry:
            game_over = True
            if score >= config.POCET_POKUT:
                message = "Blahoželám, vybrali ste potrebný počet pokút."
            else:
                message = "Nevybrali ste potrebný počet pokút."
            break

        keys = pygame.key.get_pressed()
        x, y = move_policeman(x, y, keys)
        
        stala_sa_kolizia = is_collision(policajt_mask, auto_mask, (x, y), auto_position)
        if stala_sa_kolizia:
            score += 1
            zvuk_kolizie.play()
            auto, auto_position, auto_mask = generate_car(config.ROZLISENIE, config.AUTO)
        
        window.fill(config.FARBA_POZADIA)
        window.blit(policajt, (x, y))
        window.blit(auto, auto_position)

        score_text = font.render(f"Skóre: {score}", True, config.FARBA_SCORE_TEXT)
        window.blit(score_text, (10, 10))

        time_text = font.render(f"Čas: {remaining_time}", True, config.FARBA_SCORE_TEXT)
        window.blit(time_text, (10, 40))

        pocet_pokut_text = font.render(f"Potrebné pokuty: {config.POCET_POKUT}", True, config.FARBA_SCORE_TEXT)
        window.blit(pocet_pokut_text, (10, 70))

        pygame.display.update()
        clock.tick(config.FPS)

    # Zobrazenie správy na konci hry
    window.fill(config.FARBA_POZADIA)
    message_text = font.render(message, True, config.FARBA_SCORE_TEXT)
    window.blit(message_text, (config.ROZLISENIE[0] // 2 - message_text.get_width() // 2, config.ROZLISENIE[1] // 2 - message_text.get_height() // 2))
    score_text = font.render(f"Skóre: {score}", True, config.FARBA_SCORE_TEXT)
    window.blit(score_text, (10, 10))
    time_text = font.render(f"Čas: {remaining_time}", True, config.FARBA_SCORE_TEXT)
    window.blit(time_text, (10, 40))
    pocet_pokut_text = font.render(f"Potrebné pokuty: {config.POCET_POKUT}", True, config.FARBA_SCORE_TEXT)
    window.blit(pocet_pokut_text, (10, 70))
    pygame.display.update()

    # Čakanie na ukončenie hry
    waiting_for_exit = True
    while waiting_for_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_exit = False

    pygame.quit()
    sys.exit()