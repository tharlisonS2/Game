class GameState:
    # Game state constants
    STATE_MAIN_MENU = 0
    STATE_CHARACTER_CREATION = 1
    STATE_BATTLE = 2
    STATE_ARENA_MENU = 3
    STATE_CHARACTER_STATS = 4
    STATE_GAME_OVER = 5
    STATE_PRE_BATTLE = 6  # New state for showing stats before battle
    
    def __init__(self):
        self.current_state = self.STATE_MAIN_MENU
        self.player = None
        self.enemy = None
        self.battles_won = 0
        self.battle_turn = "player"
        self.battle_log = []
        self.battle_action_delay = 0
        self.pre_battle_timer = 0  # Timer for pre-battle screen
        
        # Character creation variables
        self.input_name = "Hero"
        self.stat_points = 15  # Total points to distribute
        self.current_stats = {
            'strength': 0, 
            'agility': 0,  # Renamed from 'speed' for clarity
            'defense': 0   # Renamed from 'armor' for clarity
        }
        
        # Stat button detection rects
        self.stat_buttons = {}
    
    def change_state(self, new_state):
        self.current_state = new_state
        
    def reset_battle(self):
        self.battle_turn = "player"
        self.battle_log = []
        self.battle_action_delay = 0
    
    def add_battle_log(self, message):
        self.battle_log.append(message)
    
    def clear_battle_log(self):
        self.battle_log = []
    
    def increment_battles_won(self):
        self.battles_won += 1
        
    def get_remaining_points(self):
        """Calculate remaining stat points"""
        used_points = sum(self.current_stats.values())
        return self.stat_points - used_points
    
    def increase_stat(self, stat_name):
        """Increase a stat if points are available"""
        if self.get_remaining_points() > 0:
            self.current_stats[stat_name] += 1
            return True
        return False
    
    def decrease_stat(self, stat_name):
        """Decrease a stat if it's above 0"""
        if self.current_stats[stat_name] > 0:
            self.current_stats[stat_name] -= 1
            return True
        return False