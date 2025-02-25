"""
ai.py
----------
Chess engine AI for Royal Gambit. Implements minimax algorithm with alpha-beta pruning.
"""

import copy, math, random

from const import *
from piece import *
from book import Book

class AI:

    def __init__(self, engine='book', depth=3):
        self.engine = engine
        self.depth = depth
        self.book = Book()
        self.color = 'black'
        self.game_moves = []
        self.explored = 0
        
    def set_difficulty(self, level):
        self.difficulty = level
        if level == 'easy':
            self.depth = 2
        elif level == 'medium':
            self.depth = 4
        elif level == 'hard':
            self.depth = 6
        elif level == 'expert':
            self.depth = 8
        else:
            self.depth = 4

    def book_move(self):
        move = self.book.next_move(self.game_moves, weighted=True)
        return move

    # -------
    # MINIMAX
    # -------

    def heatmap(self, piece, row, col):
        hmp = 0
        if piece.name == 'pawn':
            if piece.color == 'black':
                hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
                ]
            elif piece.color == 'white':
                hmp = [ 
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                ]

        elif piece.name == 'knight':
            hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                    [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                    [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                    [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                    [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                    [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        elif piece.name == 'bishop':
            hmp = [ 
                    [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
                    [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                    [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                    [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                    [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                    [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                    [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                    [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
            ]
        
        elif piece.name == 'king':
            if piece.color == 'black':
                hmp = [ 
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                ]
            
            elif piece.color == 'white':
                hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                ]

        else:
            hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        eval = -hmp[row][col] if piece.color == 'black' else hmp[row][col]
        return eval

    def threats(self, board, piece):
        eval = 0
        for move in piece.moves:
            attacked = board.squares[move.final.row][move.final.col]
            if attacked.has_piece():
                if attacked.piece.color != piece.color:
                    # checks
                    if attacked.piece.name == 'king':
                        eval += attacked.piece.value / 10500
                    
                    # threat
                    else:
                        eval += attacked.piece.value / 45

        return eval

    def static_eval(self, board):
        # var
        eval = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    # piece
                    piece = board.squares[row][col].piece
                    # white - black
                    eval += piece.value
                    # heatmap
                    eval += self.heatmap(piece, row, col)
                    # moves
                    if piece.name != 'queen': 
                        eval += 0.01 * len(piece.moves)
                    else: 
                        eval += 0.003 * len(piece.moves)
                    # checks
                    eval += self.threats(board, piece)
        
        eval = round(eval, 5)
        return eval

    def get_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    board.calc_moves(square.piece, row, col)
                    moves += square.piece.moves
        
        return moves

    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0:
            return self.static_eval(board), None  # eval, move
        
        if maximizing:
            max_eval = -math.inf
            best_move = None
            moves = self.get_moves(board, 'white')
            for move in moves:
                self.explored += 1
                temp_board = copy.deepcopy(board)
                # Retrieve the piece from the deep-copied board
                piece = temp_board.squares[move.initial.row][move.initial.col].piece
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, False, alpha, beta)[0]  # eval, move
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha: 
                    break

            if best_move is None:
                best_move = moves[0]
            return max_eval, best_move  # eval, move
        
        else:
            min_eval = math.inf
            best_move = None
            moves = self.get_moves(board, 'black')
            for move in moves:
                self.explored += 1
                temp_board = copy.deepcopy(board)
                # Retrieve the piece from the deep-copied board
                piece = temp_board.squares[move.initial.row][move.initial.col].piece
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, True, alpha, beta)[0]  # eval, move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha: 
                    break
            
            if best_move is None:
                best_move = random.choice(moves)
            return min_eval, best_move  # eval, move

    # MAIN EVAL
    
    def eval(self, main_board):
        self.explored = 0

        # add last move
        last_move = main_board.last_move
        self.game_moves.append(last_move)

        # book engine
        if self.engine == 'book':
            move = self.book_move()

            # no more book moves ?
            if move is None:
                self.engine = 'minimax'

        # minimax engine
        if self.engine == 'minimax':
            print('\nFinding best move...')
            eval, move = self.minimax(main_board, self.depth, False, -math.inf, math.inf)
            print('\n- Initial eval:', self.static_eval(main_board))
            print('- Final eval:', eval)
            print('- Boards explored', self.explored)
            if eval >= 5000: 
                print('* White MATE!')
            if eval <= -5000: 
                print('* Black MATE!')
            
        self.game_moves.append(move)
        return move
