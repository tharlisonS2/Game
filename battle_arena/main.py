import pygame
import sys
from constants import *
from game_state import GameState
from entities import Character, Enemy, generate_enemy
from ui import (
    Button, 
    draw_health_bar,
    draw_main_menu,
    draw_character_creation,
    draw_arena_menu,
    draw_battle_arena,
    draw_character_stats,
    draw_game_over,
    draw_pre_battle
)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Arena")
    clock = pygame.time.Clock()
    
    fonts = {
        'small': pygame.font.SysFont('Arial', 18),
        'medium': pygame.font.SysFont('Arial', 24),
        'large': pygame.font.SysFont('Arial', 32),
        'title': pygame.font.SysFont('Arial', 48, bold=True)
    }
    
    game_state = GameState()
    
    main_menu_buttons = [
        Button(WIDTH/2 - 100, 250, 200, 50, "New Game"),
        Button(WIDTH/2 - 100, 320, 200, 50, "Exit")
    ]
    
    char_creation_buttons = []
    y_position = 240
    for stat in game_state.current_stats.keys():
        char_creation_buttons.append(Button(WIDTH/2 - 180, y_position, 30, 30, "-", color=RED))
        char_creation_buttons.append(Button(WIDTH/2 - 30, y_position, 30, 30, "+", color=GREEN))
        y_position += 40
    char_creation_buttons.append(Button(WIDTH/2 - 100, 440, 200, 50, "Create Character"))
    
    arena_buttons = [
        Button(WIDTH/2 - 100, 320, 200, 50, "Enter Battle"),
        Button(WIDTH/2 - 100, 380, 200, 50, "View Stats"),
        Button(WIDTH/2 - 100, 440, 200, 50, "Rest (Heal)"),
        Button(WIDTH/2 - 100, 500, 200, 50, "Exit Game")
    ]
    
    pre_battle_button = Button(WIDTH/2 - 100, HEIGHT - 80, 200, 40, "Start Battle!")
    
    battle_buttons = [
        # Movement buttons (top row)
        Button(50, 420, 120, 40, "Move Left", color=(0, 120, 200), hover_color=(255, 215, 0), font_size=18),
        Button(180, 420, 120, 40, "Move Right", color=(0, 120, 200), hover_color=(255, 215, 0), font_size=18),
        # Attack buttons (middle row)
        Button(50, 470, 120, 40, "Quick Strike", color=(200, 50, 50), hover_color=(255, 215, 0), font_size=18),
        Button(180, 470, 120, 40, "Heavy Strike", color=(200, 50, 50), hover_color=(255, 215, 0), font_size=18),
        Button(310, 470, 120, 40, "Leap Attack", color=(200, 50, 50), hover_color=(255, 215, 0), font_size=18),
        # Utility buttons (bottom row)
        Button(50, 520, 120, 40, "Rest", color=(50, 150, 50), hover_color=(255, 215, 0), font_size=18),
        Button(180, 520, 120, 40, "Jump Fwd", color=(0, 120, 200), hover_color=(255, 215, 0), font_size=18),
        Button(310, 520, 120, 40, "Jump Bwd", color=(0, 120, 200), hover_color=(255, 215, 0), font_size=18),
    ]
    
    stats_back_button = Button(WIDTH/2 - 100, 550, 200, 40, "Back")
    
    game_over_buttons = [
        Button(WIDTH/2 - 100, 330, 200, 50, "Return to Main Menu"),
        Button(WIDTH/2 - 100, 400, 200, 50, "New Game"),
        Button(WIDTH/2 - 100, 470, 200, 50, "Exit")
    ]
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            if event.type == pygame.KEYDOWN:
                if game_state.current_state == GameState.STATE_CHARACTER_CREATION:
                    if event.key == pygame.K_BACKSPACE:
                        game_state.input_name = game_state.input_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if game_state.get_remaining_points() == 0 and game_state.input_name:
                            game_state.player = Character(game_state.input_name, game_state.current_stats)
                            game_state.change_state(GameState.STATE_ARENA_MENU)
                    elif len(game_state.input_name) < 15 and event.unicode.isprintable():
                        game_state.input_name += event.unicode
        
        if game_state.current_state == GameState.STATE_MAIN_MENU:
            for button in main_menu_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "New Game":
                        game_state.change_state(GameState.STATE_CHARACTER_CREATION)
                        game_state.input_name = "Hero"
                        game_state.current_stats = {'strength': 0, 'agility': 0, 'defense': 0, 'stamina': 0, 'vitality': 0}
                    elif button.text == "Exit":
                        running = False
            draw_main_menu(screen, main_menu_buttons, fonts)
                
        elif game_state.current_state == GameState.STATE_CHARACTER_CREATION:
            for i, button in enumerate(char_creation_buttons):
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if i < len(char_creation_buttons) - 1:
                        stat_index = i // 2
                        stat_key = list(game_state.current_stats.keys())[stat_index]
                        if i % 2 == 0 and game_state.current_stats[stat_key] > 0:
                            game_state.current_stats[stat_key] -= 1
                        elif i % 2 == 1 and game_state.get_remaining_points() > 0:
                            game_state.current_stats[stat_key] += 1
                    elif button.text == "Create Character" and game_state.get_remaining_points() == 0 and game_state.input_name:
                        game_state.player = Character(game_state.input_name, game_state.current_stats)
                        game_state.change_state(GameState.STATE_ARENA_MENU)
                        game_state.battles_won = 0
            draw_character_creation(screen, char_creation_buttons, game_state, fonts)
                
        elif game_state.current_state == GameState.STATE_ARENA_MENU:
            for button in arena_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Enter Battle":
                        game_state.enemy = generate_enemy(game_state.player.level)
                        game_state.battle_log = [f"A {game_state.enemy.name} (Level {game_state.enemy.level}) appears!"]
                        game_state.battle_turn = "player"
                        game_state.battle_action_delay = 0
                        game_state.pre_battle_timer = 0
                        game_state.change_state(GameState.STATE_PRE_BATTLE)
                    elif button.text == "View Stats":
                        game_state.change_state(GameState.STATE_CHARACTER_STATS)
                    elif button.text == "Rest (Heal)":
                        health_restored = min(game_state.player.max_health - game_state.player.health, game_state.player.max_health // 2)
                        game_state.player.health += health_restored
                        game_state.player.stamina = game_state.player.max_stamina
                        game_state.battle_log = [f"{game_state.player.name} recovers {health_restored} health and full stamina!"]
                    elif button.text == "Exit Game":
                        game_state.change_state(GameState.STATE_GAME_OVER)
            draw_arena_menu(screen, game_state.player, arena_buttons, game_state.battles_won, fonts)
                
        elif game_state.current_state == GameState.STATE_PRE_BATTLE:
            pre_battle_button.check_hover(mouse_pos)
            if mouse_clicked and pre_battle_button.is_clicked(mouse_pos, mouse_clicked):
                game_state.player.position = list(game_state.player.base_position)
                game_state.enemy.position = list(game_state.enemy.base_position)
                game_state.change_state(GameState.STATE_BATTLE)
            draw_pre_battle(screen, game_state.player, game_state.enemy, pre_battle_button, game_state.pre_battle_timer, fonts)
                
        elif game_state.current_state == GameState.STATE_BATTLE:
            game_state.player.update_animation()
            game_state.enemy.update_animation()
            
            distance = abs(game_state.player.position[0] - game_state.enemy.position[0])
            within_attack_range = distance <= 100
            
            if game_state.battle_turn == "player":
                for button in battle_buttons:
                    # Reset button state
                    button.set_disabled(False)
                    button.color = button.base_color
                    
                    # Disable buttons based on conditions
                    if button.text == "Move Left":
                        if game_state.player.stamina < game_state.player.move_stamina_cost or game_state.player.position[0] <= 50:
                            button.set_disabled(True)
                    elif button.text == "Move Right":
                        if (within_attack_range or 
                            game_state.player.stamina < game_state.player.move_stamina_cost or 
                            game_state.player.position[0] >= WIDTH - 50):
                            button.set_disabled(True)
                    elif button.text == "Quick Strike":
                        if (game_state.player.stamina < game_state.player.skills["Quick Strike"]["stamina_cost"] or
                            not within_attack_range):
                            button.set_disabled(True)
                    elif button.text == "Heavy Strike":
                        if (game_state.player.stamina < game_state.player.skills["Heavy Strike"]["stamina_cost"] or
                            not within_attack_range):
                            button.set_disabled(True)
                    elif button.text == "Leap Attack":
                        if (within_attack_range or 
                            game_state.player.stamina < game_state.player.skills["Leap Attack"]["stamina_cost"] or 
                            game_state.player.position[0] >= game_state.enemy.position[0]):
                            button.set_disabled(True)
                    elif button.text == "Rest":
                        if game_state.player.stamina >= game_state.player.max_stamina:
                            button.set_disabled(True)
                    elif button.text == "Jump Fwd":
                        if (game_state.player.stamina < game_state.player.jump_stamina_cost or 
                            game_state.player.is_jumping or 
                            game_state.player.position[0] >= WIDTH - 50):
                            button.set_disabled(True)
                    elif button.text == "Jump Bwd":
                        if (game_state.player.stamina < game_state.player.jump_stamina_cost or 
                            game_state.player.is_jumping or 
                            game_state.player.position[0] <= 50):
                            button.set_disabled(True)
                    
                    button.check_hover(mouse_pos)
                    if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                        result = None
                        if button.text == "Move Left":
                            result = game_state.player.move_left(game_state.enemy)
                        elif button.text == "Move Right":
                            result = game_state.player.move_right(game_state.enemy)
                        elif button.text == "Quick Strike":
                            result = game_state.player.attack(game_state.enemy, "Quick Strike")
                        elif button.text == "Heavy Strike":
                            result = game_state.player.attack(game_state.enemy, "Heavy Strike")
                        elif button.text == "Leap Attack":
                            result = game_state.player.attack(game_state.enemy, "Leap Attack")
                        elif button.text == "Rest":
                            result = game_state.player.rest()
                        elif button.text == "Jump Fwd":
                            result = game_state.player.jump("forward")
                        elif button.text == "Jump Bwd":
                            result = game_state.player.jump("backward")
                        
                        if result:
                            game_state.battle_log.append(result["message"])
                            if game_state.enemy.health <= 0:
                                game_state.battle_log.append(f"{game_state.enemy.name} has been defeated!")
                                game_state.player.gain_experience(game_state.enemy.exp_reward)
                                game_state.player.gold += game_state.enemy.gold_reward
                                game_state.battle_log.append(f"You gained {game_state.enemy.exp_reward} exp and {game_state.enemy.gold_reward} gold!")
                                game_state.battles_won += 1
                                game_state.battle_action_delay = 60
                                game_state.change_state(GameState.STATE_ARENA_MENU)
                            elif result.get("success", False):
                                game_state.battle_turn = "enemy"
                                game_state.battle_action_delay = 30
            
            if game_state.battle_turn == "enemy" and game_state.battle_action_delay <= 0:
                result = game_state.enemy.choose_action(game_state.player)
                game_state.battle_log.append(result["message"])
                if game_state.player.health <= 0:
                    game_state.battle_log.append(f"{game_state.player.name} has been defeated!")
                    game_state.battle_action_delay = 60
                    game_state.change_state(GameState.STATE_GAME_OVER)
                elif result.get("success", False):
                    game_state.battle_turn = "player"
            
            if game_state.battle_action_delay > 0:
                game_state.battle_action_delay -= 1
            
            draw_battle_arena(screen, game_state.player, game_state.enemy, game_state.battle_log, game_state.battle_turn, fonts)
            if game_state.battle_turn == "player":
                for button in battle_buttons:
                    button.draw(screen)
                
        elif game_state.current_state == GameState.STATE_CHARACTER_STATS:
            stats_back_button.check_hover(mouse_pos)
            if mouse_clicked and stats_back_button.is_clicked(mouse_pos, mouse_clicked):
                game_state.change_state(GameState.STATE_ARENA_MENU)
            draw_character_stats(screen, game_state.player, stats_back_button, fonts)
            
        elif game_state.current_state == GameState.STATE_GAME_OVER:
            for button in game_over_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Return to Main Menu":
                        game_state.change_state(GameState.STATE_MAIN_MENU)
                    elif button.text == "New Game":
                        game_state.change_state(GameState.STATE_CHARACTER_CREATION)
                        game_state.input_name = "Hero"
                        game_state.current_stats = {'strength': 0, 'agility': 0, 'defense': 0, 'stamina': 0, 'vitality': 0}
                    elif button.text == "Exit":
                        running = False
            draw_game_over(screen, game_state.player, game_state.battles_won, game_over_buttons, fonts)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()