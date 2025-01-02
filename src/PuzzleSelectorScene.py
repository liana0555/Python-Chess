import pygame
import sys
from button import Button

class PuzzleSelectorScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 66)
        self.main_background = pygame.image.load("pictures/background/main_menu.png");
        # Title Text
        self.title_text = self.font.render("Puzzle Game", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height()-40))
        self.cursor = pygame.image.load("pictures/cursor.png")

        
# Hide the standard cursor
        # Puzzle Buttons
        self.puzzle_buttons = [
            Button(screen.get_width() // 2 - 126, 100, 252, 74, "Puzzle 1", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 - 126, 200, 252, 74, "Puzzle 2", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png",  
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 - 126, 300, 252, 74, "Puzzle 3", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
        ]

        
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

        # Draw Puzzle Buttons
        for button in self.puzzle_buttons:
            button.draw(self.screen)


        self.draw_custom_cursor()
        pygame.display.flip()

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # Update hover states for all buttons
        for button in self.puzzle_buttons:
            button.check_hover(mouse_pos)
        

        # Pass events to buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any of the puzzle buttons are clicked
            for i, button in enumerate(self.puzzle_buttons):
                if button.is_clicked(event.pos):
                    print(f"Puzzle {i + 1} selected")
                    # Here you can switch to the actual puzzle scene
                    self.scene_manager.switch_scene(f"PuzzleScene_{i + 1}")



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.switch_scene("MainMenuScene")
