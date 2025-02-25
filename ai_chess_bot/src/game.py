"""
game.py
----------
Core game loop and rendering for Royal Gambit.
"""

import pygame

from ai import AI
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.dragger = Dragger()
        self.config = Config()
        self.move_log = []      # list of moves made during the game
        self.game_over = False  # flag for game over

    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                center = (move.final.col * SQSIZE + SQSIZE // 2, move.final.row * SQSIZE + SQSIZE // 2)
                radius = SQSIZE // 7
                circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (211, 211, 211, 150), (radius, radius), radius)
                surface.blit(circle_surface, (center[0] - radius, center[1] - radius))

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()

    # Updated helper: converts a move to algebraic notation with a space between the starting square and ending square.
    def move_to_notation(self, move):
        initial_file = chr(ord('a') + move.initial.col)
        initial_rank = str(8 - move.initial.row)
        final_file = chr(ord('a') + move.final.col)
        final_rank = str(8 - move.final.row)
        # Return notation with a space between the squares (e.g., "e2 e4")
        return initial_file + initial_rank + " " + final_file + final_rank

    # Modified move log drawing method using chess notation.
    def draw_move_log(self, surface):
        move_log_panel_width = 210
        move_log_panel_height = HEIGHT
        move_log_area = pygame.Rect(WIDTH, 0, move_log_panel_width, move_log_panel_height)
        pygame.draw.rect(surface, (45, 45, 46), move_log_area)
        move_texts = []
        for i in range(0, len(self.move_log), 2):
            move_string = f'{i // 2 + 1}. {self.move_to_notation(self.move_log[i])}'
            if i + 1 < len(self.move_log):
                # Insert a space between white and black moves
                move_string += f' {self.move_to_notation(self.move_log[i + 1])}'
            move_texts.append(move_string)
        padding = 5
        line_spacing = 2
        text_y = padding
        font = pygame.font.SysFont('Arial', 14)
        for text in move_texts:
            text_object = font.render(text, True, (245, 245, 245))
            text_location = move_log_area.move(padding, text_y)
            surface.blit(text_object, text_location)
            text_y += text_object.get_height() + line_spacing

    # Draw endgame text with a shadow effect.
    def draw_endgame_text(self, surface, text):
        font = pygame.font.SysFont('Helvetica', 32, True, False)
        text_object = font.render(text, True, (128, 128, 128), (245, 255, 250))
        text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(
            WIDTH / 2 - text_object.get_width() / 2,
            HEIGHT / 2 - text_object.get_height() / 2
        )
        surface.blit(text_object, text_location)
        shadow = font.render(text, True, (0, 0, 0))
        surface.blit(shadow, text_location.move(2, 2))

    # Check for game over (using board's checkmate condition) and display message.
    def check_game_over(self, surface):
        if self.board.is_checkmate(self.next_player):
            self.game_over = True
            text = 'Black wins by checkmate' if self.next_player == 'white' else 'White wins by checkmate'
            self.draw_endgame_text(surface, text)

    def __str__(self):
        return "Game()"
