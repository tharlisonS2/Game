# ui/drawing.py
import pygame
from constants import BLACK, RED, GREEN, BROWN, BLUE, GOLD, WHITE, WIDTH, HEIGHT

# Initialize fonts
def init_fonts():
    fonts = {
        'small': pygame.font.SysFont('Arial', 18),
        'medium': pygame.font.SysFont('Arial', 24),
        'large': pygame.font.SysFont('Arial', 32),
        'title': pygame.font.SysFont('Arial', 48, bold=True)
    }
    return fonts

def draw_health_bar(surface, x, y, width, height, value, max_value, border_color=BLACK, back_color=RED, fill_color=GREEN):
    """Draw a health or stamina bar with border"""
    # Draw background
    pygame.draw.rect(surface, back_color, (x, y, width, height))
    
    # Draw fill amount
    fill_width = int(width * (value / max_value))
    pygame.draw.rect(surface, fill_color, (x, y, fill_width, height))
    
    # Draw border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

def draw_battle_arena(surface, player, enemy, battle_log, fonts):
    """Draw the battle arena screen"""
    # Background
    surface.fill((50, 50, 100))  # Dark blue background for arena
    
    # Ground
    pygame.draw.rect(surface, BROWN, (0, 400, WIDTH, 200))
    
    # Draw characters
    player.draw(surface)
    enemy.draw(surface)
    
    # Battle log (last 5 messages)
    log_height = 150
    log_rect = pygame.Rect(50, HEIGHT - log_height - 20, WIDTH - 100, log_height)
    pygame.draw.rect(surface, (0, 0, 0, 180), log_rect)  # Semi-transparent background
    pygame.draw.rect(surface, WHITE, log_rect, 2)  # Border
    
    # Display the log messages
    for i, msg in enumerate(battle_log[-5:]):
        text = fonts['small'].render(msg, True, WHITE)
        surface.blit(text, (log_rect.x + 10, log_rect.y + 10 + i * 25))
    
    # Draw battle HUD
    title_text = fonts['large'].render("BATTLE", True, WHITE)
    title_rect = title_text.get_rect(midtop=(WIDTH/2, 20))
    surface.blit(title_text, title_rect)
    
    # Player stats
    player_level = fonts['small'].render(f"Lvl: {player.level}", True, WHITE)
    surface.blit(player_level, (20, 20))
    
    # Enemy level
    enemy_level = fonts['small'].render(f"Lvl: {enemy.level}", True, WHITE)
    level_rect = enemy_level.get_rect(topright=(WIDTH-20, 20))
    surface.blit(enemy_level, level_rect)