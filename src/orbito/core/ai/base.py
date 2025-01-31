"""Base class for AI players."""
from abc import ABC, abstractmethod

class BaseAI(ABC):
    """Abstract base class for AI implementations."""
    
    def __init__(self, player_number=2, difficulty='medium'):
        """
        Initialize AI player.
        
        Args:
            player_number (int): AI player number (1:white, 2:black)
            difficulty (str): 'easy', 'medium', or 'hard'
        """
        self.player = player_number
        self.difficulty = difficulty
        self.depth_map = {
            'easy': 2,
            'medium': 3,
            'hard': 4
        }
        
    @abstractmethod
    def get_best_move(self, game):
        """Get best move for current game state."""
        pass