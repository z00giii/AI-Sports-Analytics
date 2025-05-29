class FoulDetector:
    def __init__(self, sport='basketball'):
        self.sport = sport
        self.rules = self._load_rules(sport)
        
    def _load_rules(self, sport):
        if sport == 'basketball':
            return {
                'traveling': self._detect_traveling,
                'charging': self._detect_charging,
                'shooting_foul': self._detect_shooting_foul
            }
        else:
            return {
                'offside': self._detect_offside,
                'dangerous_tackle': self._detect_dangerous_tackle,
                'handball': self._detect_handball
            }
    
    def detect_fouls(self, game_state):
        fouls = []
        for rule_name, rule_func in self.rules.items():
            if rule_func(game_state):
                fouls.append(rule_name)
        return fouls
    
    # Basketball specific foul detection methods
    def _detect_traveling(self, game_state):
        player_positions = game_state['player_positions']
        ball_handler = game_state['ball_handler']
        pivot_foot = player_positions[ball_handler]['pivot_foot']
        
        # Check if pivot foot has moved significantly
        return pivot_foot['distance_moved'] > 0.1  # threshold in meters
    
    def _detect_charging(self, game_state):
        offensive_player = game_state['ball_handler']
        defensive_players = game_state['defensive_players']
        
        for defender in defensive_players:
            if self._check_collision(offensive_player, defender):
                return defender['position']['established']
        return False
    
    # Football specific foul detection methods
    def _detect_offside(self, game_state):
        # Simplified offside detection
        attacking_players = game_state['attacking_players']
        second_last_defender = game_state['second_last_defender']
        ball_position = game_state['ball_position']
        
        for player in attacking_players:
            if player['position']['x'] > second_last_defender['x'] and \
               player['position']['x'] > ball_position['x']:
                return True
        return False

# Usage example
foul_detector = FoulDetector(sport='basketball')
game_state = {
    'player_positions': {...},
    'ball_handler': 23,
    'defensive_players': [...]
}

fouls = foul_detector.detect_fouls(game_state)
if fouls:
    print(f"Detected fouls: {', '.join(fouls)}")
