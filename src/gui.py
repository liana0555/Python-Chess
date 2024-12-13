import pygame
from piece import *
from vboard import *
from movement_matrix import * 
from movement_restrictions import * 
import sys

# Initialize Pygame
pygame.init()

# Constants
BORDER_SIZE = 28  # Border size
BOARD_SIZE = 8
SQUARE_SIZE = 480 // BOARD_SIZE  # Square size
SCREEN_WIDTH = 480 + BORDER_SIZE * 2
SCREEN_HEIGHT = 480 + BORDER_SIZE * 2

COLORS = [(255, 255, 255), (12, 100, 29)]  # Light and dark square colors
BORDER_COLOR = (81, 93, 56)  # Border color
HIGHLIGHT_COLOR = (200, 200, 0)  # Highlight color for valid moves

# Load piece images
PICTURES_FOLDER = "pictures"
IMAGES = {
    "p_w": pygame.image.load(f"{PICTURES_FOLDER}/white_pawn.png"),
    "p_b": pygame.image.load(f"{PICTURES_FOLDER}/black_pawn.png"),
    "r_w": pygame.image.load(f"{PICTURES_FOLDER}/white_rook.png"),
    "r_b": pygame.image.load(f"{PICTURES_FOLDER}/black_rook.png"),
    "k_w": pygame.image.load(f"{PICTURES_FOLDER}/white_king.png"),
    "k_b": pygame.image.load(f"{PICTURES_FOLDER}/black_king.png"),
    "q_w": pygame.image.load(f"{PICTURES_FOLDER}/white_queen.png"),
    "q_b": pygame.image.load(f"{PICTURES_FOLDER}/black_queen.png"),
    "b_w": pygame.image.load(f"{PICTURES_FOLDER}/white_bishop.png"),
    "b_b": pygame.image.load(f"{PICTURES_FOLDER}/black_bishop.png"),
    "n_w": pygame.image.load(f"{PICTURES_FOLDER}/white_knight.png"),
    "n_b": pygame.image.load(f"{PICTURES_FOLDER}/black_knight.png"),
}

# Scale images to square size
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (SQUARE_SIZE, SQUARE_SIZE))

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess with Drag and Drop")
clock = pygame.time.Clock()

# Initialize the board
board = initBoardR()

# Fonts
font = pygame.font.SysFont("Arial", 20)

def draw_board():
    """Draws the chessboard with borders."""
    # Draw the border
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, BORDER_SIZE))  # Top
    pygame.draw.rect(screen, BORDER_COLOR, (0, SCREEN_HEIGHT - BORDER_SIZE, SCREEN_WIDTH, BORDER_SIZE))  # Bottom
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, BORDER_SIZE, SCREEN_HEIGHT))  # Left
    pygame.draw.rect(screen, BORDER_COLOR, (SCREEN_WIDTH - BORDER_SIZE, 0, BORDER_SIZE, SCREEN_HEIGHT))  # Right

    # Draw the squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = COLORS[(row + col) % 2]
            pygame.draw.rect(screen, color, 
                             (col * SQUARE_SIZE + BORDER_SIZE, 
                              row * SQUARE_SIZE + BORDER_SIZE, 
                              SQUARE_SIZE, SQUARE_SIZE))

    # Draw coordinates
    for col in range(BOARD_SIZE):
        label = font.render(chr(ord("a") + col), True, (255, 255, 255))
        screen.blit(label, (col * SQUARE_SIZE + BORDER_SIZE + SQUARE_SIZE // 3, SCREEN_HEIGHT - BORDER_SIZE + 4))

    for row in range(BOARD_SIZE):
        label = font.render(str(8 - row), True, (255, 255, 255))
        screen.blit(label, (8, row * SQUARE_SIZE + BORDER_SIZE + SQUARE_SIZE // 3))

def draw_pieces():
    """Draws the pieces on the board."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if isinstance(piece, Piece):
                img_key = f"{piece.name.lower()}_{'w' if piece.color == Color.white else 'b'}"
                screen.blit(IMAGES[img_key], 
                            (col * SQUARE_SIZE + BORDER_SIZE, 
                             row * SQUARE_SIZE + BORDER_SIZE))

def draw_moves(piece):
    """Highlights valid moves for the selected piece."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if piece.possibleMoves[row][col] == "1":
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                                 (col * SQUARE_SIZE + BORDER_SIZE, 
                                  row * SQUARE_SIZE + BORDER_SIZE, 
                                  SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse():
    """Gets the chessboard square under the mouse pointer."""
    mouse_pos = pygame.mouse.get_pos()
    x, y = (mouse_pos[0] - BORDER_SIZE) // SQUARE_SIZE, (mouse_pos[1] - BORDER_SIZE) // SQUARE_SIZE
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        return x, y
    return None, None

def main():
    selected_piece = None
    selected_pos = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = get_square_under_mouse()
                if x is not None and y is not None and isinstance(board[y][x], Piece):
                    selected_piece = board[y][x]
                    selected_pos = (y, x)
                    selected_piece.possibleMoves = restrictImpossibleMoves(board, selected_piece, y, x)

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    new_x, new_y = get_square_under_mouse()
                    if (new_x is not None and new_y is not None and 
                        selected_piece.possibleMoves[new_y][new_x] == "1"):
                        board[selected_pos[0]][selected_pos[1]] = "_"
                        board[new_y][new_x] = selected_piece
                    selected_piece.possibleMoves = clearMap(selected_piece.possibleMoves)
                    selected_piece = None
                    selected_pos = None

        # Drawing
        screen.fill((0, 0, 0))
        draw_board()
        draw_pieces()

        if selected_piece:
            x, y = get_square_under_mouse()
            draw_moves(selected_piece)
            if x!=None and y!=None:
                pygame.draw.rect(screen, (100,100,0), ((x * SQUARE_SIZE)+BORDER_SIZE, (y * SQUARE_SIZE)+BORDER_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
