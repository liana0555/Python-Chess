# main.py

import pygame
from sceneManager import SceneManager
from MainMenuScene import MainMenuScene
# from settingsScene import SettingsScene
from ChessGameScene import ChessGameScene

pygame.init()

screen = pygame.display.set_mode((708, 536))

# Instantiate SceneManager
scene_manager = SceneManager(screen)


main_menu_scene = MainMenuScene(screen, scene_manager)
scene_manager.add_scene("MainMenuScene", main_menu_scene)

# settings_scene = SettingsScene(screen, scene_manager)
# scene_manager.add_scene("SettingsScene", settings_scene)

new_game_scene = ChessGameScene(screen, scene_manager)
scene_manager.add_scene("NewGameScene", new_game_scene)

# Set the initial scene
scene_manager.switch_scene("MainMenuScene")

while True:
    if scene_manager.current_scene:
        scene_manager.run_current_scene()
        pygame.display.flip()