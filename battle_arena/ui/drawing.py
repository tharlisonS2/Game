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
    
# Modified version of CHARACTER CREATION in ui/screens.py
def draw_character_creation(surface, buttons, input_name, current_stats, total_points, fonts):
    """Draw the character creation screen with stat distribution"""
    # Background
    surface.fill((30, 30, 50))
    
    # Title
    title_text = fonts['title'].render("CHARACTER CREATION", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 60))
    surface.blit(title_text, title_rect)
    
    # Name input box
    pygame.draw.rect(surface, WHITE, (WIDTH/2 - 150, 140, 300, 40), 2)
    name_label = fonts['medium'].render("Character Name:", True, WHITE)
    surface.blit(name_label, (WIDTH/2 - 150, 110))
    
    # Display entered name
    name_text = fonts['medium'].render(input_name, True, WHITE)
    surface.blit(name_text, (WIDTH/2 - 140, 150))
    
    # Calculate remaining points
    used_points = sum(current_stats.values())
    remaining_points = total_points - used_points
    
    # Stat distribution title
    stat_title = fonts['medium'].render(f"Distribute Stat Points: {remaining_points} remaining", True, WHITE)
    surface.blit(stat_title, (WIDTH/2 - 150, 200))
    
    # Stat explanations
    stat_explanations = {
        'strength': "Increases damage and health",
        'agility': "Improves accuracy and stamina",
        'defense': "Reduces damage taken"
    }
    
    # Draw stat distribution bars and values
    y_position = 240
    for i, (stat, value) in enumerate(current_stats.items()):
        # Stat name and value
        stat_text = fonts['medium'].render(f"{stat.capitalize()}: {value}", True, GOLD)
        surface.blit(stat_text, (WIDTH/2 - 150, y_position))
        
        # + and - buttons
        # Minus button (only enabled if value > 0)
        minus_color = RED if value > 0 else GRAY
        pygame.draw.rect(surface, minus_color, (WIDTH/2 - 180, y_position, 25, 25))
        minus_text = fonts['medium'].render("-", True, WHITE)
        minus_rect = minus_text.get_rect(center=(WIDTH/2 - 167, y_position + 12))
        surface.blit(minus_text, minus_rect)
        
        # Plus button (only enabled if remaining points > 0)
        plus_color = GREEN if remaining_points > 0 else GRAY
        pygame.draw.rect(surface, plus_color, (WIDTH/2 + 20, y_position, 25, 25))
        plus_text = fonts['medium'].render("+", True, WHITE)
        plus_rect = plus_text.get_rect(center=(WIDTH/2 + 32, y_position + 12))
        surface.blit(plus_text, plus_rect)
        
        # Stat explanation
        explanation = fonts['small'].render(stat_explanations[stat], True, WHITE)
        surface.blit(explanation, (WIDTH/2 + 50, y_position))
        
        y_position += 50
    
    # Stat point info
    points_text = fonts['medium'].render(
        f"You have {remaining_points} points remaining", 
        True, 
        WHITE if remaining_points > 0 else RED
    )
    surface.blit(points_text, (WIDTH/2 - 150, y_position))
    
    # Draw create button
    create_button = pygame.Rect(WIDTH/2 - 100, y_position + 40, 200, 50)
    button_color = GREEN if remaining_points == 0 else GRAY  # Only enabled if all points are spent
    pygame.draw.rect(surface, button_color, create_button)
    pygame.draw.rect(surface, BLACK, create_button, 2)  # Border
    
    create_text = fonts['medium'].render("Create Character", True, WHITE)
    create_rect = create_text.get_rect(center=create_button.center)
    surface.blit(create_text, create_rect)