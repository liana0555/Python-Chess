import pygame
from sceneManager import SceneManager
from scenes.MainMenuScene import MainMenuScene
from scenes.PuzzleSelectorScene import PuzzleSelectorScene

from scenes.SideSelectorScene import SideSelectorScene

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((708, 536))


scene_manager = SceneManager(screen)


main_menu_scene = MainMenuScene(screen, scene_manager)
scene_manager.add_scene("MainMenuScene", main_menu_scene)

puzzle_selector_scene = PuzzleSelectorScene(screen, scene_manager)
scene_manager.add_scene("PuzzleSelectorScene", puzzle_selector_scene)

side_selector_scene = SideSelectorScene(screen, scene_manager)
scene_manager.add_scene("SideSelectorScene", side_selector_scene)

scene_manager.switch_scene("MainMenuScene")

while True:
    if scene_manager.current_scene:
        scene_manager.run_current_scene()
        pygame.display.flip()