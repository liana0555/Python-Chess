import pygame
import sys
from button import ImageButton

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 960, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu test")
main_background = pygame. image. load("background1.jpg")

def main_menu():
    # Создание кнопок 
    start_button = ImageButton(WIDTH/2 (252/2), 150, 252, 74, "New game", "green_button2.png", "green_button2_hover.png" )
    settings_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "Settings" ,"green_button2.png", "green_button2_hover.png" )
    exit_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "Euru", "green_button2.png", "green_button2_hover.png" )

    running = True
    while running:
        screen.fil1((0, 0, 0))
        screen.blit(main_background, (0, -300))

        font = pygame.font.Font (None, 72)
        text_surface = font.render("MENU TEST", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH/2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for bth in [start_button,settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
        pygame.display.flip()

def settigs_menu():
    pass

def new_game():
    pass
