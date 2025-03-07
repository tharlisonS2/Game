import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Arena")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
GRAY = (150, 150, 150)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)

# Fonts
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)
font_title = pygame.font.SysFont('Arial', 48, bold=True)

# Game states
STATE_MAIN_MENU = 0
STATE_CHARACTER_CREATION = 1
STATE_BATTLE = 2
STATE_ARENA_MENU = 3
STATE_CHARACTER_STATS = 4
STATE_GAME_OVER = 5

# Character classes
WARRIOR = "Warrior"
ROGUE = "Rogue"
KNIGHT = "Knight"

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        text_surface = font_medium.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.max_health = 100
        self.health = self.max_health
        self.strength = 10
        self.speed = 10
        self.armor = 5
        self.gold = 50
        self.experience = 0
        self.exp_to_level = 100
        self.weapons = {"Rusty Sword": 5}
        self.equipped_weapon = "Rusty Sword"
        self.armor_items = {"Cloth Tunic": 2}
        self.equipped_armor = "Cloth Tunic"
        self.skills = {
            "Quick Strike": {"damage": 0.8, "accuracy": 0.9, "stamina_cost": 10},
            "Heavy Strike": {"damage": 1.5, "accuracy": 0.7, "stamina_cost": 20}
        }
        self.max_stamina = 100
        self.stamina = self.max_stamina
        
        # Apply class bonuses
        if character_class == WARRIOR:
            self.strength += 5
            self.max_health += 20
            self.health = self.max_health
        elif character_class == ROGUE:
            self.speed += 5
            self.armor += 2
        elif character_class == KNIGHT:
            self.armor += 5
            self.strength += 2
            
        # Animation state
        self.is_attacking = False
        self.attack_frame = 0
        self.is_hit = False
        self.hit_frame = 0
        self.position = (200, 300)  # Default position on screen
        self.color = (50, 100, 200)  # Player color
            
    def attack(self, enemy, skill_name):
        skill = self.skills[skill_name]
        
        # Check if enough stamina
        if self.stamina < skill["stamina_cost"]:
            return {"success": False, "message": f"{self.name} is too tired to use {skill_name}!"}
            
        # Consume stamina
        self.stamina -= skill["stamina_cost"]
        
        # Set animation state
        self.is_attacking = True
        self.attack_frame = 0
        
        # Calculate hit chance
        hit_chance = skill["accuracy"] * (self.speed / (self.speed + enemy.speed))
        
        if random.random() <= hit_chance:
            # Calculate damage
            weapon_damage = self.weapons[self.equipped_weapon]
            base_damage = self.strength + weapon_damage
            skill_modifier = skill["damage"]
            damage = int(base_damage * skill_modifier)
            
            # Apply armor reduction
            armor_value = enemy.armor_items[enemy.equipped_armor]
            damage_reduced = max(1, damage - armor_value - (enemy.armor // 2))
            
            # Apply damage
            enemy.health = max(0, enemy.health - damage_reduced)
            
            # Set enemy hit animation
            enemy.is_hit = True
            enemy.hit_frame = 0
            
            return {
                "success": True, 
                "hit": True, 
                "damage": damage_reduced,
                "message": f"{self.name} hits {enemy.name} with {skill_name} for {damage_reduced} damage!"
            }
        else:
            return {
                "success": True, 
                "hit": False, 
                "damage": 0,
                "message": f"{self.name}'s {skill_name} missed {enemy.name}!"
            }
            
    def rest(self):
        """Recover some stamina during a turn"""
        recovery = max(5, self.max_stamina // 10)  # Recover 10% of max stamina
        self.stamina = min(self.max_stamina, self.stamina + recovery)
        return {"message": f"{self.name} takes a moment to catch their breath. (+{recovery} stamina)"}
        
    def gain_experience(self, amount):
        """Gain experience and level up if enough is accumulated"""
        self.experience += amount
        result = {"message": f"{self.name} gained {amount} experience!"}
        
        if self.experience >= self.exp_to_level:
            levelup_msg = self.level_up()
            result["message"] += " " + levelup_msg
            result["levelup"] = True
        
        return result
    
    def level_up(self):
        self.level += 1
        self.experience -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        
        # Stat increases
        self.max_health += 10
        self.health = self.max_health
        self.strength += 2
        self.speed += 1
        self.armor += 1
        self.max_stamina += 10
        self.stamina = self.max_stamina
        
        return f"{self.name} has reached level {self.level}! Your attributes have increased!"
        
    def update_animation(self):
        # Update attack animation
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame > 10:  # Animation duration
                self.is_attacking = False
                self.attack_frame = 0
                
        # Update hit animation
        if self.is_hit:
            self.hit_frame += 1
            if self.hit_frame > 10:  # Animation duration
                self.is_hit = False
                self.hit_frame = 0
    
    def draw(self, surface):
        # Basic character representation (will be replaced with sprites in a full game)
        color = self.color
        
        # Flash red when hit
        if self.is_hit:
            color = RED if self.hit_frame % 2 == 0 else self.color
            
        # Position adjustment for attack animation
        position = list(self.position)
        if self.is_attacking:
            if self.attack_frame < 5:
                position[0] += self.attack_frame * 5  # Move forward
            else:
                position[0] -= (self.attack_frame - 5) * 5  # Move back
        
        # Draw character body (basic)
        pygame.draw.circle(surface, color, position, 30)  # Head
        pygame.draw.rect(surface, color, (position[0]-20, position[1]+30, 40, 60))  # Body
        
        # Draw weapon
        if self.is_attacking:
            weapon_color = BROWN
            pygame.draw.rect(surface, weapon_color, (position[0]+20, position[1]-10, 40, 10))
        
        # Draw health bar
        health_width = 60
        health_percent = self.health / self.max_health
        pygame.draw.rect(surface, RED, (position[0]-30, position[1]-50, health_width, 10))
        pygame.draw.rect(surface, GREEN, (position[0]-30, position[1]-50, int(health_width * health_percent), 10))
        
        # Draw stamina bar
        stamina_width = 60
        stamina_percent = self.stamina / self.max_stamina
        pygame.draw.rect(surface, GRAY, (position[0]-30, position[1]-38, stamina_width, 6))
        pygame.draw.rect(surface, BLUE, (position[0]-30, position[1]-38, int(stamina_width * stamina_percent), 6))
        
        # Draw name
        name_text = font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(position[0], position[1]-60))
        surface.blit(name_text, name_rect)

class Enemy(Character):
    def __init__(self, name, level):
        super().__init__(name, "Enemy")  # Reuse Character's init
        self.level = level
        self.max_health = 50 + (level * 10)
        self.health = self.max_health
        self.strength = 5 + (level * 2)
        self.speed = 5 + level
        self.armor = 2 + level
        self.equipped_weapon = "Claws"
        self.weapons = {self.equipped_weapon: 3 + level}
        self.equipped_armor = "Tough Skin"
        self.armor_items = {self.equipped_armor: 1 + (level // 2)}
        self.gold_reward = 10 + (level * 5)
        self.exp_reward = 20 + (level * 10)
        self.skills = {
            "Strike": {"damage": 1.0, "accuracy": 0.8, "stamina_cost": 10},
            "Fierce Attack": {"damage": 1.3, "accuracy": 0.6, "stamina_cost": 15}
        }
        self.max_stamina = 80
        self.stamina = self.max_stamina
        
        # Enemy position and color
        self.position = (600, 300)
        self.color = (200, 50, 50)
    
    def choose_action(self, player):
        """Enemy AI to choose an action"""
        if self.stamina < 15:  # If low on stamina
            return self.rest()
            
        # Choose attack based on health situation
        if self.health < self.max_health * 0.3:  # Low health, go for high damage
            if self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                return self.attack(player, "Fierce Attack")
            else:
                return self.attack(player, "Strike")
        else:  # Normal situation, randomize a bit
            if random.random() < 0.7:  # 70% chance for normal attack
                return self.attack(player, "Strike")
            else:
                if self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                    return self.attack(player, "Fierce Attack")
                else:
                    return self.attack(player, "Strike")

def generate_enemy(player_level):
    """Generate an appropriate enemy based on player level"""
    enemy_types = [
        "Goblin", "Bandit", "Wolf", "Skeleton", "Orc", 
        "Troll", "Dark Knight", "Shadow Assassin", "Ogre"
    ]
    
    # Choose enemy level based on player level
    enemy_level = max(1, player_level - 1 + random.randint(-1, 2))
    
    # Choose appropriate enemy type based on level
    if enemy_level <= 3:
        enemy_pool = enemy_types[:4]
    elif enemy_level <= 6:
        enemy_pool = enemy_types[2:7]
    else:
        enemy_pool = enemy_types[5:]
    
    enemy_name = random.choice(enemy_pool)
    
    # Add suffix for higher level enemies
    if enemy_level > 5:
        suffixes = ["the Strong", "the Fierce", "the Deadly", "the Brutal"]
        enemy_name += " " + random.choice(suffixes)
    
    return Enemy(enemy_name, enemy_level)

def draw_health_bar(surface, x, y, width, height, value, max_value, border_color=BLACK, back_color=RED, fill_color=GREEN):
    """Draw a health or stamina bar with border"""
    # Draw background
    pygame.draw.rect(surface, back_color, (x, y, width, height))
    
    # Draw fill amount
    fill_width = int(width * (value / max_value))
    pygame.draw.rect(surface, fill_color, (x, y, fill_width, height))
    
    # Draw border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

def draw_battle_arena(surface, player, enemy, battle_log):
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
        text = font_small.render(msg, True, WHITE)
        surface.blit(text, (log_rect.x + 10, log_rect.y + 10 + i * 25))
    
    # Draw battle HUD
    title_text = font_large.render("BATTLE", True, WHITE)
    title_rect = title_text.get_rect(midtop=(WIDTH/2, 20))
    surface.blit(title_text, title_rect)
    
    # Player stats
    player_level = font_small.render(f"Lvl: {player.level}", True, WHITE)
    surface.blit(player_level, (20, 20))
    
    # Player health/stamina bars are drawn in player.draw()
    
    # Enemy level
    enemy_level = font_small.render(f"Lvl: {enemy.level}", True, WHITE)
    level_rect = enemy_level.get_rect(topright=(WIDTH-20, 20))
    surface.blit(enemy_level, level_rect)
    
    # Enemy health/stamina bars are drawn in enemy.draw()

def draw_main_menu(surface, buttons):
    """Draw the main menu screen"""
    # Background
    surface.fill((30, 30, 50))  # Dark background
    
    # Title
    title_text = font_title.render("BATTLE ARENA", True, GOLD)
    title_rect = title_text.get_rect(center=(WIDTH/2, 100))
    surface.blit(title_text, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_character_creation(surface, buttons, input_name, selected_class):
    """Draw the character creation screen"""
    # Background
    surface.fill((30, 30, 50))
    
    # Title
    title_text = font_title.render("CHARACTER CREATION", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 60))
    surface.blit(title_text, title_rect)
    
    # Name input box
    pygame.draw.rect(surface, WHITE, (WIDTH/2 - 150, 140, 300, 40), 2)
    name_label = font_medium.render("Character Name:", True, WHITE)
    surface.blit(name_label, (WIDTH/2 - 150, 110))
    
    # Display entered name
    name_text = font_medium.render(input_name, True, WHITE)
    surface.blit(name_text, (WIDTH/2 - 140, 150))
    
    # Class selection
    class_label = font_medium.render("Select Class:", True, WHITE)
    surface.blit(class_label, (WIDTH/2 - 150, 200))
    
    # Class info
    if selected_class:
        class_info = {
            WARRIOR: "High Strength and Health. Born for battle.",
            ROGUE: "High Speed. Masters of evasion and quick strikes.",
            KNIGHT: "High Armor. Well-protected defenders."
        }
        
        class_text = font_large.render(selected_class, True, GOLD)
        surface.blit(class_text, (WIDTH/2 - 100, 240))
        
        # Class description
        desc = class_info.get(selected_class, "")
        desc_text = font_small.render(desc, True, WHITE)
        surface.blit(desc_text, (WIDTH/2 - 150, 290))
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_arena_menu(surface, player, buttons, battles_won):
    """Draw the arena menu screen"""
    # Background
    surface.fill((50, 30, 30))  # Dark red background for arena menu
    
    # Title
    title_text = font_title.render("ARENA MENU", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 60))
    surface.blit(title_text, title_rect)
    
    # Player basic info
    info_text = font_medium.render(f"{player.name} (Level {player.level}) - Gold: {player.gold}", True, GOLD)
    info_rect = info_text.get_rect(center=(WIDTH/2, 120))
    surface.blit(info_text, info_rect)
    
    # Battles won
    battles_text = font_medium.render(f"Battles Won: {battles_won}", True, WHITE)
    battles_rect = battles_text.get_rect(center=(WIDTH/2, 160))
    surface.blit(battles_text, battles_rect)
    
    # Health and Stamina bars
    bar_width = 300
    bar_height = 20
    
    # Health
    health_label = font_small.render(f"Health: {player.health}/{player.max_health}", True, WHITE)
    surface.blit(health_label, (WIDTH/2 - bar_width/2, 190))
    draw_health_bar(surface, WIDTH/2 - bar_width/2, 210, bar_width, bar_height, 
                   player.health, player.max_health)
    
    # Stamina
    stamina_label = font_small.render(f"Stamina: {player.stamina}/{player.max_stamina}", True, WHITE)
    surface.blit(stamina_label, (WIDTH/2 - bar_width/2, 240))
    draw_health_bar(surface, WIDTH/2 - bar_width/2, 260, bar_width, bar_height, 
                   player.stamina, player.max_stamina, fill_color=BLUE)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def draw_character_stats(surface, player, button):
    """Draw the character stats screen"""
    # Background
    surface.fill((30, 50, 30))  # Dark green background for stats
    
    # Title
    title_text = font_title.render("CHARACTER STATS", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH/2, 50))
    surface.blit(title_text, title_rect)
    
    # Character basic info
    info_text = font_large.render(f"{player.name} - {player.character_class}", True, GOLD)
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
        stat_text = font_medium.render(stat, True, WHITE)
        surface.blit(stat_text, (WIDTH/2 - 150, 150 + i * 30))
    
    # Skills
    skill_title = font_large.render("Skills:", True, GOLD)
    surface.blit(skill_title, (WIDTH/2 - 150, 450))
    
    y_offset = 490
    for skill_name, skill_info in player.skills.items():
        skill_text = font_medium.render(
            f"{skill_name}: Damage x{skill_info['damage']}, "
            f"Accuracy {int(skill_info['accuracy']*100)}%, "
            f"Cost {skill_info['stamina_cost']} stamina", 
            True, WHITE
        )
        surface.blit(skill_text, (WIDTH/2 - 150, y_offset))
        y_offset += 30
    
    # Draw back button
    button.draw(surface)

def draw_game_over(surface, player, battles_won, buttons):
    """Draw game over screen"""
    # Background
    surface.fill((10, 10, 10))  # Very dark background
    
    # Title
    title_text = font_title.render("GAME OVER", True, RED)
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
        stat = font_medium.render(text, True, WHITE)
        stat_rect = stat.get_rect(center=(WIDTH/2, 200 + i * 40))
        surface.blit(stat, stat_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(surface)

def main():
    clock = pygame.time.Clock()
    game_state = STATE_MAIN_MENU
    
    # Game variables
    player = None
    enemy = None
    battles_won = 0
    battle_turn = "player"  # Who's turn it is in battle
    battle_log = []  # Messages during battle
    battle_action_delay = 0  # Delay between actions for animation
    
    # Character creation variables
    input_name = "Hero"  # Default name
    selected_class = None
    
    # Main menu buttons
    main_menu_buttons = [
        Button(WIDTH/2 - 100, 250, 200, 50, "New Game"),
        Button(WIDTH/2 - 100, 320, 200, 50, "Exit")
    ]
    
    # Character creation buttons
    char_creation_buttons = [
        Button(WIDTH/2 - 300, 240, 180, 40, WARRIOR),
        Button(WIDTH/2 - 90, 240, 180, 40, ROGUE),
        Button(WIDTH/2 + 120, 240, 180, 40, KNIGHT),
        Button(WIDTH/2 - 100, 350, 200, 50, "Create Character")
    ]
    
    # Arena menu buttons
    arena_buttons = [
        Button(WIDTH/2 - 100, 320, 200, 50, "Enter Battle"),
        Button(WIDTH/2 - 100, 380, 200, 50, "View Stats"),
        Button(WIDTH/2 - 100, 440, 200, 50, "Rest (Heal)"),
        Button(WIDTH/2 - 100, 500, 200, 50, "Exit Game")
    ]
    
    # Battle buttons
    battle_buttons = [
        Button(50, 450, 200, 40, "Quick Strike"),
        Button(270, 450, 200, 40, "Heavy Strike"),
        Button(490, 450, 200, 40, "Rest")
    ]
    
    # Stats screen back button
    stats_back_button = Button(WIDTH/2 - 100, 550, 200, 40, "Back")
    
    # Game over buttons
    game_over_buttons = [
        Button(WIDTH/2 - 100, 400, 200, 50, "New Game"),
        Button(WIDTH/2 - 100, 470, 200, 50, "Exit")
    ]
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True
                    
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_CHARACTER_CREATION:
                    if event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if selected_class and input_name:
                            player = Character(input_name, selected_class)
                            game_state = STATE_ARENA_MENU
                    else:
                        # Limit name length and only add printable characters
                        if len(input_name) < 15 and event.unicode.isprintable():
                            input_name += event.unicode
        
        # Main menu state
        if game_state == STATE_MAIN_MENU:
            for button in main_menu_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "New Game":
                        game_state = STATE_CHARACTER_CREATION
                        input_name = "Hero"  # Reset default name
                        selected_class = None
                    elif button.text == "Exit":
                        running = False
            
            # Draw main menu
            draw_main_menu(screen, main_menu_buttons)
                
        # Character creation state
        elif game_state == STATE_CHARACTER_CREATION:
            for i, button in enumerate(char_creation_buttons):
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if i < 3:  # Class selection buttons
                        selected_class = button.text
                    elif button.text == "Create Character" and selected_class and input_name:
                        player = Character(input_name, selected_class)
                        game_state = STATE_ARENA_MENU
                        battles_won = 0
            
            # Draw character creation
            draw_character_creation(screen, char_creation_buttons, input_name, selected_class)
                
        # Arena menu state
        elif game_state == STATE_ARENA_MENU:
            for i, button in enumerate(arena_buttons):
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Enter Battle":
                        enemy = generate_enemy(player.level)
                        battle_log = [f"A {enemy.name} (Level {enemy.level}) appears!"]
                        battle_turn = "player"
                        battle_action_delay = 0
                        game_state = STATE_BATTLE
                    elif button.text == "View Stats":
                        game_state = STATE_CHARACTER_STATS
                    elif button.text == "Rest (Heal)":
                        health_restored = min(player.max_health - player.health, player.max_health // 2)
                        stamina_restored = min(player.max_stamina - player.stamina, player.max_stamina)
                        
                        player.health += health_restored
                        player.stamina = player.max_stamina
                        
                        battle_log = [f"{player.name} takes a rest and recovers {health_restored} health and full stamina!"]
                    elif button.text == "Exit Game":
                        game_state = STATE_GAME_OVER
            
            # Draw arena menu
            draw_arena_menu(screen, player, arena_buttons, battles_won)
                
        # Battle state
        elif game_state == STATE_BATTLE:
            # Update character animations
            player.update_animation()
            enemy.update_animation()
            
            # Handle battle turns
            if battle_turn == "player":
                for i, button in enumerate(battle_buttons):
                    button.check_hover(mouse_pos)
                    if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                        result = None
                        
                        if button.text == "Quick Strike":
                            result = player.attack(enemy, "Quick Strike")
                        elif button.text == "Heavy Strike":
                            result = player.attack(enemy, "Heavy Strike")
                        elif button.text == "Rest":
                            result = player.rest()
                        
                        if result:
                            battle_log.append(result["message"])
                            
                            # Check if enemy is defeated
                            if enemy.health <= 0:
                                battle_log.append(f"{enemy.name} has been defeated!")
                                player.gain_experience(enemy.exp_reward)
                                player.gold += enemy.gold_reward
                                battle_log.append(f"You gained {enemy.exp_reward} experience and {enemy.gold_reward} gold!")
                                battles_won += 1
                                battle_action_delay = 60  # Set delay before returning to arena menu
                                game_state = STATE_ARENA_MENU
                            else:
                                battle_turn = "enemy"
                                battle_action_delay = 30  # Delay before enemy's turn
            
            # Enemy turn
            if battle_turn == "enemy" and battle_action_delay <= 0:
                result = enemy.choose_action(player)
                battle_log.append(result["message"])
                
                # Check if player is defeated
                if player.health <= 0:
                    battle_log.append(f"{player.name} has been defeated!")
                    battle_action_delay = 60
                    game_state = STATE_GAME_OVER
                else:
                    battle_turn = "player"
            
            # Update action delay
            if battle_action_delay > 0:
                battle_action_delay -= 1
            
            # Draw battle screen
            draw_battle_arena(screen, player, enemy, battle_log)
            
            # Only draw buttons during player's turn
            if battle_turn == "player":
                for button in battle_buttons:
                    button.draw(screen)
                
        # Character stats state
        elif game_state == STATE_CHARACTER_STATS:
            stats_back_button.check_hover(mouse_pos)
            if mouse_clicked and stats_back_button.is_clicked(mouse_pos, mouse_clicked):
                game_state = STATE_ARENA_MENU
                
            # Draw character stats
            draw_character_stats(screen, player, stats_back_button)
                
        # Game over state
        elif game_state == STATE_GAME_OVER:
            for button in game_over_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "New Game":
                        game_state = STATE_CHARACTER_CREATION
                        input_name = "Hero"
                        selected_class = None
                    elif button.text == "Exit":
                        running = False
                        
            # Draw game over screen
            draw_game_over(screen, player, battles_won, game_over_buttons)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()