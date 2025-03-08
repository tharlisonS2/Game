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
    draw_pre_battle  # Add the new function here
)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Arena")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    fonts = {
        'small': pygame.font.SysFont('Arial', 18),
        'medium': pygame.font.SysFont('Arial', 24),
        'large': pygame.font.SysFont('Arial', 32),
        'title': pygame.font.SysFont('Arial', 48, bold=True)
    }
    
    # Initialize game state
    game_state = GameState()
    
    # Main menu buttons
    main_menu_buttons = [
        Button(WIDTH/2 - 100, 250, 200, 50, "New Game"),
        Button(WIDTH/2 - 100, 320, 200, 50, "Exit")
    ]
    
    # Character creation stat buttons
    char_creation_buttons = []
    
    # Stat increase/decrease buttons for each stat
    y_position = 240
    for stat in game_state.current_stats.keys():
        # Decrease button
        char_creation_buttons.append(
            Button(WIDTH/2 - 180, y_position, 30, 30, "-", color=RED)
        )
        # Increase button
        char_creation_buttons.append(
            Button(WIDTH/2 - 30, y_position, 30, 30, "+", color=GREEN)
        )
        y_position += 50
    
    # Create character button
    char_creation_buttons.append(
        Button(WIDTH/2 - 100, 400, 200, 50, "Create Character")
    )
    
    # Arena menu buttons
    arena_buttons = [
        Button(WIDTH/2 - 100, 320, 200, 50, "Enter Battle"),
        Button(WIDTH/2 - 100, 380, 200, 50, "View Stats"),
        Button(WIDTH/2 - 100, 440, 200, 50, "Rest (Heal)"),
        Button(WIDTH/2 - 100, 500, 200, 50, "Exit Game")
    ]
    
    # Pre-battle screen skip button
    pre_battle_button = Button(WIDTH/2 - 100, HEIGHT - 80, 200, 40, "Skip to Battle")
    
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
        Button(WIDTH/2 - 100, 330, 200, 50, "Return to Main Menu"),
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
                if game_state.current_state == GameState.STATE_CHARACTER_CREATION:
                    if event.key == pygame.K_BACKSPACE:
                        game_state.input_name = game_state.input_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if game_state.get_remaining_points() == 0 and game_state.input_name:
                            game_state.player = Character(game_state.input_name, game_state.current_stats)
                            game_state.change_state(GameState.STATE_ARENA_MENU)
                    else:
                        # Limit name length and only add printable characters
                        if len(game_state.input_name) < 15 and event.unicode.isprintable():
                            game_state.input_name += event.unicode
        
        # Main menu state
        if game_state.current_state == GameState.STATE_MAIN_MENU:
            for button in main_menu_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "New Game":
                        game_state.change_state(GameState.STATE_CHARACTER_CREATION)
                        game_state.input_name = "Hero"  # Reset default name
                        game_state.current_stats = {'strength': 0, 'speed': 0, 'armor': 0}
                    elif button.text == "Exit":
                        running = False
            
            # Draw main menu
            draw_main_menu(screen, main_menu_buttons, fonts)
                
        # Character creation state
        elif game_state.current_state == GameState.STATE_CHARACTER_CREATION:
            for i, button in enumerate(char_creation_buttons):
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if i < len(char_creation_buttons) - 1:  # Stat buttons
                        stat_index = i // 2
                        stat_key = list(game_state.current_stats.keys())[stat_index]
                        
                        if i % 2 == 0:  # Decrease button
                            if game_state.current_stats[stat_key] > 0:
                                game_state.current_stats[stat_key] -= 1
                        else:  # Increase button
                            if game_state.get_remaining_points() > 0:
                                game_state.current_stats[stat_key] += 1
                    elif button.text == "Create Character":
                        if game_state.get_remaining_points() == 0 and game_state.input_name:
                            game_state.player = Character(game_state.input_name, game_state.current_stats)
                            game_state.change_state(GameState.STATE_ARENA_MENU)
                            game_state.battles_won = 0
            
            # Draw character creation
            draw_character_creation(screen, char_creation_buttons, game_state, fonts)
                
        # Arena menu state
        elif game_state.current_state == GameState.STATE_ARENA_MENU:
            for i, button in enumerate(arena_buttons):
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Enter Battle":
                        game_state.enemy = generate_enemy(game_state.player.level)
                        game_state.battle_log = [f"A {game_state.enemy.name} (Level {game_state.enemy.level}) appears!"]
                        game_state.battle_turn = "player"
                        game_state.battle_action_delay = 0
                        # Change to pre-battle state instead of battle state
                        game_state.pre_battle_timer = 0
                        game_state.change_state(GameState.STATE_PRE_BATTLE)
                    elif button.text == "View Stats":
                        game_state.change_state(GameState.STATE_CHARACTER_STATS)
                    elif button.text == "Rest (Heal)":
                        health_restored = min(
                            game_state.player.max_health - game_state.player.health, 
                            game_state.player.max_health // 2
                        )
                        stamina_restored = min(
                            game_state.player.max_stamina - game_state.player.stamina, 
                            game_state.player.max_stamina
                        )
                        
                        game_state.player.health += health_restored
                        game_state.player.stamina = game_state.player.max_stamina
                        
                        game_state.battle_log = [
                            f"{game_state.player.name} takes a rest and recovers "
                            f"{health_restored} health and full stamina!"
                        ]
                    elif button.text == "Exit Game":
                        game_state.change_state(GameState.STATE_GAME_OVER)
            
            # Draw arena menu
            draw_arena_menu(screen, game_state.player, arena_buttons, game_state.battles_won, fonts)
                
        # Pre-battle state - NEW STATE
        elif game_state.current_state == GameState.STATE_PRE_BATTLE:
            # Check for skip button click
            pre_battle_button.check_hover(mouse_pos)
            if mouse_clicked and pre_battle_button.is_clicked(mouse_pos, mouse_clicked):
                game_state.change_state(GameState.STATE_BATTLE)
                
            # Increment timer
            game_state.pre_battle_timer += 1
            
            # Auto-transition after countdown (about 3 seconds)
            if game_state.pre_battle_timer >= 60:  # 60 frames = about 3 seconds at 60 FPS
                game_state.change_state(GameState.STATE_BATTLE)
            
            # Draw pre-battle screen
            draw_pre_battle(screen, game_state.player, game_state.enemy, pre_battle_button, game_state.pre_battle_timer, fonts)
                
        # Battle state
        elif game_state.current_state == GameState.STATE_BATTLE:
            # Update character animations
            game_state.player.update_animation()
            game_state.enemy.update_animation()
            
            # Handle battle turns
            if game_state.battle_turn == "player":
                for i, button in enumerate(battle_buttons):
                    button.check_hover(mouse_pos)
                    if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                        result = None
                        
                        if button.text == "Quick Strike":
                            result = game_state.player.attack(game_state.enemy, "Quick Strike")
                        elif button.text == "Heavy Strike":
                            result = game_state.player.attack(game_state.enemy, "Heavy Strike")
                        elif button.text == "Rest":
                            result = game_state.player.rest()
                        
                        if result:
                            game_state.battle_log.append(result["message"])
                            
                            # Check if enemy is defeated
                            if game_state.enemy.health <= 0:
                                game_state.battle_log.append(f"{game_state.enemy.name} has been defeated!")
                                game_state.player.gain_experience(game_state.enemy.exp_reward)
                                game_state.player.gold += game_state.enemy.gold_reward
                                game_state.battle_log.append(
                                    f"You gained {game_state.enemy.exp_reward} experience "
                                    f"and {game_state.enemy.gold_reward} gold!"
                                )
                                game_state.battles_won += 1
                                game_state.battle_action_delay = 60  # Set delay before returning to arena menu
                                game_state.change_state(GameState.STATE_ARENA_MENU)
                            else:
                                game_state.battle_turn = "enemy"
                                game_state.battle_action_delay = 30  # Delay before enemy's turn
            
            # Enemy turn
            if game_state.battle_turn == "enemy" and game_state.battle_action_delay <= 0:
                result = game_state.enemy.choose_action(game_state.player)
                game_state.battle_log.append(result["message"])
                
                # Check if player is defeated
                if game_state.player.health <= 0:
                    game_state.battle_log.append(f"{game_state.player.name} has been defeated!")
                    game_state.battle_action_delay = 60
                    game_state.change_state(GameState.STATE_GAME_OVER)
                else:
                    game_state.battle_turn = "player"
            
            # Update action delay
            if game_state.battle_action_delay > 0:
                game_state.battle_action_delay -= 1
            
            # Draw battle screen
            draw_battle_arena(screen, game_state.player, game_state.enemy, game_state.battle_log, game_state.battle_turn, fonts)
            
            # Only draw buttons during player's turn
            if game_state.battle_turn == "player":
                for button in battle_buttons:
                    button.draw(screen)
                
        # Character stats state
        elif game_state.current_state == GameState.STATE_CHARACTER_STATS:
            stats_back_button.check_hover(mouse_pos)
            if mouse_clicked and stats_back_button.is_clicked(mouse_pos, mouse_clicked):
                game_state.change_state(GameState.STATE_ARENA_MENU)
                
            # Draw character stats
            draw_character_stats(screen, game_state.player, stats_back_button, fonts)   
            
        # Game over state
        elif game_state.current_state == GameState.STATE_GAME_OVER:
            for button in game_over_buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Return to Main Menu":
                        game_state.change_state(GameState.STATE_MAIN_MENU)
                    elif button.text == "New Game":
                        game_state.change_state(GameState.STATE_CHARACTER_CREATION)
                        game_state.input_name = "Hero"
                        game_state.current_stats = {'strength': 0, 'speed': 0, 'armor': 0}
                    elif button.text == "Exit":
                        running = False
                        
            # Draw game over screen
            draw_game_over(screen, game_state.player, game_state.battles_won, game_over_buttons, fonts)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()