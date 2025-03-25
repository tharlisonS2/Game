import pygame
import random
from constants import RED, GREEN, BLUE, WHITE, BROWN, WIDTH

class Character:
    def __init__(self, name, stats=None):
        self.name = name
        self.level = 1
        self.strength = 5
        self.agility = 5
        self.armor = 5
        self.stamina_stat = 5
        self.vitality = 5
        
        if stats:
            self.strength += stats.get('strength', 0)
            self.agility += stats.get('agility', 0)
            self.armor += stats.get('defense', 0)
            self.stamina_stat += stats.get('stamina', 0)
            self.vitality += stats.get('vitality', 0)
        
        self.max_health = 80 + (self.vitality * 10)
        self.health = self.max_health
        self.max_stamina = 80 + (self.agility * 2) + (self.stamina_stat * 5)
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
            "Heavy Strike": {"damage": 1.5, "accuracy": 0.7, "stamina_cost": 20},
            "Leap Attack": {"damage": 1.8, "accuracy": 0.65, "stamina_cost": 30}
        }
        
        self.is_attacking = False
        self.attack_frame = 0
        self.is_hit = False
        self.hit_frame = 0
        self.base_position = (200, 400)  # Position[1] is bottom of body
        self.position = list(self.base_position)
        self.move_speed = 5 + self.agility * 2
        self.move_stamina_cost = 5
        self.color = (50, 100, 200)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
        self.is_jumping = False
        self.jump_frame = 0
        self.base_jump_height = 60  # Base jump height before agility scaling
        self.base_jump_distance = 40  # Base jump distance before agility scaling
        self.jump_height = self.base_jump_height + (self.agility * 2)  # Scales with agility (2 pixels per agility point)
        self.jump_distance = self.base_jump_distance + (self.agility * 2)  # Scales with agility (2 pixels per agility point)
        self.jump_stamina_cost = 15
        self.jump_direction = None  # "forward" or "backward"

    def attack(self, enemy, skill_name):
        distance = abs(self.position[0] - enemy.position[0])
        skill = self.skills[skill_name]
        
        if skill_name == "Leap Attack":
            if distance <= 100:
                return {"success": False, "message": f"{self.name} is already too close for Leap Attack!"}
            if self.stamina < skill["stamina_cost"]:
                return {"success": False, "message": f"{self.name} is too tired to use {skill_name}!"}
            
            self.stamina -= skill["stamina_cost"]
            leap_distance = self.move_speed * 2.5
            if self.position[0] < enemy.position[0]:
                new_position = min(self.position[0] + leap_distance, enemy.position[0] - 100)
                self.position[0] = min(new_position, WIDTH - 50)
            else:
                new_position = max(self.position[0] - leap_distance, enemy.position[0] + 100)
                self.position[0] = max(50, new_position)
            
            new_distance = abs(self.position[0] - enemy.position[0])
            if new_distance > 100:
                return {
                    "success": True,
                    "hit": False,
                    "damage": 0,
                    "message": f"{self.name} leaps toward {enemy.name} but is still too far to hit!"
                }
        else:
            if distance > 100:
                return {"success": False, "message": f"{self.name} is too far to attack {enemy.name}!"}
            if self.stamina < skill["stamina_cost"]:
                return {"success": False, "message": f"{self.name} is too tired to use {skill_name}!"}
            self.stamina -= skill["stamina_cost"]
        
        self.is_attacking = True
        self.attack_frame = 0
        
        hit_chance = skill["accuracy"] * (self.agility / (self.agility + enemy.agility))
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
            message = (f"{self.name} leaps and hits {enemy.name} for {damage_reduced} damage!" 
                      if skill_name == "Leap Attack" 
                      else f"{self.name} hits {enemy.name} with {skill_name} for {damage_reduced} damage!")
            return {
                "success": True, 
                "hit": True, 
                "damage": damage_reduced,
                "message": message
            }
        message = (f"{self.name}'s Leap Attack missed {enemy.name}!" 
                  if skill_name == "Leap Attack" 
                  else f"{self.name}'s {skill_name} missed {enemy.name}!")
        return {
            "success": True, 
            "hit": False, 
            "damage": 0,
            "message": message
        }

    def rest(self):
        recovery = max(5, self.max_stamina // 10) + self.stamina_stat
        self.stamina = min(self.max_stamina, self.stamina + recovery)
        return {"success": True, "message": f"{self.name} rests and recovers {recovery} stamina!"}

    def jump(self, direction):
        if self.stamina < self.jump_stamina_cost:
            return {"success": False, "message": f"{self.name} is too tired to jump!"}
        if self.is_jumping:
            return {"success": False, "message": f"{self.name} is already jumping!"}
        
        self.stamina -= self.jump_stamina_cost
        self.is_jumping = True
        self.jump_frame = 0
        self.jump_direction = direction
        direction_text = "forward" if direction == "forward" else "backward"
        return {"success": True, "message": f"{self.name} jumps {direction_text}!"}

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
        self.agility += 1
        self.armor += 1
        self.stamina_stat += 1
        self.vitality += 1
        self.max_health = 80 + (self.vitality * 10)
        self.health = self.max_health
        self.max_stamina = 80 + (self.agility * 2) + (self.stamina_stat * 5)
        self.stamina = self.max_stamina
        self.move_speed = 5 + self.agility * 2
        # Update jump stats when agility changes
        self.jump_height = self.base_jump_height + (self.agility * 2)
        self.jump_distance = self.base_jump_distance + (self.agility * 2)
        return f"{self.name} has reached level {self.level}! Attributes increased!"

    def move_left(self, enemy=None):
        if self.stamina < self.move_stamina_cost:
            return {"success": False, "message": f"{self.name} is too tired to move!"}
        if self.position[0] <= 50:
            return {"success": False, "message": f"{self.name} cannot move further left!"}
        
        self.stamina -= self.move_stamina_cost
        new_position = self.position[0] - self.move_speed
        
        if enemy and self.position[0] > enemy.position[0]:
            min_position = enemy.position[0] + 100
            if new_position < min_position:
                new_position = min_position
                self.position[0] = new_position
                return {"success": True, "message": f"{self.name} moves left and stops near {enemy.name}!"}
        
        self.position[0] = max(50, new_position)
        return {"success": True, "message": f"{self.name} moves left!"}

    def move_right(self, enemy=None):
        if self.stamina < self.move_stamina_cost:
            return {"success": False, "message": f"{self.name} is too tired to move!"}
        if self.position[0] >= WIDTH - 50:
            return {"success": False, "message": f"{self.name} cannot move further right!"}
        
        self.stamina -= self.move_stamina_cost
        new_position = self.position[0] + self.move_speed
        
        if enemy and self.position[0] < enemy.position[0]:
            max_position = enemy.position[0] - 100
            if new_position > max_position:
                new_position = max_position
                self.position[0] = new_position
                return {"success": True, "message": f"{self.name} moves right and stops near {enemy.name}!"}
        
        self.position[0] = min(WIDTH - 50, new_position)
        return {"success": True, "message": f"{self.name} moves right!"}

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
        if self.is_jumping:
            self.jump_frame += 1
            total_frames = 20
            if self.jump_frame <= 10:  # Ascending
                self.position[1] = self.base_position[1] - (self.jump_height * (self.jump_frame / 10))
                if self.jump_direction == "forward":
                    self.position[0] += self.jump_distance / total_frames
                elif self.jump_direction == "backward":
                    self.position[0] -= self.jump_distance / total_frames
            else:  # Descending
                self.position[1] = self.base_position[1] - (self.jump_height * (1 - (self.jump_frame - 10) / 10))
                if self.jump_direction == "forward":
                    self.position[0] += self.jump_distance / total_frames
                elif self.jump_direction == "backward":
                    self.position[0] -= self.jump_distance / total_frames
            
            # Ensure position stays within bounds
            self.position[0] = max(50, min(WIDTH - 50, self.position[0]))
            
            if self.jump_frame >= total_frames:
                self.is_jumping = False
                self.jump_frame = 0
                self.jump_direction = None
                self.position[1] = self.base_position[1]

    def draw(self, surface):
        color = self.color if not self.is_hit else (RED if self.hit_frame % 2 == 0 else self.color)
        position = list(self.position)
        
        if self.is_attacking:
            if self.attack_frame < 5:
                position[0] += self.attack_frame * 5
            else:
                position[0] -= (self.attack_frame - 5) * 5
        
        # Define character dimensions
        body_height = 60
        head_radius = 30
        
        # Body bottom is at position[1], head is above it
        body_bottom = position[1]
        body_top = body_bottom - body_height
        head_center_y = body_top - head_radius
        
        # Draw body
        pygame.draw.rect(surface, color, (int(position[0]) - 20, body_top, 40, body_height))
        # Draw head
        pygame.draw.circle(surface, color, (int(position[0]), int(head_center_y)), head_radius)
        
        # Draw weapon during attack
        if self.is_attacking:
            pygame.draw.rect(surface, BROWN, (int(position[0]) + 20, body_top - 10, 40, 10))
        
        # Draw health and stamina bars above the head
        health_width = 60
        health_percent = self.health / self.max_health
        pygame.draw.rect(surface, RED, (int(position[0]) - 30, head_center_y - 20, health_width, 10))
        pygame.draw.rect(surface, GREEN, (int(position[0]) - 30, head_center_y - 20, int(health_width * health_percent), 10))
        
        stamina_width = 60
        stamina_percent = self.stamina / self.max_stamina
        pygame.draw.rect(surface, (150, 150, 150), (int(position[0]) - 30, head_center_y - 8, stamina_width, 6))
        pygame.draw.rect(surface, BLUE, (int(position[0]) - 30, head_center_y - 8, int(stamina_width * stamina_percent), 6))
        
        # Draw name above everything
        name_text = self.font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(int(position[0]), head_center_y - 30))
        surface.blit(name_text, name_rect)