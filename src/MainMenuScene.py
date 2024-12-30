import pygame
import sys  # To use to finish the program (sys.exit)
from button import Button

class MainMenuScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 36)

        # Title Text
        self.title_text = self.font.render("New Game", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 100))

        # Buttons
        self.start_button = Button(
            screen.get_width() // 2 - 126, 50, 252, 74, "", 
            "pictures/Pictures_button/play_button.png", "pictures/Pictures_button/play1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.puzzles_button = Button(
            screen.get_width() // 2 - 126, 150, 252, 74, "", 
            "pictures/Pictures_button/puzzle_button.png", "pictures/Pictures_button/puzzle1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.settings_button = Button(
            screen.get_width() // 2 - 126, 250, 252, 74, "", 
            "pictures/Pictures_button/exit_button.png", "pictures/Pictures_button/exit1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.exit_button = Button(
            screen.get_width() // 2 - 126, 350, 252, 74, "", 
            "pictures/Pictures_button/exit_button.png", "pictures/Pictures_button/exit1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )

    def setup(self):
        pass

    def cleanup(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        # Draw Title
        self.screen.blit(self.title_text, self.title_rect)

        # Draw Buttons
        self.start_button.draw(self.screen)
        self.puzzles_button.draw(self.screen)
        self.exit_button.draw(self.screen)

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
                print("Puzzles menu selected")
            elif self.exit_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
