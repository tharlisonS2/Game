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
            "Fierce Attack": {"damage": 1.3, "accuracy": 0.6, "stamina_cost": 15},
            "Leap Attack": {"damage": 1.8, "accuracy": 0.65, "stamina_cost": 30}
        }
        self.max_health = 80 + (self.vitality * 10)
        self.health = self.max_health
        self.max_stamina = 80 + (self.agility * 2) + (self.stamina_stat * 5)
        self.stamina = self.max_stamina
        self.base_position = (600, 400)  # Position[1] now represents the bottom of the body
        self.position = list(self.base_position)
        self.move_speed = 5 + self.agility * 2
        self.move_stamina_cost = 5
        self.color = (200, 50, 50)

    def choose_action(self, player):
        distance = abs(self.position[0] - player.position[0])
        
        if self.stamina < self.skills["Strike"]["stamina_cost"]:
            return self.rest()
        
        if distance > 100:
            if (self.stamina >= self.skills["Leap Attack"]["stamina_cost"] and 
                random.random() < 0.7):
                return self.attack(player, "Leap Attack")
            elif (self.stamina >= self.jump_stamina_cost and 
                  random.random() < 0.3 and not self.is_jumping):
                # Jump toward player
                direction = "forward" if self.position[0] > player.position[0] else "backward"
                return self.jump(direction)
            elif self.position[0] > player.position[0]:
                return self.move_left(player)
            else:
                return self.move_right(player)
        
        if self.health < self.max_health * 0.3:
            if (self.stamina >= self.jump_stamina_cost and 
                random.random() < 0.4 and not self.is_jumping):
                # Jump away from player
                direction = "backward" if self.position[0] > player.position[0] else "forward"
                return self.jump(direction)
            elif self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                return self.attack(player, "Fierce Attack")
            return self.attack(player, "Strike")
        else:
            roll = random.random()
            if roll < 0.3 and self.stamina >= self.jump_stamina_cost and not self.is_jumping:
                # Random jump direction
                direction = "forward" if random.random() < 0.5 else "backward"
                return self.jump(direction)
            elif roll < 0.6:
                return self.attack(player, "Strike")
            elif roll < 0.9 and self.stamina >= self.skills["Fierce Attack"]["stamina_cost"]:
                return self.attack(player, "Fierce Attack")
            return self.attack(player, "Strike")