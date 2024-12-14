import pygame
import sys #To use to finish the program(sys.exit)
from button import Button
import Comunication
import PuzzleBoard

# Initializing pygame
pygame.init()

# Screen Options
WIDTH, HEIGHT = 900, 900
MAX_FPS = 60;

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creates a window for the game
pygame.display.set_caption("Menu")
main_background = pygame.image.load("image.png")
clock = pygame.time.Clock()  #Frames Per Second(game stability)

#Loading and setting the cursor 
cursor = pygame.image.load("cursor.png")
pygame.mouse.set_visible(False) #Hiding our default cursor

# Creating buttons with added sound
start_button = Button(WIDTH/2 - (252/2), 50, 252, 74, "", "Pictures_button/play_button.png", "Pictures_button/play1_button.png" , "knopka-vyiklyuchatelya1.mp3")  
puzzles_menu = Button(WIDTH/2 - (252/2), 150, 252, 74,"", "Pictures_button/puzzle_button.png", "Pictures_button/puzzle1_button.png" , "knopka-vyiklyuchatelya1.mp3")  
exit_button = Button(WIDTH/2 - (252/2), 250, 250, 74,"", "Pictures_button/exit_button.png", "Pictures_button/exit1_button.png" , "knopka-vyiklyuchatelya1.mp3")  

# List of levels for the puzzle
puzzle_levels = [
    {"level": 1},
    {"level": 2},
    {"level": 3},]

def puzzles_menu():
    current_level = 0
    puzzle_board = PuzzleBoard(puzzle_levels[current_level]["level"])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checking the solution to the puzzle
            if puzzle_board.check_solution():
                current_level += 1
                if current_level < len(puzzle_levels):
                    puzzle_board = PuzzleBoard(puzzle_levels[current_level]["level"])
                else:
                    print("You've passed all the levels!")
                    return  # Return to main menu
                
   # Drawing the board
        puzzle_board.draw_board(screen, PuzzleBoard.SQUARE_SIZE, PuzzleBoard.COLORS, PuzzleBoard.IMAGES, WIDTH, HEIGHT, PuzzleBoard.BORDER_SIZE)
        pygame.display.flip()

def new_game():
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                #Closing the program 
                pygame.quit()
                sys.exit()

        clock.tick(MAX_FPS)  # Limit FPS
        pygame.display.flip()

