import pygame
import sys
import os
from button import Button
from scenes.ChessGameScene import ChessGameScene
import vboard


class SideSelectorScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 66)
        self.main_background = pygame.image.load("pictures/background/main_menu.png")

        # Title Text
        self.title_text = self.font.render("Select Your Side", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 40))
        self.cursor = pygame.image.load("pictures/cursor.png")

        # Side Buttons
        self.side_buttons = [
            Button(screen.get_width() // 2 - 225, screen.get_height() // 2 - 100, 232, 100, "Side 1", 
                   "pictures\Pictures_button\white_queen_button.png", 
                   "pictures\Pictures_button\white_queen_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 + 25, screen.get_height() // 2 - 100, 232, 100, "Side 2", 
                   "pictures\Pictures_button\\black_queen_button.png", 
                   "pictures\Pictures_button\\black_queen_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 232, 100, "Side R",  
                   "pictures\Pictures_button\\random_button.png", 
                   "pictures\Pictures_button\\random_button.png", 
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

        # Draw Side Buttons
        for button in self.side_buttons:
            button.draw(self.screen)

        self.draw_custom_cursor()
        pygame.display.flip()

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # Update hover states for all buttons
        for button in self.side_buttons:
            button.check_hover(mouse_pos)

        # Pass events to buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.side_buttons):
                if button.is_clicked(event.pos):
                    print(i)
                    new_game_scene = None
                    if i == 0:
                        new_game_scene = ChessGameScene(self.screen, self.scene_manager , vboard.initBoardW())
                    elif i == 1:
                        new_game_scene = ChessGameScene(self.screen, self.scene_manager , vboard.initBoardB())
                    elif i == 2:
                        new_game_scene = ChessGameScene(self.screen, self.scene_manager , vboard.initBoardR())
                    else:
                        new_game_scene = ChessGameScene(self.screen, self.scene_manager , vboard.initBoardR())
                    self.scene_manager.add_scene("NewGameScene", new_game_scene)
                    self.scene_manager.switch_scene("NewGameScene")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.switch_scene("MainMenuScene")
