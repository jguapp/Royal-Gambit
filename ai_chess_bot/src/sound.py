"""
sound.py
----------
Sound class for Royal Gambit.
"""

import pygame

class Sound:
    def __init__(self, path):
        self.path = path
        # Load the sound file using pygame mixer
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        # Play the loaded sound effect
        pygame.mixer.Sound.play(self.sound)
