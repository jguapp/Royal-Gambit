"""
piece.py
----------
Defines chess piece classes for Royal Gambit.
"""

import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        # Adjust value sign based on color (white positive, black negative)
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []  # List of valid moves
        self.moved = False  # Track if piece has been moved
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        # Set the image path for the piece texture based on its name and color
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

# Specific piece classes with personalized initialization
class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1  # Direction of movement based on color
        self.en_passant = False
        super().__init__('pawn', color, 1.0)

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        # Store references for castling later on
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)
