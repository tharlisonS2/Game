# battle_arena/entities/character.py
import pygame
import random
from constants import RED, GREEN, BLUE, WHITE, BROWN, WIDTH

class Character:
    def __init__(self, name, stats=None):
        self.name = name
        self.level = 1
        self.strength = 5
        self.speed = 5
        self.armor = 5
        
        if stats:
            self.strength += stats.get('strength', 0)
            self.speed += stats.get('agility', 0)
            self.armor += stats.get('defense', 0)
        
        self.max_health = 80 + (self.strength * 2)
        self.health = self.max_health
        self.max_stamina = 80 + (self.speed * 2)
        self.stamina = self.max_stamina
        
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
        
        self.is_attacking = False
        self.attack_frame = 0
        self.is_hit = False
        self.hit_frame = 0
        self.base_position = (200, 300)
        self.position = list(self.base_position)
        self.move_speed = 5
        self.color = (50, 100, 200)
        self.font_small = pygame.font.SysFont('Arial', 18)

    def attack(self, enemy, skill_name):
        distance = abs(self.position[0] - enemy.position[0])
        if distance > 100:  # Increased from 50 to 100 (already done)
            return {"success": False, "message": f"{self.name} is too far to attack {enemy.name}!"}
        
        skill = self.skills[skill_name]
        if self.stamina < skill["stamina_cost"]:
            return {"success": False, "message": f"{self.name} is too tired to use {skill_name}!"}
        
        self.stamina -= skill["stamina_cost"]
        self.is_attacking = True
        self.attack_frame = 0
        
        hit_chance = skill["accuracy"] * (self.speed / (self.speed + enemy.speed))
        if random.random() <= hit_chance:
            weapon_damage = self.weapons[self.equipped_weapon]
            base_damage = self.strength + weapon_damage
            skill_modifier = skill["damage"]
            damage = int(base_damage * skill_modifier)
            armor_value = enemy.armor_items[enemy.equipped_armor]
            damage_reduced = max(1, damage - armor_value - (enemy.armor // 2))
            enemy.health = max(0, enemy.health - damage_reduced)
            enemy.is_hit = True
            enemy.hit_frame = 0
            return {
                "success": True, 
                "hit": True, 
                "damage": damage_reduced,
                "message": f"{self.name} hits {enemy.name} with {skill_name} for {damage_reduced} damage!"
            }
        return {
            "success": True, 
            "hit": False, 
            "damage": 0,
            "message": f"{self.name}'s {skill_name} missed {enemy.name}!"
        }

    def rest(self):
        recovery = max(5, self.max_stamina // 10)
        self.stamina = min(self.max_stamina, self.stamina + recovery)
        return {"success": True, "message": f"{self.name} rests and recovers {recovery} stamina!"}

    def gain_experience(self, amount):
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
        self.strength += 2
        self.speed += 1
        self.armor += 1
        self.max_health = 80 + (self.strength * 2)
        self.health = self.max_health
        self.max_stamina = 80 + (self.speed * 2)
        self.stamina = self.max_stamina
        return f"{self.name} has reached level {self.level}! Attributes increased!"

    def move_left(self):
        if self.position[0] > 50:
            self.position[0] -= self.move_speed

    def move_right(self):
        if self.position[0] < WIDTH - 50:
            self.position[0] += self.move_speed

    def update_animation(self):
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame > 10:
                self.is_attacking = False
                self.attack_frame = 0
        if self.is_hit:
            self.hit_frame += 1
            if self.hit_frame > 10:
                self.is_hit = False
                self.hit_frame = 0

    def draw(self, surface):
        color = self.color if not self.is_hit else (RED if self.hit_frame % 2 == 0 else self.color)
        position = list(self.position)
        if self.is_attacking:
            if self.attack_frame < 5:
                position[0] += self.attack_frame * 5
            else:
                position[0] -= (self.attack_frame - 5) * 5
        
        pygame.draw.circle(surface, color, (int(position[0]), int(position[1])), 30)
        pygame.draw.rect(surface, color, (int(position[0]) - 20, int(position[1]) + 30, 40, 60))
        if self.is_attacking:
            pygame.draw.rect(surface, BROWN, (int(position[0]) + 20, int(position[1]) - 10, 40, 10))
        
        health_width = 60
        health_percent = self.health / self.max_health
        pygame.draw.rect(surface, RED, (int(position[0]) - 30, int(position[1]) - 50, health_width, 10))
        pygame.draw.rect(surface, GREEN, (int(position[0]) - 30, int(position[1]) - 50, int(health_width * health_percent), 10))
        
        stamina_width = 60
        stamina_percent = self.stamina / self.max_stamina
        pygame.draw.rect(surface, (150, 150, 150), (int(position[0]) - 30, int(position[1]) - 38, stamina_width, 6))
        pygame.draw.rect(surface, BLUE, (int(position[0]) - 30, int(position[1]) - 38, int(stamina_width * stamina_percent), 6))
        
        name_text = self.font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(int(position[0]), int(position[1]) - 60))
        surface.blit(name_text, name_rect)