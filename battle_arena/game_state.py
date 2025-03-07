class GameState:
    # Game state constants
    STATE_MAIN_MENU = 0
    STATE_CHARACTER_CREATION = 1
    STATE_BATTLE = 2
    STATE_ARENA_MENU = 3
    STATE_CHARACTER_STATS = 4
    STATE_GAME_OVER = 5
    
    def __init__(self):
        self.current_state = self.STATE_MAIN_MENU
        self.player = None
        self.enemy = None
        self.battles_won = 0
        self.battle_turn = "player"
        self.battle_log = []
        self.battle_action_delay = 0
        
        # Character creation variables
        self.input_name = "Hero"
        self.selected_class = None
    
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