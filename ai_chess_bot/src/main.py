"""
main.py
----------
Main entry point for Royal Gambit.
"""
import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from piece import King
from menu import StartMenu  # Import the StartMenu class

class Main:
    
    def __init__(self):
        pygame.init()
        # Start in menu mode, so the display starts at WIDTH x HEIGHT.
        self.current_mode = 'menu'  # either 'menu' or 'game'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Royal Gambit')
        self.game = Game()
        self.menu = StartMenu(self.screen)  # Initialize the start menu

    def switch_mode(self, mode):
        if mode == 'menu':
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        elif mode == 'game':
            self.screen = pygame.display.set_mode((WIDTH + 210, HEIGHT))
        self.current_mode = mode

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            if self.menu.menu_active:
                # If we are not already in menu mode, switch to it.
                if self.current_mode != 'menu':
                    self.switch_mode('menu')
                self.screen.fill((0, 0, 0))
                self.menu.draw_menu()
                action = self.menu.handle_menu_events()

                if action == 'Start Game':
                    self.menu.menu_active = False
                    self.game.reset()
                    self.game.ai_enabled = False  # Disable AI
                    self.game.config.start_sound.play()
                    self.switch_mode('game')
                elif action == 'Play vs AI':
                    difficulty = self.menu.select_difficulty()
                    # If escape was pressed during difficulty selection, difficulty will be None.
                    if difficulty is None:
                        # Simply continue the loop so that the main menu remains active.
                        continue
                    self.game.ai.set_difficulty(difficulty.lower())
                    self.menu.menu_active = False
                    self.game.reset()
                    self.game.ai_enabled = True  # Enable AI
                    self.game.config.start_sound.play()
                    self.switch_mode('game')
                elif action == 'Controls':
                    self.menu.show_instructions()
                elif action == 'Exit':
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
            else:
                # We are in game mode.
                if self.current_mode != 'game':
                    self.switch_mode('game')
                screen = self.screen
                game = self.game
                board = self.game.board
                dragger = self.game.dragger

                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                if game.ai_enabled and game.next_player == game.ai.color and not game.game_over:
                    pygame.display.update()
                    pygame.time.wait(500)
                    best_move = game.ai.eval(game.board)
                    if best_move:
                        piece = board.squares[best_move.initial.row][best_move.initial.col].piece
                        board.move(piece, best_move)
                        game.move_log.append(best_move)
                        game.next_turn()
                        game.play_sound(captured=board.squares[best_move.final.row][best_move.final.col].has_piece())

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE
                        game.set_hover(motion_row, motion_col)
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):
                                if isinstance(dragger.piece, King) and abs(dragger.initial_col - released_col) == 2:
                                    board.move(dragger.piece, move)
                                    game.config.castle_sound.play()
                                else:
                                    captured = board.squares[released_row][released_col].has_piece()
                                    board.move(dragger.piece, move)
                                    board.set_true_en_passant(dragger.piece)
                                    game.play_sound(captured)
                                game.move_log.append(move)
                                game.next_turn()
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                        dragger.undrag_piece()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.game.reset()
                        elif event.key == pygame.K_ESCAPE:
                            self.menu.menu_active = True
                            self.switch_mode('menu')
                        elif event.key == pygame.K_t:
                            self.game.change_theme()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Draw the move log and game over text only in game mode.
                game.draw_move_log(screen)
                game.check_game_over(screen)

                pygame.display.update()
            clock.tick(60)

main = Main()
main.mainloop()
