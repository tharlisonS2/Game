# ui/screens.py
import pygame
from constants import WHITE, GOLD, BLACK, RED, BLUE, WIDTH, HEIGHT

def draw_main_menu(surface, buttons, fonts):
    """Draw the main menu screen"""
    # Background
    surface.fill((30, 30, 50))  # Dark background
    
    # Title
    title_text = fonts['title'].render("BATTLE ARENA", True, GOLD)
    title_rect = title_text.get_rect(center=(WIDTH/2, 100))
    surface.blit(title_text, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_character_creation(surface, buttons, input_name, selected_class, fonts):
    """Draw the character creation screen"""
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
    
    # Class selection
    class_label = fonts['medium'].render("Select Class:", True, WHITE)
    surface.blit(class_label, (WIDTH/2 - 150, 200))
    
    # Class info
    if selected_class:
        class_info = {
            "Warrior": "High Strength and Health. Born for battle.",
            "Rogue": "High Speed. Masters of evasion and quick strikes.",
            "Knight": "High Armor. Well-protected defenders."
        }
        
        class_text = fonts['large'].render(selected_class, True, GOLD)
        surface.blit(class_text, (WIDTH/2 - 100, 240))
        
        # Class description
        desc = class_info.get(selected_class, "")
        desc_text = fonts['small'].render(desc, True, WHITE)
        surface.blit(desc_text, (WIDTH/2 - 150, 290))
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_arena_menu(surface, player, buttons, battles_won, fonts):
    """Draw the arena menu screen"""
    # Background
    surface.fill((50, 30, 30))  # Dark red background for arena menu
    
    # Title
    title_text = fonts['title'].render("ARENA MENU", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 60))
    surface.blit(title_text, title_rect)
    
    # Player basic info
    info_text = fonts['medium'].render(f"{player.name} (Level {player.level}) - Gold: {player.gold}", True, GOLD)
    info_rect = info_text.get_rect(center=(WIDTH/2, 120))
    surface.blit(info_text, info_rect)
    
    # Battles won
    battles_text = fonts['medium'].render(f"Battles Won: {battles_won}", True, WHITE)
    battles_rect = battles_text.get_rect(center=(WIDTH/2, 160))
    surface.blit(battles_text, battles_rect)
    
    # Health and Stamina bars
    bar_width = 300
    bar_height = 20
    
    # Health
    health_label = fonts['small'].render(f"Health: {player.health}/{player.max_health}", True, WHITE)
    surface.blit(health_label, (WIDTH/2 - bar_width/2, 190))
    draw_health_bar(surface, WIDTH/2 - bar_width/2, 210, bar_width, bar_height, 
                   player.health, player.max_health)
    
    # Stamina
    stamina_label = fonts['small'].render(f"Stamina: {player.stamina}/{player.max_stamina}", True, WHITE)
    surface.blit(stamina_label, (WIDTH/2 - bar_width/2, 240))
    draw_health_bar(surface, WIDTH/2 - bar_width/2, 260, bar_width, bar_height, 
                   player.stamina, player.max_stamina, fill_color=BLUE)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_character_stats(surface, player, button, fonts):
    """Draw the character stats screen"""
    # Background
    surface.fill((30, 50, 30))  # Dark green background for stats
    
    # Title
    title_text = fonts['title'].render("CHARACTER STATS", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 50))
    surface.blit(title_text, title_rect)
    
    # Character basic info
    info_text = fonts['large'].render(f"{player.name} - {player.character_class}", True, GOLD)
    info_rect = info_text.get_rect(center=(WIDTH/2, 100))
    surface.blit(info_text, info_rect)
    
    # Stats
    stats = [
        f"Level: {player.level}",
        f"Experience: {player.experience}/{player.exp_to_level}",
        f"Health: {player.health}/{player.max_health}",
        f"Stamina: {player.stamina}/{player.max_stamina}",
        f"Strength: {player.strength}",
        f"Speed: {player.speed}",
        f"Armor: {player.armor}",
        f"Gold: {player.gold}",
        f"Weapon: {player.equipped_weapon} (Damage: {player.weapons[player.equipped_weapon]})",
        f"Armor: {player.equipped_armor} (Protection: {player.armor_items[player.equipped_armor]})"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = fonts['medium'].render(stat, True, WHITE)
        surface.blit(stat_text, (WIDTH/2 - 150, 150 + i * 30))
    
    # Skills
    skill_title = fonts['large'].render("Skills:", True, GOLD)
    surface.blit(skill_title, (WIDTH/2 - 150, 450))
    
    y_offset = 490
    for skill_name, skill_info in player.skills.items():
        skill_text = fonts['medium'].render(
            f"{skill_name}: Damage x{skill_info['damage']}, "
            f"Accuracy {int(skill_info['accuracy']*100)}%, "
            f"Cost {skill_info['stamina_cost']} stamina", 
            True, WHITE
        )
        surface.blit(skill_text, (WIDTH/2 - 150, y_offset))
        y_offset += 30
    
    # Draw back button
    button.draw(surface)

def draw_game_over(surface, player, battles_won, buttons, fonts):
    """Draw game over screen"""
    # Background
    surface.fill((10, 10, 10))  # Very dark background
    
    # Title
    title_text = fonts['title'].render("GAME OVER", True, RED)
    title_rect = title_text.get_rect(center=(WIDTH/2, 100))
    surface.blit(title_text, title_rect)
    
    # Stats
    stats_text = [
        f"Warrior: {player.name}",
        f"Level Reached: {player.level}",
        f"Battles Won: {battles_won}",
        f"Gold Earned: {player.gold}"
    ]
    
    for i, text in enumerate(stats_text):
        stat = fonts['medium'].render(text, True, WHITE)
        stat_rect = stat.get_rect(center=(WIDTH/2, 200 + i * 40))
        surface.blit(stat, stat_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

# Import from drawing.py to avoid circular dependency
from ui.drawing import draw_health_bar