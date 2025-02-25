"""
menu.py
----------
Main menu and UI components for Royal Gambit.
"""
import pygame
from const import WIDTH, HEIGHT
from utils import load_gif_frames
import sys

def render_text_with_outline(text, font, text_color, outline_color, outline_width):
    """
    Render text with an outline by drawing the text multiple times in the outline color.
    """
    base_text = font.render(text, True, text_color)
    w, h = base_text.get_size()
    outline_surface = pygame.Surface((w + 2 * outline_width, h + 2 * outline_width), pygame.SRCALPHA)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            offset_pos = (dx + outline_width, dy + outline_width)
            outline_surface.blit(font.render(text, True, outline_color), offset_pos)
    outline_surface.blit(base_text, (outline_width, outline_width))
    return outline_surface

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        # Load custom fonts
        self.menu_font = pygame.font.Font('assets/fonts/Cinzel-Regular.ttf', 50)
        self.title_font = pygame.font.Font('assets/fonts/Cinzel-Bold.ttf', 80)
        self.menu_active = True
        self.hovered_option = None
        self.menu_options = ['Start Game', 'Play vs AI', 'Controls', 'Exit']
        
        # Load animated background frames from a GIF
        self.bg_frames = load_gif_frames('assets/images/bg.gif')
        self.current_frame = 0
        self.frame_delay = 100  # milliseconds delay between frames
        self.last_frame_update = pygame.time.get_ticks()
        
        # Other animation parameters (for title/options)
        self.alpha = 0
        self.fade_speed = 5
        self.title_y = -100
        self.target_title_y = HEIGHT // 4
        self.title_slide_speed = 5
        self.options_offset = -300
        self.target_options_offset = 0
        self.options_slide_speed = 10

        # Decorative piece animation
        self.decorative_piece = pygame.image.load('assets/images/imgs-80px/black_knight.png')
        self.decorative_piece_rect = self.decorative_piece.get_rect()
        self.decorative_piece_rect.x = WIDTH - 150
        self.decorative_piece_rect.y = HEIGHT - 150
        self.piece_direction = 1

    def update(self):
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + self.fade_speed)
        if self.title_y < self.target_title_y:
            self.title_y += self.title_slide_speed
        if self.options_offset < self.target_options_offset:
            self.options_offset += self.options_slide_speed
        self.decorative_piece_rect.y += self.piece_direction
        if self.decorative_piece_rect.y > HEIGHT - 130 or self.decorative_piece_rect.y < HEIGHT - 170:
            self.piece_direction *= -1
        
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.last_frame_update = now

    def draw_menu(self):
        self.update()
        bg = self.bg_frames[self.current_frame]
        menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_surface.blit(bg, (0, 0))
        
        title_surface = render_text_with_outline('Royal Gambit', self.title_font, (255, 255, 255), (0, 0, 0), 2)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, self.title_y))
        menu_surface.blit(title_surface, title_rect)
        
        for i, option in enumerate(self.menu_options):
            text_color = (255, 255, 255)
            if self.hovered_option == option:
                text_color = (255, 223, 0)
            option_surface = render_text_with_outline(option, self.menu_font, text_color, (0, 0, 0), 2)
            option_rect = option_surface.get_rect(center=(WIDTH // 2 + self.options_offset, HEIGHT // 2 + i * 60))
            menu_surface.blit(option_surface, option_rect)
        
        menu_surface.blit(self.decorative_piece, self.decorative_piece_rect)
        menu_surface.set_alpha(self.alpha)
        self.screen.blit(menu_surface, (0, 0))
        pygame.display.update()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.handle_menu_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                return self.handle_menu_click(mouse_pos)
        return None

    def handle_menu_hover(self, mouse_pos):
        self.hovered_option = None
        for i, option in enumerate(self.menu_options):
            option_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + i * 60 - 25, 300, 50)
            if option_rect.collidepoint(mouse_pos):
                self.hovered_option = option
                break

    def handle_menu_click(self, mouse_pos):
        for i, option in enumerate(self.menu_options):
            option_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + i * 60 - 25, 300, 50)
            if option_rect.collidepoint(mouse_pos):
                return option
        return None

    def select_difficulty(self):
        """
        Display a difficulty selection screen with the animated GIF background,
        centered text, and highlight on hover. Returns the chosen difficulty.
        Pressing escape will cancel and return None to go back to the main menu.
        """
        difficulties = ['Easy', 'Medium', 'Hard']
        selected_difficulty = None
        while selected_difficulty is None:
            self.update()
            bg = self.bg_frames[self.current_frame]
            menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            menu_surface.blit(bg, (0, 0))
            
            # Render and center the title.
            font = pygame.font.Font('assets/fonts/Cinzel-Regular.ttf', 50)
            title_surface = render_text_with_outline("Select Difficulty", font, (255, 255, 255), (0, 0, 0), 2)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            menu_surface.blit(title_surface, title_rect)
            
            # Get the current mouse position for hover effect.
            mouse_pos = pygame.mouse.get_pos()
            for i, diff in enumerate(difficulties):
                text_color = (255, 255, 255)
                diff_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + i * 60 - 25, 300, 50)
                if diff_rect.collidepoint(mouse_pos):
                    text_color = (255, 223, 0)
                diff_surface = render_text_with_outline(diff, self.menu_font, text_color, (0, 0, 0), 2)
                diff_rect = diff_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                menu_surface.blit(diff_surface, diff_rect)
            
            self.screen.blit(menu_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(100)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, diff in enumerate(difficulties):
                        diff_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + i * 60 - 25, 300, 50)
                        if diff_rect.collidepoint(pos):
                            selected_difficulty = diff
                            break
        pygame.event.clear()
        print("Selected difficulty:", selected_difficulty)
        return selected_difficulty

    def show_instructions(self):
        self.screen.fill((30, 30, 30))
        instructions = [
            "Controls:",
            "1. Drag-and-drop on a square to move the selected piece.",
            "2. Press 'T' to change the theme.",
            "3. Press 'R' to reset the game.",
            "4. Press 'Esc' to return to the main menu."
        ]
        for i, line in enumerate(instructions):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            instruction_surface = self.menu_font.render(line, True, color)
            instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 + i * 50))
            self.screen.blit(instruction_surface, instruction_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
