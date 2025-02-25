"""
config.py
----------
Royal Gambit configuration settings.
"""

import pygame
import os
from sound import Sound
from theme import Theme

class Config:
    def __init__(self):
        # List of available themes for the game board
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        # Set up a custom font (monospace) for board labels
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        # Load sounds for various game actions
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
        self.castle_sound = Sound(os.path.join('assets/sounds/castle.wav'))
        self.promote_sound = Sound(os.path.join('assets/sounds/promote.wav'))
        self.start_sound = Sound(os.path.join('assets/sounds/start.wav'))
        self.check_sound = Sound(os.path.join('assets/sounds/check.wav'))
        self.checkmate_sound = Sound(os.path.join('assets/sounds/checkmate.wav'))

    def change_theme(self):
        # Cycle through available themes
        self.idx = (self.idx + 1) % len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        # Personalized themes created by Joel for Royal Gambit.
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        purple = Theme((220, 200, 255), (130, 90, 190), (180, 140, 240), (110, 70, 160), '#C86464', '#C84646')
        red = Theme((240, 128, 128), (165, 42, 42), (255, 99, 71), (139, 0, 0), '#C86464', '#C84646')
        yellow = Theme((255, 223, 100), (204, 153, 0), (255, 200, 50), (153, 102, 0), '#C86464', '#C84646')
        orange = Theme((255, 200, 150), (200, 120, 50), (255, 180, 100), (180, 90, 30), '#C86464', '#C84646')
        pink = Theme((255, 200, 220), (220, 120, 150), (255, 170, 190), (180, 90, 120), '#C86464', '#C84646')
        cyan = Theme((200, 255, 255), (90, 170, 170), (140, 210, 210), (60, 140, 140), '#C86464', '#C84646')
        teal = Theme((180, 240, 200), (60, 140, 110), (120, 190, 160), (40, 110, 90), '#C86464', '#C84646')

        self.themes = [green, brown, blue, purple, red, yellow, orange, pink, cyan, teal]
