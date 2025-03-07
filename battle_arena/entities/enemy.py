# entities/enemy.py
import random
from entities.character import Character

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