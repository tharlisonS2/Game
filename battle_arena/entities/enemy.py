# battle_arena/entities/enemy.py
import random
from entities.character import Character
from constants import WIDTH

class Enemy(Character):
    def __init__(self, name, level):
        enemy_stats = {'strength': 0, 'speed': 0, 'armor': 0}
        super().__init__(name, enemy_stats)
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
        self.base_position = (600, 300)
        self.position = list(self.base_position)
        self.move_speed = 5
        self.color = (200, 50, 50)

    def choose_action(self, player):
        distance = abs(self.position[0] - player.position[0])
        
        if self.stamina < 15:
            return self.rest()
        
        # Move toward player if too far to attack (updated to 100 to match attack range)
        if distance > 100:  # Changed from 50 to 100
            if self.position[0] > player.position[0]:
                self.move_left()
                return {"success": True, "message": f"{self.name} moves closer to {player.name}!"}
            else:
                self.move_right()
                return {"success": True, "message": f"{self.name} moves closer to {player.name}!"}
        
        # Attack if close enough
        if self.health < self.max_health * 0.3:
            if self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                return self.attack(player, "Fierce Attack")
            return self.attack(player, "Strike")
        else:
            if random.random() < 0.7:
                return self.attack(player, "Strike")
            elif self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                return self.attack(player, "Fierce Attack")
            return self.attack(player, "Strike")