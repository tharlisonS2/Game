import random
from entities.character import Character
from constants import WIDTH

class Enemy(Character):
    def __init__(self, name, level):
        enemy_stats = {'strength': 0, 'agility': 0, 'armor': 0, 'stamina': 0, 'vitality': 0}
        super().__init__(name, enemy_stats)
        self.level = level
        self.max_health = 50 + (level * 10)
        self.health = self.max_health
        self.strength = 5 + (level * 2)
        self.agility = 5 + level
        self.armor = 2 + level
        self.stamina_stat = 5 + level
        self.vitality = 5 + level
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
        self.max_health = 80 + (self.vitality * 10)
        self.health = self.max_health
        self.max_stamina = 80 + (self.agility * 2) + (self.stamina_stat * 5)
        self.stamina = self.max_stamina
        self.base_position = (600, 300)
        self.position = list(self.base_position)
        self.move_speed = 5 + self.agility * 2  # Increased agility impact on movement
        self.move_stamina_cost = 5  # Base stamina cost for movement
        self.color = (200, 50, 50)

    def choose_action(self, player):
        distance = abs(self.position[0] - player.position[0])
        
        if self.stamina < 15:
            return self.rest()
        
        if distance > 100:
            if self.position[0] > player.position[0]:
                return self.move_left(player)
            else:
                return self.move_right(player)
        # Within range, only attack or rest, no movement
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