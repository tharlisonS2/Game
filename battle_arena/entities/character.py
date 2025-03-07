# entities/character.py
import pygame
import random
from constants import RED, GREEN, BLUE, WHITE, BROWN

class Character:
    def __init__(self, name, stats=None):
        self.name = name
        self.level = 1
        
        # Base stats
        self.strength = 10
        self.speed = 10
        self.armor = 5
        
        # Apply custom stats if provided
        if stats:
            self.strength += stats.get('strength', 0)
            self.speed += stats.get('speed', 0)
            self.armor += stats.get('armor', 0)
        
        # Calculated stats
        self.max_health = 80 + (self.strength * 2)
        self.health = self.max_health
        self.max_stamina = 80 + (self.speed * 2)
        self.stamina = self.max_stamina
        
        # Other character attributes
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
        
        # Animation state
        self.is_attacking = False
        self.attack_frame = 0
        self.is_hit = False
        self.hit_frame = 0
        self.position = (200, 300)  # Default position on screen
        self.color = (50, 100, 200)  # Player color
        self.font_small = pygame.font.SysFont('Arial', 18)
            
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
        self.strength += 2
        self.speed += 1
        self.armor += 1
        
        # Update calculated stats
        self.max_health = 80 + (self.strength * 2)
        self.health = self.max_health
        self.max_stamina = 80 + (self.speed * 2)
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
        pygame.draw.rect(surface, (150, 150, 150), (position[0]-30, position[1]-38, stamina_width, 6))
        pygame.draw.rect(surface, BLUE, (position[0]-30, position[1]-38, int(stamina_width * stamina_percent), 6))
        
        # Draw name
        name_text = self.font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(position[0], position[1]-60))
        surface.blit(name_text, name_rect)