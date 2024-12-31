import pygame
from sceneManager import SceneManager
from MainMenuScene import MainMenuScene
from PuzzleSelectorScene import PuzzleSelectorScene
from ChessGameScene import ChessGameScene
import puzzle_boards
pygame.init()

screen = pygame.display.set_mode((708, 536))


scene_manager = SceneManager(screen)


main_menu_scene = MainMenuScene(screen, scene_manager)
scene_manager.add_scene("MainMenuScene", main_menu_scene)

puzzle_selector_scene = PuzzleSelectorScene(screen, scene_manager)
scene_manager.add_scene("PuzzleSelectorScene", puzzle_selector_scene)

new_game_scene = ChessGameScene(screen, scene_manager)
scene_manager.add_scene("NewGameScene", new_game_scene)

puzzle_1 = ChessGameScene(screen,scene_manager, puzzle_boards.initPuzzle1())
scene_manager.add_scene("PuzzleScene_1",puzzle_1)

puzzle_2 = ChessGameScene(screen,scene_manager, puzzle_boards.initPuzzle2())
scene_manager.add_scene("PuzzleScene_2",puzzle_2)

puzzle_3 = ChessGameScene(screen,scene_manager, puzzle_boards.initPuzzle3())
scene_manager.add_scene("PuzzleScene_3",puzzle_3)

scene_manager.switch_scene("MainMenuScene")

while True:
    if scene_manager.current_scene:
        scene_manager.run_current_scene()
        pygame.display.flip()