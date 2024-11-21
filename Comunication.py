import pygame #Initializing Pygame
import os

from Board import Board

pygame.init()


BORDER_SIZE = 40  # Border size
WIDTH, HEIGHT = 480 + BORDER_SIZE * 2, 480 + BORDER_SIZE * 2  
SQUARE_SIZE = 480 // 8  # The size of the square
COLORS = [(255, 255, 255), (217, 78, 4)]  # White and black square colors

# Customizing the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Uploading images
PICTURES_FOLDER = "pictures"
IMAGES = {
    "pawn_w": pygame.image.load(f"{PICTURES_FOLDER}/white_pawn.png"),
    "pawn_b": pygame.image.load(f"{PICTURES_FOLDER}/black_pawn.png"),
    "rook_w": pygame.image.load(f"{PICTURES_FOLDER}/white_rook.png"),
    "rook_b": pygame.image.load(f"{PICTURES_FOLDER}/black_rook.png"),
    "king_w": pygame.image.load(f"{PICTURES_FOLDER}/white_king.png"),
    "king_b": pygame.image.load(f"{PICTURES_FOLDER}/black_king.png"),
    "queen_w": pygame.image.load(f"{PICTURES_FOLDER}/white_queen.png"),
    "queen_b": pygame.image.load(f"{PICTURES_FOLDER}/black_queen.png"),
    "bishop_w": pygame.image.load(f"{PICTURES_FOLDER}/white_bishop.png"),
    "bishop_b": pygame.image.load(f"{PICTURES_FOLDER}/black_bishop.png"),
    "knight_w": pygame.image.load(f"{PICTURES_FOLDER}/white_knight.png"),
    "knight_b": pygame.image.load(f"{PICTURES_FOLDER}/black_knight.png"),
    "knight_w": pygame.image.load(f"{PICTURES_FOLDER}/white_knight.png"),
    "knight_b": pygame.image.load(f"{PICTURES_FOLDER}/black_knight.png"),
}

# Making images to fit the size of the square
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (SQUARE_SIZE, SQUARE_SIZE))


# Creating a board
board = Board()

# Main game cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Draw the board
    board.draw_board(screen, SQUARE_SIZE, COLORS, IMAGES, WIDTH, HEIGHT, BORDER_SIZE)

    #Refreshing the screen
    pygame.display.flip()

pygame.quit()
