import pygame
import sys 
from button import Button

class MainMenuScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 66)

        # Title Text
        self.title_text = self.font.render("New Game", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height()-40))

        self.main_background = pygame.image.load("pictures/background/main_menu.png")
        self.cursor = pygame.image.load("pictures/cursor.png")
        
        # Buttons positioned horizontally
        button_width = 232
        button_height = 74
        button_spacing = 10

        total_width = 3 * button_width + 2 * button_spacing
        start_x = (screen.get_width() - total_width) // 2

        self.start_button = Button(
            start_x, 25, button_width, button_height, "",
            "pictures/Pictures_button/play_button.png", "pictures/Pictures_button/play1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.puzzles_button = Button(
            start_x + button_width + button_spacing, 25, button_width, button_height, "",
            "pictures/Pictures_button/puzzle_button.png", "pictures/Pictures_button/puzzle1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.exit_button = Button(
            start_x + 2 * (button_width + button_spacing), 25, button_width, button_height, "",
            "pictures/Pictures_button/exit_button.png", "pictures/Pictures_button/exit1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )

    def draw_custom_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor, (mouse_pos[0] - self.cursor.get_width() // 2, mouse_pos[1] - self.cursor.get_height() // 2))
        
    def setup(self):
        pass

    def cleanup(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.main_background, (0, -30))

        # Draw Title
        self.screen.blit(self.title_text, self.title_rect)

        # Draw Buttons
        self.start_button.draw(self.screen)
        self.puzzles_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        self.draw_custom_cursor()
        pygame.display.flip()

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # Update hover states
        self.start_button.check_hover(mouse_pos)
        self.puzzles_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)

        # Pass events to buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos):
                self.scene_manager.switch_scene("NewGameScene")
            elif self.puzzles_button.is_clicked(event.pos):
                self.scene_manager.switch_scene("PuzzleSelectorScene")
            elif self.exit_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
