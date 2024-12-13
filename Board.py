import pygame
from Number import *

class Board(object):
    def __init__(self):
        self.board = [['.'] * 8 for _ in range(8)]

        # Initializing the chess pieces on the board:

        self.board[6][0] = Pawn(0)
        self.board[1][0] = Pawn(1)
        self.board[6][1] = Pawn(0)
        self.board[1][1] = Pawn(1)
        self.board[6][2] = Pawn(0)
        self.board[1][2] = Pawn(1)
        self.board[6][3] = Pawn(0)
        self.board[1][3] = Pawn(1)
        self.board[6][4] = Pawn(0)
        self.board[1][4] = Pawn(1)
        self.board[6][5] = Pawn(0)
        self.board[1][5] = Pawn(1)
        self.board[6][6] = Pawn(0)
        self.board[1][6] = Pawn(1)
        self.board[6][7] = Pawn(0)
        self.board[1][7] = Pawn(1)



        self.board[0][4] = King(1)
        self.board[7][4] = King(0)
        self.board[0][3] = Queen(1)
        self.board[7][3] = Queen(0)
        self.board[0][7] = Rook(1)
        self.board[7][7] = Rook(0)
        self.board[0][5] = Bishop(1)
        self.board[7][5] = Bishop(0)
        self.board[0][6] = Knight(1)
        self.board[7][6] = Knight(0)
        self.board[0][0] = Rook(1)
        self.board[7][0] = Rook(0)
        self.board[0][1] = Bishop(1)
        self.board[7][1] = Bishop(0)
        self.board[0][2] = Knight(1)
        self.board[7][2] = Knight(0)

       
    def __str__(self): #Board output text
        a = ''
        for y in range(8):
            a += ''.join(map(str, self.board[y])) + "\n"
        return a

    def draw_board(self, screen, square_size, colors, images, width, height, border_size):

        # Edge color and text style
        border_color = (81, 93, 56)  
        font = pygame.font.SysFont('Arial', 20)

        # Draw the sides:
        pygame.draw.rect(screen, border_color, (0, 0, width, border_size))  # Upper
        pygame.draw.rect(screen, border_color, (0, height - border_size, width, border_size))  # Lower
        pygame.draw.rect(screen, border_color, (0, 0, border_size, height))  # Left 
        pygame.draw.rect(screen, border_color, (width - border_size, 0, border_size, height))  # Right

        
        for row in range(8):
            for col in range(8):
                # Draw a square
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen,
                    color,
                    (col * square_size + border_size, row * square_size + border_size, square_size, square_size),
                )

                # Draw figures
                piece = self.board[row][col]
                if piece != ".":  # Check that there's a igure on the square
                    img_key = piece.get_image_key()  
                    screen.blit(images[img_key], (col * square_size + border_size, row * square_size + border_size))

        # Draw a-h horizontally
        for col in range(8):
            letter = chr(ord('a') + col)  # From "a" to "h"
            label = font.render(letter, True, (255,255,255))
            screen.blit(label, (col * square_size + border_size + square_size // 3, height - border_size + 4))
           # screen.blit(label, (col * square_size + border_size + square_size // 3, 4))  # Top edge

        # Draw the numbers (1-8) vertically
        for row in range(8):
            number = str(8 - row)  # From 1 to 8
            label = font.render(number, True, (255,255,255))
            screen.blit(label, (8, row * square_size + border_size + square_size // 3))  # Left edge 
           # screen.blit(label, (width - border_size + 5, row * square_size + border_size + square_size // 3))  # Right edge