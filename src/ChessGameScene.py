import pygame
import sys
from piece import *
from vboard import *
from movement_matrix import *
from movement_restrictions import *
from button import Button
import copy

class ChessGameScene:
    def __init__(self, screen, scene_manager, custom_board=None):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont("Arial", 20)
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
        self.PICTURES_FOLDER = "pictures/pieces"
        self.IMAGES = self.load_images()
        self.custom_board = custom_board
        self.cursor = pygame.image.load("pictures/cursor.png")
        self.exit_button = Button(
            (self.screen.get_width() - 200), self.screen.get_height() - 80, 200, 80, "",
            "pictures/Pictures_button/exit_button.png", "pictures/Pictures_button/exit1_button.png", "audio/knopka-vyiklyuchatelya1.mp3"
        )
        self.dragging_piece = None  # Currently dragged piece
        self.dragging_piece_pos = (0, 0)  # Position of the dragged piece

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
        self.board = None
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = Color.white
        self.move_history = []
        self.previous_states = []
        self.history_scroll_offset = 0
        self.clock = pygame.time.Clock()
        if self.custom_board is None:
            self.board = initBoardR()
        else:
            self.board = copy.deepcopy(self.custom_board)

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
                if isinstance(piece, Piece) and piece != self.dragging_piece:
                    self.draw_piece(piece, col * self.SQUARE_SIZE + self.BORDER_SIZE, row * self.SQUARE_SIZE + self.BORDER_SIZE)

    def highlight_square(self, x, y, highlight_color):
        pygame.draw.rect(
            self.screen, highlight_color,
            (x * self.SQUARE_SIZE + self.BORDER_SIZE, y * self.SQUARE_SIZE + self.BORDER_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_moves(self, piece):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if piece.possibleMoves[row][col] != "0":
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
            if 25 <= y_position < self.SCREEN_HEIGHT - 80:
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
                self.dragging_piece = selected_piece  # Start dragging
                self.dragging_piece_pos = pygame.mouse.get_pos()

    def handle_mouse_button_up(self):
        if self.selected_piece:
            new_x, new_y = self.get_square_under_mouse()
            if new_x is not None and new_y is not None:
                move_type = self.selected_piece.possibleMoves[new_y][new_x]

                if move_type in {"1", "2"}:
                    self.previous_states.append({
                        "board": [row[:] for row in self.board],
                        "has_moved": [[piece.has_moved if isinstance(piece, Piece) else None for piece in row] for row in self.board]
                    })

                    if move_type == "2":
                        if isinstance(self.selected_piece, Pawn) and abs(new_x - self.selected_pos[1]) == 1:
                            self.board = executeEnPassant(self.board, self.selected_pos[0], self.selected_pos[1], new_y, new_x)
                            self.write_in_history(new_x, new_y, special="e.p.")
                        elif isinstance(self.selected_piece, Piece) and abs(new_x - self.selected_pos[1]) == 2:
                            direction = "left" if new_x < self.selected_pos[1] else "right"
                            self.board = executeCastle(self.board, self.selected_pos[0], self.selected_pos[1], direction)
                            self.write_in_history(new_x, new_y, special="O-O" if direction == "right" else "O-O-O")
                    else:
                        self.write_in_history(new_x, new_y)
                        self.board[self.selected_pos[0]][self.selected_pos[1]] = "_"
                        self.board[new_y][new_x] = self.selected_piece

                    if isinstance(self.selected_piece, Pawn):
                        for row in self.board:
                            for cell in row:
                                if isinstance(cell, Pawn):
                                    cell.justMovedTwo = False
                        if abs(new_y - self.selected_pos[0]) == 2:
                            self.selected_piece.justMovedTwo = True

                    self.selected_piece.has_moved = True
                    self.current_turn = Color.black if self.current_turn == Color.white else Color.white

                self.selected_piece.possibleMoves = clearMap(self.selected_piece.possibleMoves)

            self.selected_piece = None
            self.dragging_piece = None  # Stop dragging

    def write_in_history(self, new_x, new_y, special=None):
        piece_symbol = self.selected_piece.name.upper() if self.selected_piece.name != "p" else ""
        move_notation = f"{piece_symbol}{chr(ord('a') + new_x)}{8 - new_y}"
        if self.board[new_y][new_x] != "_":
            move_notation = f"{piece_symbol}x{chr(ord('a') + new_x)}{8 - new_y}"
        if special:
            move_notation = special
        self.move_history.append(move_notation)

    def handle_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.scene_manager.switch_scene("MainMenuScene")
        elif event.key == pygame.K_u and self.previous_states:
            last_state = self.previous_states.pop()
            self.board = last_state["board"]
            for row_idx, row in enumerate(self.board):
                for col_idx, piece in enumerate(row):
                    if isinstance(piece, Piece):
                        piece.has_moved = last_state["has_moved"][row_idx][col_idx]
            self.move_history.pop()
            self.current_turn = Color.black if self.current_turn == Color.white else Color.white
        elif event.key == pygame.K_UP:
            self.history_scroll_offset = max(0, self.history_scroll_offset - self.HISTORY_SCROLL_STEP)
        elif event.key == pygame.K_DOWN:
            self.history_scroll_offset += self.HISTORY_SCROLL_STEP

    def display_winner_popup(self, winner):
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        popup_font = pygame.font.SysFont("Arial", 50)
        text = f"{winner} Wins!"
        text_surface = popup_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_custom_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor, (mouse_pos[0] - self.cursor.get_width() // 2, mouse_pos[1] - self.cursor.get_height() // 2))

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.exit_button.check_hover(mouse_pos)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down()
            if self.exit_button.is_clicked(event.pos):
                self.scene_manager.switch_scene("MainMenuScene")
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up()
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)

    def cleanup(self):
        pass

    def update(self):
        for event in pygame.event.get():
            self.handle_event(event)
        if self.dragging_piece:
            self.dragging_piece_pos = pygame.mouse.get_pos()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw_board()
        self.draw_cursor_highlight()
        self.draw_pieces()
        if self.dragging_piece:
            mouse_x, mouse_y = self.dragging_piece_pos
            img_key = f"{self.dragging_piece.name.lower()}_{'w' if self.dragging_piece.color == Color.white else 'b'}"
            self.screen.blit(self.IMAGES[img_key], (mouse_x - self.SQUARE_SIZE // 2, mouse_y - self.SQUARE_SIZE // 2))
        self.draw_move_history()
        self.exit_button.draw(self.screen)
        if isMate(self.board, self.current_turn):
            winner = "White" if self.current_turn == Color.black else "Black"
            self.display_winner_popup(winner)
        self.draw_custom_cursor()
        pygame.display.flip()
        self.clock.tick(60)
