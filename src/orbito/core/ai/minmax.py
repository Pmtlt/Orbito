"""Minimax AI implementation."""
from copy import deepcopy
from .base import BaseAI
from .evaluator import evaluate_position

class MinimaxAI(BaseAI):
    def get_best_move(self, game):
        """Find best move using minimax algorithm."""
        best_score = float('-inf')
        best_move = None
        
        for row in range(4):
            for col in range(4):
                if game.is_valid_move(row, col):
                    game_copy = deepcopy(game)
                    game_copy.make_move(row, col)
                    score = self._minimax(
                        game_copy, 
                        self.depth_map[self.difficulty], 
                        False
                    )
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                        
        return best_move
        
    def _minimax(self, game, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            game: Current game state
            depth: Search depth remaining
            maximizing_player: True if AI's turn
            alpha, beta: Alpha-beta pruning bounds
            
        Returns:
            int: Position score
        """
        if depth == 0 or game.check_win_for_player(1) or game.check_win_for_player(2):
            return evaluate_position(game, self.player)
            
        if maximizing_player:
            max_eval = float('-inf')
            for row in range(4):
                for col in range(4):
                    if game.is_valid_move(row, col):
                        game_copy = deepcopy(game)
                        game_copy.make_move(row, col)
                        eval = self._minimax(game_copy, depth - 1, False, alpha, beta)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(4):
                for col in range(4):
                    if game.is_valid_move(row, col):
                        game_copy = deepcopy(game)
                        game_copy.make_move(row, col)
                        eval = self._minimax(game_copy, depth - 1, True, alpha, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval