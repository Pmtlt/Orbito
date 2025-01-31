"""AI player implementation for Orbito game."""
from copy import deepcopy
import random

class OrbitoAI:
    """
    AI player for Orbito using minimax algorithm.
    """
    def __init__(self, player_number=2):
        """
        Initialize AI player.
        
        Args:
            player_number (int): AI player number (1 for white, 2 for black)
        """
        self.player = player_number
        
    def get_best_move(self, game):
        """
        Find the best move for the current game state.
        
        Args:
            game: Current game instance
            
        Returns:
            tuple: (row, col) for the best move found
        """
        # Get all valid moves
        valid_moves = []
        for i in range(4):
            for j in range(4):
                if game.is_valid_move(i, j):
                    valid_moves.append((i, j))
                    
        if not valid_moves:
            return None
            
        # For now, just return a random valid move
        # Later we'll implement minimax here
        return random.choice(valid_moves)
        
    def evaluate_board(self, game):
        """
        Evaluate the current board state.
        Positive score favors AI, negative favors opponent.
        
        Args:
            game: Current game instance
        
        Returns:
            int: Score for current position
        """
        if game.check_win_for_player(self.player):
            return 1000
        elif game.check_win_for_player(3 - self.player):
            return -1000
            
        # Add more sophisticated evaluation here later
        return 0