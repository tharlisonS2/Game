import pygame
from constants import BLACK, WHITE, BLUE, GRAY, GOLD

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GOLD, disabled_color=(100, 100, 100), font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.color = color
        self.is_hovered = False
        self.is_disabled = False
        # Use a more thematic font (replace with a custom font if available)
        self.font = pygame.font.SysFont('Times New Roman', font_size, bold=True)
        self.scale = 1.0  # For hover animation
        self.alpha = 255  # For click feedback

    def draw(self, surface):
        # Adjust color based on state
        if self.is_disabled:
            color = self.disabled_color
        else:
            color = self.hover_color if self.is_hovered else self.base_color

        # Create a temporary surface for the button
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        button_surface.set_alpha(self.alpha)

        # Draw rounded rectangle with gradient effect
        pygame.draw.rect(button_surface, color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        
        # Add a subtle border
        pygame.draw.rect(button_surface, WHITE, (0, 0, self.rect.width, self.rect.height), 2, border_radius=10)

        # Add a shadow effect when hovered
        if self.is_hovered and not self.is_disabled:
            shadow_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
            pygame.draw.rect(button_surface, shadow_color, (2, 2, self.rect.width - 4, self.rect.height - 4), border_radius=8)

        # Render text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        button_surface.blit(text_surface, text_rect)

        # Scale for hover effect
        if self.is_hovered and not self.is_disabled:
            scale = 1.05
            scaled_size = (int(self.rect.width * scale), int(self.rect.height * scale))
            button_surface = pygame.transform.smoothscale(button_surface, scaled_size)
            scaled_rect = button_surface.get_rect(center=self.rect.center)
            surface.blit(button_surface, scaled_rect.topleft)
        else:
            surface.blit(button_surface, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        if self.is_disabled:
            return False
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            self.alpha = 200  # Brief transparency for click feedback
            return True
        self.alpha = 255
        return False

    def set_disabled(self, disabled):
        self.is_disabled = disabled
        self.color = self.disabled_color if disabled else self.base_color