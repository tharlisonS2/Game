import random
from .enemy import Enemy

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