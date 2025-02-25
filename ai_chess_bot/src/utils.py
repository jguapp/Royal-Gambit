"""
utils.py
----------
Utility functions for Royal Gambit.
"""

from PIL import Image
import pygame

def load_gif_frames(filename):
    frames = []
    gif = Image.open(filename)
    try:
        while True:
            frame = gif.copy().convert('RGBA')
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            py_image = pygame.transform.scale(py_image, (pygame.display.get_surface().get_width(),
                                                           pygame.display.get_surface().get_height()))
            frames.append(py_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames
