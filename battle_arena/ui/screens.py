# ui/screens.py
import pygame
from constants import WHITE, GOLD, BLACK, RED, BLUE, WIDTH, HEIGHT
from ui.drawing import draw_health_bar, draw_battle_arena

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
        
def draw_pre_battle(surface, player, enemy, button, battle_timer, fonts):
    """Draw the pre-battle screen showing character stats comparison"""
    # Background
    surface.fill((30, 30, 80))  # Darker blue for pre-battle tension
    
    # Title
    title_text = fonts['title'].render("BATTLE PREPARATION", True, GOLD)
    title_rect = title_text.get_rect(center=(WIDTH/2, 50))
    surface.blit(title_text, title_rect)
    
    # Remove countdown timer section and replace with instruction
    instruction_text = fonts['medium'].render("Review stats and click 'Start Battle!' when ready", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH/2, HEIGHT - 120))
    surface.blit(instruction_text, instruction_rect)
    
    # Player Stats (Left side)
    player_title = fonts['large'].render(f"{player.name} (Level {player.level})", True, BLUE)
    surface.blit(player_title, (100, 120))
    
    # Enemy Stats (Right side)
    enemy_title = fonts['large'].render(f"{enemy.name} (Level {enemy.level})", True, RED)
    enemy_title_rect = enemy_title.get_rect(topright=(WIDTH - 100, 120))
    surface.blit(enemy_title, enemy_title_rect)
    
    # VS text in the middle
    vs_text = fonts['title'].render("VS", True, GOLD)
    vs_rect = vs_text.get_rect(center=(WIDTH/2, 120))
    surface.blit(vs_text, vs_rect)
    
    # Draw stat comparisons
    stats = [
        ("Health", player.health, player.max_health, enemy.health, enemy.max_health),
        ("Stamina", player.stamina, player.max_stamina, enemy.stamina, enemy.max_stamina),
        ("Strength", player.strength, player.strength, enemy.strength, enemy.strength),
        ("Speed", player.speed, player.speed, enemy.speed, enemy.speed),
        ("Armor", player.armor, player.armor, enemy.armor, enemy.armor)
    ]
    
    y_pos = 180
    for stat_name, p_val, p_max, e_val, e_max in stats:
        # Stat name in center
        stat_text = fonts['medium'].render(stat_name, True, WHITE)
        stat_rect = stat_text.get_rect(center=(WIDTH/2, y_pos))
        surface.blit(stat_text, stat_rect)
        
        # Player stat (left)
        if stat_name in ["Health", "Stamina"]:
            p_text = fonts['medium'].render(f"{p_val}/{p_max}", True, WHITE)
            draw_health_bar(surface, 100, y_pos + 25, 200, 15, p_val, p_max)
        else:
            p_text = fonts['medium'].render(f"{p_val}", True, WHITE)
        p_rect = p_text.get_rect(topleft=(100, y_pos))
        surface.blit(p_text, p_rect)
        
        # Enemy stat (right)
        if stat_name in ["Health", "Stamina"]:
            e_text = fonts['medium'].render(f"{e_val}/{e_max}", True, WHITE)
            e_rect = e_text.get_rect(topright=(WIDTH - 100, y_pos))
            surface.blit(e_text, e_rect)
            draw_health_bar(surface, WIDTH - 300, y_pos + 25, 200, 15, e_val, e_max)
        else:
            e_text = fonts['medium'].render(f"{e_val}", True, WHITE)
            e_rect = e_text.get_rect(topright=(WIDTH - 100, y_pos))
            surface.blit(e_text, e_rect)
        
        y_pos += 60
    
    # Battle tips
    tip_text = fonts['small'].render("Tip: Assess your opponent's strengths and weaknesses before planning your attack!", True, GOLD)
    tip_rect = tip_text.get_rect(center=(WIDTH/2, HEIGHT - 150))
    surface.blit(tip_text, tip_rect)
    
    # Start Battle button (more prominent)
    if button:
        button.draw(surface)
        
def draw_character_creation(surface, buttons, game_state, fonts):
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
    name_text = fonts['medium'].render(game_state.input_name, True, WHITE)
    surface.blit(name_text, (WIDTH/2 - 140, 150))
    
    # Stat distribution title
    stat_title = fonts['medium'].render(f"Distribute Stat Points: {game_state.get_remaining_points()} remaining", True, WHITE)
    surface.blit(stat_title, (WIDTH/2 - 150, 200))
    
    # Stat explanations
    stat_explanations = {
        'strength': "Increases damage and health",
        'speed': "Improves accuracy and stamina",
        'armor': "Reduces damage taken"
    }
    
    # Draw stat distribution bars and values
    y_position = 240
    for i, (stat, value) in enumerate(game_state.current_stats.items()):
        # Stat name and value
        stat_text = fonts['medium'].render(f"{stat.capitalize()}: {value}", True, GOLD)
        surface.blit(stat_text, (WIDTH/2 - 150, y_position))
        
        # Stat explanation
        explanation = fonts['small'].render(stat_explanations[stat], True, WHITE)
        surface.blit(explanation, (WIDTH/2 + 50, y_position))
        
        y_position += 50
    
    # Stat point info
    points_text = fonts['medium'].render(
        f"You have {game_state.get_remaining_points()} points remaining", 
        True, 
        WHITE if game_state.get_remaining_points() > 0 else RED
    )
    surface.blit(points_text, (WIDTH/2 - 150, y_position))
    
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
    info_text = fonts['large'].render(f"{player.name}", True, GOLD)
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