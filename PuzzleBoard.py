import pygame  # Initializing Pygame
import os
import sys
from button import Button
from Number import *

# Screen settings
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 532
GAME_AREA_WIDTH = 500     # Chessboard width
MOVE_PANEL_WIDTH = 200    # Panel width for moving
MAX_FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

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


# Function to draw the custom cursor
def draw_custom_cursor():
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(cursor, (mouse_pos[0] - cursor.get_width() // 2, mouse_pos[1] - cursor.get_height() // 2))

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Definition of the decision checking function
def check_puzzle_completed(board):
    """
    Проверяет, завершена ли головоломка.
    Условие завершения: мат королю противоположного цвета.
    """
    # Finding the kings
    king_positions = {
        0: None,  # White king's position
        1: None   # Black king's position
    }

     # Determining the position of the kings
    for row_idx, row in enumerate(board.board):
        for col_idx, piece in enumerate(row):
            if isinstance(piece, King):
                king_positions[piece.color] = (row_idx, col_idx)

    # Checking if the black king is surrounded
    black_king_pos = king_positions[1]
    if black_king_pos and is_king_in_checkmate(board, black_king_pos):
        return True  # Checkmate to the black king, puzzle complete

    return False # The puzzle is not complete


#Displaying moves to the right
def draw_move_history(screen, move_history, font, area_x, area_width):
    for idx, move in enumerate(move_history[-20:]):
        move_text = font.render(move, True, (255, 255, 255))
        screen.blit(move_text, (area_x + 10, 10 + idx * 20))

def is_king_in_checkmate(board, king_position):
    #Checking to see if the king is in the checkmate
    row, col = king_position
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]):
            if board.board[r][c] == '.':
                return False  # There's at least one safe move
    return True  # The king is surrounded or under attack

class PuzzleBoard:
    def __init__(self, level):
        self.level = level
        self.board_size = 8  # Board size (8x8)
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.setup_puzzle(level)

    def setup_puzzle(self, level):
    #Set the pieces on the board according to the level of the puzzle
        if level == 1:
            self.board[7][7] = King(0)  # The White King
            self.board[6][6] = Queen(1)  # Black queen
            self.board[6][7] = Pawn(1)   # Black pawn
        elif level == 2:
            self.board[0][0] = King(1)   
            self.board[1][1] = Queen(0)  
        elif level == 3:
            self.board[7][0] = King(0) 
            self.board[5][4] = Queen(1) 
            self.board[3][3] = Pawn(1)   

    def draw_board(self, screen, square_size, colors, images, width, height, border_size):
        #Drawing a chessboard with pieces
        border_color = (81, 93, 56)
        font = pygame.font.SysFont('Arial', 20)
        offset_x = border_size  # Board offset in X
        offset_y = border_size  # Board offset in Y

        # Boundary drawing
        pygame.draw.rect(screen, border_color, (0, 0, width, border_size))  # Upper boundary
        pygame.draw.rect(screen, border_color, (0, 0, border_size, height))  # Left 
        pygame.draw.rect(screen, border_color, (0, height - border_size, width, border_size))  # Lower

        # Drawing cells
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen,
                    color,
                    (col * square_size + offset_x, row * square_size + offset_y, square_size, square_size),
                )

                # Figure drawing
                piece = self.board[row][col]
                if isinstance(piece, King):
                    img = images["king_b"] if piece.color == 1 else images["king_w"]
                elif isinstance(piece, Queen):
                    img = images["queen_b"] if piece.color == 1 else images["queen_w"]
                elif isinstance(piece, Pawn):
                    img = images["pawn_b"] if piece.color == 1 else images["pawn_w"]
                else:
                    img = None

                if img is not None:
                    screen.blit(img, (col * square_size + offset_x, row * square_size + offset_y))

     

        # Draw a-h horizontally
        for col in range(8):
            letter = chr(ord('a') + col)  # From "a" to "h"
            label = font.render(letter, True, (255,255,255))
            screen.blit(label, (col * square_size + border_size + square_size // 3, height - border_size + 4))

        # Draw the numbers (1-8) vertically
        for row in range(8):
            number = str(8 - row)  # From 1 to 8
            label = font.render(number, True, (255,255,255))
            screen.blit(label, (8, row * square_size + border_size + square_size // 3))  # Left edge 

    def check_solution(self):
        #Checking if the puzzle is complete
        return check_puzzle_completed(self)


def puzzle_screen(level):
    #The main function of the puzzle screen
    puzzle_board = PuzzleBoard(level)  # Creating a puzzle board
    move_history = []  # Initializing the history of moves
    font = pygame.font.Font(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                move_history.append("примерный ход")

        # Drawing the board
        puzzle_board.draw_board(screen, SQUARE_SIZE, COLORS, IMAGES, WIDTH, HEIGHT, BORDER_SIZE)

        # Drawing a history of moves
        pygame.draw.rect(screen, (50, 50, 50), (GAME_AREA_WIDTH, 0, MOVE_PANEL_WIDTH, HEIGHT))
        draw_move_history(screen, move_history, font, GAME_AREA_WIDTH, MOVE_PANEL_WIDTH)

        # Checking level completion
        if puzzle_board.check_solution():
            return "next_level"

        draw_custom_cursor()
        pygame.display.flip()
