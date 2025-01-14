import pygame
import sys
import os
from button import Button
from scenes.ChessGameScene import ChessGameScene
from puzzleBoards import initPuzzle1,initPuzzle2,initPuzzle3

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
            Button(screen.get_width() //  2 - 348, 25, 232, 74, "Puzzle 1", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 - 116, 25, 232, 74, "Puzzle 2", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png",  
                   "audio/knopka-vyiklyuchatelya1.mp3"),
            Button(screen.get_width() // 2 + 116, 25, 232, 74, "Puzzle 3", 
                   "pictures/Pictures_button/puzzle_button.png", 
                   "pictures/Pictures_button/puzzle1_button.png", 
                   "audio/knopka-vyiklyuchatelya1.mp3"),
        ]

        
    def draw_custom_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor, (mouse_pos[0] - self.cursor.get_width() // 2, mouse_pos[1] - self.cursor.get_height() // 2))
        
    def setup(self): # Setup - Initialize scenes (creates initial variables)
        pass

    def cleanup(self): #Cleanup - Changing the scene
        pass

    def update(self): #Update - Update the scene
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

    #All the action scenes
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
                    match i+1:
                        case 1 :
                            new_game_scene = ChessGameScene(self.screen, self.scene_manager , initPuzzle1())
                        case 2 :
                            new_game_scene = ChessGameScene(self.screen, self.scene_manager , initPuzzle2())
                        case 3 :
                            new_game_scene = ChessGameScene(self.screen, self.scene_manager , initPuzzle3())
                    self.scene_manager.add_scene("NewGameScene", new_game_scene)
                    self.scene_manager.switch_scene("NewGameScene")



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.switch_scene("MainMenuScene")
