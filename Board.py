import pygame
from Number import *

class Board:
    BORDER_COLOR = (81, 93, 56)
    FONT_COLOR = (255, 255, 255)
    SQUARE_COLORS = [(240, 217, 181), (181, 136, 99)]
    FONT_SIZE = 20

    def __init__(self):
        # Initializing an empty board
        self.board = [['.'] * 8 for _ in range(8)]

        # Pawn placement
        for col in range(8):
            self.board[6][col] = Pawn(0)  # White pawns
            self.board[1][col] = Pawn(1)  # Black pawns

        # Arrangement of the other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece in enumerate(piece_order):
            self.board[0][col] = piece(1)  # Black figures
            self.board[7][col] = piece(0)  # White figures


    def draw_board(self, screen, square_size, colors, images, width, height, border_size):
        # Drawing frames
        self.draw_borders(screen, width, height, border_size)
        
        for row in range(8):
            for col in range(8):
                # Draw a square
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen,
                    color,
                    (col * square_size + border_size, row * square_size + border_size, square_size, square_size))

                # Draw figures
                piece = self.board[row][col]
                if piece != ".":  # Check that there's a igure on the square
                    img_key = piece.get_image_key()  
                    screen.blit(images[img_key], (col * square_size + border_size, row * square_size + border_size))

    def draw_borders(self, screen, width, height, border_size):
        pygame.draw.rect(screen, self.BORDER_COLOR, (0, 0, width, border_size))  # Upper boundary
        pygame.draw.rect(screen, self.BORDER_COLOR, (0, height - border_size, width, border_size))  # Lower boundary
        pygame.draw.rect(screen, self.BORDER_COLOR, (0, 0, border_size, height))  # Left border


    def draw_labels(self, screen, font, square_size, width, height, border_size):
        # Draw the letters a-h horizontally
        for col in range(8):
            letter = chr(ord('a') + col)
            label = font.render(letter, True, self.FONT_COLOR)
            # Lower boundary
            x = col * square_size + border_size + square_size // 3
            y = height - border_size + 4
            screen.blit(label, (x, y))

        # Draw the numbers 1-8 vertically
        for row in range(8):
            number = str(8 - row)
            label = font.render(number, True, self.FONT_COLOR)
            # Left border
            x = border_size // 3
            y = row * square_size + border_size + square_size // 3
            screen.blit(label, (x, y))