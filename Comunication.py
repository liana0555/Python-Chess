import pygame  # Initializing Pygame
import os
import sys
from button import Button
from Board import Board
from PuzzleBoard import PuzzleBoard # Importing a puzzle board


pygame.init() # Pygame initialization

# Screen settings
WIDTH, HEIGHT = 600, 532  # Window dimensions
GAME_AREA_WIDTH = 500     # Chessboard width
MOVE_PANEL_WIDTH = 200    # Panel width for moving
MAX_FPS = 60  # Maximum frame rate

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Background for the main menu
main_background = pygame.image.load("image.png")

# Cursor setup
cursor = pygame.image.load("cursor.png")
pygame.mouse.set_visible(False)  # Hide the standard cursor

BORDER_SIZE = 27  # Border size
SQUARE_SIZE = 480 // 8  # Size of each square on the board
COLORS = [(255, 255, 255), (12, 100, 29)]  # White and black square colors

PICTURES_FOLDER = "pictures"

# List of figures and colors
pieces = ['pawn', 'rook', 'king', 'queen', 'bishop', 'knight']
colors = ['white', 'black']

# Automatic image uploading
IMAGES = {f"{piece}_{color[0]}": pygame.image.load(f"{PICTURES_FOLDER}/{color}_{piece}.png")
          for piece in pieces for color in colors}



# Resize images to fit squares on the board
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (SQUARE_SIZE, SQUARE_SIZE))

def handle_buttons(buttons, event):
    for button in buttons:
        button.handle_event(event) # Check the events for each button
        if event.type == pygame.USEREVENT and event.button == button:
            return button  # Returns the button that was clicked
    return None


# Initialize board
board = Board()

current_screen = "menu" 

# Function to draw the custom cursor
def draw_custom_cursor():
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(cursor, (mouse_pos[0] - cursor.get_width() // 2, mouse_pos[1] - cursor.get_height() // 2))

# Check if puzzle is completed
def check_puzzle_completed(puzzle_board):


    return puzzle_board.check_solution()


# Main menu function
def main_menu():
    # Creating buttons and positioning them horizontally from left to right
    start_button = Button(5, 20, 200, 74, "", "Pictures_button/play_button.png", "Pictures_button/play1_button.png" , "knopka-vyiklyuchatelya1.mp3")  
    puzzles_menu = Button(205, 20, 200, 74, "", "Pictures_button/puzzle_button.png", "Pictures_button/puzzle1_button.png" , "knopka-vyiklyuchatelya1.mp3")  
    exit_button = Button(400, 20, 200, 74, "", "Pictures_button/exit_button.png", "Pictures_button/exit1_button.png" , "knopka-vyiklyuchatelya1.mp3")  
    buttons = [start_button, puzzles_menu, exit_button]  # List of buttons

    while True:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -30))

        # Moving the "Chess Game" text to the bottom of the screen
        font = pygame.font.Font(None, 72)
        text_surface = font.render("Chess Game", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT - 50))  # Placing text at the bottom
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handling button presses
            clicked_button = handle_buttons(buttons, event)
            if clicked_button == start_button:
                return "game" # Switching to the game screen
            elif clicked_button == puzzles_menu:
                return "puzzle"
            elif clicked_button == exit_button:
                pygame.quit()
                sys.exit()

        # Drawing buttons
        for btn in buttons:
            btn.check_hover(pygame.mouse.get_pos())  # Checking the mouseover
            btn.draw(screen)  # Draw the button

        draw_custom_cursor()  
        pygame.display.flip() # Refreshing the screen

# Game screen function
def game_screen():
    move_history = []  # Initialize move history

    back_to_menu_button = Button(
         x=WIDTH - 105,  # Place the button in the lower right corner
        y=HEIGHT - 50,  # Offset from the bottom edge
        width=110,
        height=60,
        text="",
        image_path="Pictures_button/exit_button.png",
        hover_image_path="Pictures_button/exit1_button.png",
        sound_path="knopka-vyiklyuchatelya1.mp3"
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#***Addition
            # Return to menu when ESC is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Checks the press
                return "menu" #If pressed return to the screen "menu"

            # Check button click
            back_to_menu_button.handle_event(event)
            if event.type == pygame.USEREVENT and event.button == back_to_menu_button:
                return "menu"

            # Example of adding a move to history (replace with actual game logic)
            if event.type == pygame.MOUSEBUTTONDOWN:
                move_history.append("e2-e4")  # Add example move

        # Drawing the chess board
        board.draw_board(screen, SQUARE_SIZE, COLORS, IMAGES, WIDTH, HEIGHT, BORDER_SIZE)
        

        # Draw the move history panel
        pygame.draw.rect(screen, (50, 50, 50), (GAME_AREA_WIDTH, 0, MOVE_PANEL_WIDTH, HEIGHT))  # Panel on the right
        font = pygame.font.Font(None, 24)

        # Display the last 20 moves
        for idx, move in enumerate(move_history[-20:]):
            move_text = font.render(move, True, (255, 255, 255))
            screen.blit(move_text, (GAME_AREA_WIDTH + 10, 10 + idx * 20))

        # Draw the "back to menu" button
        back_to_menu_button.check_hover(pygame.mouse.get_pos())
        back_to_menu_button.draw(screen)
        

        # Draw the custom cursor
        draw_custom_cursor()

        pygame.display.flip()

def puzzle_screen(level):
    puzzle_board = PuzzleBoard(level)  # Creating a puzzle board
    move_history = []  # Initializing the history of moves

    # Create “Back to menu” button
    back_to_menu_button = Button(
        x=WIDTH - 105,  # Place the button in the lower right corner
        y=HEIGHT - 50,  # Offset from the bottom edge
        width=110,
        height=60,
        text="",
        image_path="Pictures_button/exit_button.png",
        hover_image_path="Pictures_button/exit1_button.png",
        sound_path="knopka-vyiklyuchatelya1.mp3"
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"  # Exit to the main menu

            # Processing of clicks on the “Back to menu” button
            back_to_menu_button.handle_event(event)
            if event.type == pygame.USEREVENT and event.button == back_to_menu_button:
                return "menu"  # Exit to the main menu

            if event.type == pygame.MOUSEBUTTONDOWN:
                move_history.append("e2-e4")  # Добавляем примерный ход в историю (заменяем на реальную логику)

        # Drawing the board
        puzzle_board.draw_board(screen, SQUARE_SIZE, COLORS, IMAGES, WIDTH, HEIGHT, BORDER_SIZE)

        # Draw the panel on the right
        pygame.draw.rect(screen, (50, 50, 50), (GAME_AREA_WIDTH, 0, MOVE_PANEL_WIDTH, HEIGHT))  # Panel on the right

        # Displaying the history of moves
        font = pygame.font.Font(None, 24)
        for idx, move in enumerate(move_history[-20:]):  # The last 20 moves
            move_text = font.render(move, True, (255, 255, 255))
            screen.blit(move_text, (GAME_AREA_WIDTH + 10, 10 + idx * 20))

        # Checking to see if the puzzle is complete
        if puzzle_board.check_solution():
            return "next_level"  # Moving to the next level

        # Display the “Back to menu” button
        back_to_menu_button.check_hover(pygame.mouse.get_pos())
        back_to_menu_button.draw(screen)

        draw_custom_cursor()
        pygame.display.flip()


# Main loop
while True:
    if current_screen == "menu":
        current_screen = main_menu()
    elif current_screen == "game":
        current_screen = game_screen()
    elif current_screen == "puzzle":
        current_screen = puzzle_screen(level=1)  # Set the puzzle level (can be dynamically changed)
