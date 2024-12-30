import pygame
import sys
from piece import *
from vboard import *
from movement_matrix import *
from movement_restrictions import *

class ChessGameScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont("Arial", 20)

        # Constants
        self.HISTORY_SCROLL_STEP = 20
        self.HISTORY_WIDTH = 200
        self.BORDER_SIZE = 28
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 480 // self.BOARD_SIZE
        self.SCREEN_WIDTH = 480 + self.BORDER_SIZE * 2 + self.HISTORY_WIDTH
        self.SCREEN_HEIGHT = 480 + self.BORDER_SIZE * 2

        self.COLORS = [(255, 255, 255), (12, 100, 29)]
        self.BORDER_COLOR = (81, 93, 56)
        self.HIGHLIGHT_COLOR_LIGHT = (220, 220, 80)
        self.HIGHLIGHT_COLOR_DARK = (200, 200, 0)
        self.HIGHLIGHT_CURSOUR_COLOR_LIGHT = (180, 180, 60)
        self.HIGHLIGHT_CURSOUR_COLOR_DARK = (120, 120, 0)

        self.PICTURES_FOLDER = "pictures"
        self.IMAGES = self.load_images()

        # Initialize the board
        self.board = None

        # Game state
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = Color.white
        self.move_history = []
        self.previous_states = []  # Stack for undo functionality
        self.history_scroll_offset = 0

        # Clock for frame rate
        self.clock = pygame.time.Clock()

    def load_images(self):
        images = {
            "p_w": "white_pawn.png",
            "p_b": "black_pawn.png",
            "r_w": "white_rook.png",
            "r_b": "black_rook.png",
            "k_w": "white_king.png",
            "k_b": "black_king.png",
            "q_w": "white_queen.png",
            "q_b": "black_queen.png",
            "b_w": "white_bishop.png",
            "b_b": "black_bishop.png",
            "n_w": "white_knight.png",
            "n_b": "black_knight.png",
        }
        for key, filename in images.items():
            images[key] = pygame.image.load(f"{self.PICTURES_FOLDER}/{filename}")
            images[key] = pygame.transform.scale(images[key], (self.SQUARE_SIZE, self.SQUARE_SIZE))
        return images

    def setup(self):
        self.board = initBoardR()
        self.selected_piece = None
        self.selected_pos = None

    def draw_borders(self):
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (0, 0, self.SCREEN_WIDTH, self.BORDER_SIZE))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (0, self.SCREEN_HEIGHT - self.BORDER_SIZE, self.SCREEN_WIDTH, self.BORDER_SIZE))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (0, 0, self.BORDER_SIZE, self.SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (self.SCREEN_WIDTH - self.BORDER_SIZE - self.HISTORY_WIDTH, 0, self.BORDER_SIZE, self.SCREEN_HEIGHT))

    def draw_grid(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.COLORS[(row + col) % 2]
                pygame.draw.rect(
                    self.screen, color,
                    (col * self.SQUARE_SIZE + self.BORDER_SIZE, row * self.SQUARE_SIZE + self.BORDER_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_coordinates(self):
        for col in range(self.BOARD_SIZE):
            label = self.font.render(chr(ord("a") + col), True, (255, 255, 255))
            self.screen.blit(label, (col * self.SQUARE_SIZE + self.BORDER_SIZE + self.SQUARE_SIZE // 3, self.SCREEN_HEIGHT - self.BORDER_SIZE + 4))

        for row in range(self.BOARD_SIZE):
            label = self.font.render(str(8 - row), True, (255, 255, 255))
            self.screen.blit(label, (8, row * self.SQUARE_SIZE + self.BORDER_SIZE + self.SQUARE_SIZE // 3))

    def draw_board(self):
        self.draw_borders()
        self.draw_grid()
        self.draw_coordinates()

    def draw_piece(self, piece, x, y):
        img_key = f"{piece.name.lower()}_{'w' if piece.color == Color.white else 'b'}"
        self.screen.blit(self.IMAGES[img_key], (x, y))

    def draw_pieces(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    self.draw_piece(piece, col * self.SQUARE_SIZE + self.BORDER_SIZE, row * self.SQUARE_SIZE + self.BORDER_SIZE)

    def highlight_square(self, x, y, highlight_color):
        pygame.draw.rect(
            self.screen, highlight_color,
            (x * self.SQUARE_SIZE + self.BORDER_SIZE, y * self.SQUARE_SIZE + self.BORDER_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_moves(self, piece):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if piece.possibleMoves[row][col] == "1":
                    square_color = self.COLORS[(row + col) % 2]
                    highlight_color = self.HIGHLIGHT_COLOR_LIGHT if square_color == self.COLORS[0] else self.HIGHLIGHT_COLOR_DARK
                    self.highlight_square(col, row, highlight_color)

    def draw_cursor_highlight(self):
        if self.selected_piece:
            x, y = self.get_square_under_mouse()
            self.draw_moves(self.selected_piece)
            if x is not None and y is not None:
                square_color = self.COLORS[(y + x) % 2]
                highlight_color = self.HIGHLIGHT_CURSOUR_COLOR_LIGHT if square_color == self.COLORS[0] else self.HIGHLIGHT_CURSOUR_COLOR_DARK
                self.highlight_square(x, y, highlight_color)

    def draw_move_history_background(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (self.SCREEN_WIDTH - (self.HISTORY_WIDTH + self.BORDER_SIZE), 0, self.HISTORY_WIDTH, self.SCREEN_HEIGHT))

    def draw_move_history_title(self):
        title = self.font.render("Move History", True, (255, 255, 255))
        self.screen.blit(title, (self.SCREEN_WIDTH - (self.HISTORY_WIDTH + self.BORDER_SIZE) + 10, 10))

    def draw_move_history_entries(self):
        for i, move in enumerate(self.move_history):
            y_position = 40 + i * 20 - self.history_scroll_offset
            if 25 <= y_position < self.SCREEN_HEIGHT:  # Draw only visible moves
                move_text = self.font.render(move, True, (255, 255, 255))
                self.screen.blit(move_text, (self.SCREEN_WIDTH - (self.HISTORY_WIDTH + self.BORDER_SIZE) + 10, y_position))

    def draw_move_history(self):
        self.draw_move_history_background()
        self.draw_move_history_title()
        self.draw_move_history_entries()

    def get_square_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = (mouse_pos[0] - self.BORDER_SIZE) // self.SQUARE_SIZE, (mouse_pos[1] - self.BORDER_SIZE) // self.SQUARE_SIZE
        if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
            return x, y
        return None, None

    def handle_mouse_button_down(self):
        x, y = self.get_square_under_mouse()
        if x is not None and y is not None:
            selected_piece = self.board[y][x]
            if isinstance(selected_piece, Piece) and selected_piece.color == self.current_turn:
                self.selected_piece = selected_piece
                self.selected_pos = (y, x)
                self.selected_piece.possibleMoves = restrictImpossibleMoves(self.board, self.selected_piece, y, x)

    def handle_mouse_button_up(self):
        if self.selected_piece:
            new_x, new_y = self.get_square_under_mouse()
            if new_x is not None and new_y is not None and self.selected_piece.possibleMoves[new_y][new_x] == "1":
                self.previous_states.append([row[:] for row in self.board])
                self.write_in_history(new_x,new_y)
                self.board[self.selected_pos[0]][self.selected_pos[1]] = "_"
                self.board[new_y][new_x] = self.selected_piece
                self.selected_piece.has_moved = 1

                self.current_turn = Color.black if self.current_turn == Color.white else Color.white

            self.selected_piece.possibleMoves = clearMap(self.selected_piece.possibleMoves)
            self.selected_piece = None
            self.selected_pos = None
    
    def write_in_history(self,new_x,new_y):
        piece_symbol = self.selected_piece.name.upper() if self.selected_piece.name != "p" else ""
        move_notation = f"{piece_symbol}{chr(ord('a') + new_x)}{8 - new_y}"
        if self.board[new_y][new_x] != "_":
                move_notation = f"{piece_symbol}x{chr(ord('a') + new_x)}{8 - new_y}"
        self.move_history.append(move_notation)     
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up()
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)

    def handle_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.scene_manager.switch_scene("MainMenuScene")
        elif event.key == pygame.K_u and self.previous_states:
            self.board = self.previous_states.pop()
            self.move_history.pop()
            self.current_turn = Color.black if self.current_turn == Color.white else Color.white
        elif event.key == pygame.K_UP:
            self.history_scroll_offset = max(0, self.history_scroll_offset - self.HISTORY_SCROLL_STEP)
        elif event.key == pygame.K_DOWN:
            self.history_scroll_offset += self.HISTORY_SCROLL_STEP

    def cleanup(self):
        pass

    def update(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw_board()
        self.draw_cursor_highlight()
        self.draw_pieces()
        self.draw_move_history()
        pygame.display.flip()
        self.clock.tick(60)
