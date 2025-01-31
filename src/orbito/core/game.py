# src/orbito/core/game.py
"""
Core game logic for the Orbito board game.

This module implements the core game mechanics for Orbito, a strategic board game
where two players compete to align four balls of their color while using rotation
mechanics to outmaneuver their opponent.

The game is played on a 4x4 board where:
    - Players take turns placing balls of their color (White: 1, Black: 2)
    - After placing a ball, players must rotate part of the board
    - The goal is to align 4 balls horizontally, vertically, or diagonally
    - First player to achieve alignment wins

Classes:
    OrbitGame: Main class handling game logic and state management
"""

class OrbitGame:
    """
    Main class implementing Orbito game logic.
    
    This class manages the game state and implements all game rules, including:
    - Board state management
    - Move validation
    - Turn handling
    - Win condition checking
    - Board rotation mechanics
    
    Attributes:
        board (list[list[int]]): 4x4 matrix representing game state where:
            - 0: Empty cell
            - 1: White player's ball
            - 2: Black player's ball
        current_player (int): Identifier for current player (1: White, 2: Black)
        move_made (bool): Tracks if a move has been made in current turn
    
    Example:
        >>> game = OrbitGame()
        >>> game.make_move(0, 0)  # Place ball at top-left
        True
        >>> game.orbit_move()     # Rotate the board
        (False, False)            # No winner yet (white_wins, black_wins)
    """
    
    def __init__(self):
        """
        Initialize a new game of Orbito.

        Creates an empty 4x4 board, sets White as first player, and initializes
        game state tracking variables.
        """
        self.board = self.init_game()
        self.current_player = 1  # 1 for White, 2 for Black
        self.move_made = False
        
    @staticmethod
    def init_game():
        """
        Create and initialize an empty game board.
        
        Returns:
            list[list[int]]: 4x4 matrix of zeros representing empty board
        
        Note:
            Board uses following representation:
            - 0: Empty cell
            - 1: White player's ball
            - 2: Black player's ball
        """
        return [[0 for _ in range(4)] for _ in range(4)]
    
    def make_move(self, row, col):
        """
        Attempt to place a ball at specified board position.
        
        Args:
            row (int): Row index (0-3) from top
            col (int): Column index (0-3) from left
        
        Returns:
            bool: True if move was valid and executed, False otherwise
        
        Note:
            Move is considered valid when:
            - No move has been made this turn
            - Target cell is empty
            - Coordinates are within board bounds
        """
        if not self.move_made and self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.move_made = True
            return True
        return False
    
    def is_valid_move(self, row, col):
        """
        Check if a move to specified position is valid.
        
        Args:
            row (int): Row index to check
            col (int): Column index to check
        
        Returns:
            bool: True if move to specified position would be valid
        
        Note:
            A move is valid when:
            - Position is within board bounds (0-3 for both coordinates)
            - Target cell is empty (contains 0)
        """
        return 0 <= row < 4 and 0 <= col < 4 and self.board[row][col] == 0
    
    def orbit_move(self):
        """
        Execute the orbit (rotation) move on the board.
        
        The orbit move rotates balls on the board in a specific pattern:
        - Outer ring rotates clockwise
        - Inner square rotates counterclockwise
        
        Returns:
            tuple[bool, bool]: (white_wins, black_wins) indicating if either
                or both players have won after rotation
        
        Note:
            - Move can only be executed if a ball has been placed this turn
            - After rotation, switches to other player unless game is won
        """
        if not self.move_made:
            return False, False
            
        # Create new board for rotated state
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        
        # Define rotation movements for all affected positions
        moves = {
            # Outer ring clockwise rotation
            (0,0): (1,0), (1,0): (2,0), (2,0): (3,0),  # Left side down
            (3,0): (3,1), (3,1): (3,2), (3,2): (3,3),  # Bottom right
            (3,3): (2,3), (2,3): (1,3), (1,3): (0,3),  # Right side up
            (0,3): (0,2), (0,2): (0,1), (0,1): (0,0),  # Top left
            # Inner square counterclockwise rotation
            (1,1): (2,1), (2,1): (2,2), (2,2): (1,2), (1,2): (1,1)
        }
        
        # Apply rotation movements to create new board state
        for (old_row, old_col), (new_row, new_col) in moves.items():
            new_board[new_row][new_col] = self.board[old_row][old_col]
        
        self.board = new_board
        
        # Check win conditions
        white_wins = self.check_win_for_player(1)
        black_wins = self.check_win_for_player(2)
        
        # If no winner, prepare for next turn
        if not (white_wins or black_wins):
            self.current_player = 3 - self.current_player  # Switch players (1->2 or 2->1)
            self.move_made = False
            
        return white_wins, black_wins
    
    def check_win_for_player(self, player):
        """
        Check if specified player has achieved a winning condition.
        
        Args:
            player (int): Player number to check (1: White, 2: Black)
        
        Returns:
            bool: True if player has aligned 4 balls, False otherwise
        
        Note:
            Checks all possible winning alignments:
            - 4 horizontal lines
            - 4 vertical lines
            - 2 diagonals
        """
        # Define all possible winning combinations
        winning_conditions = [
            [(i,j) for j in range(4)] for i in range(4)  # Horizontal lines
        ] + [
            [(j,i) for j in range(4)] for i in range(4)  # Vertical lines
        ] + [
            [(i,i) for i in range(4)],                   # Main diagonal
            [(i,3-i) for i in range(4)]                  # Other diagonal
        ]
        
        # Check if any winning condition is met
        return any(all(self.board[row][col] == player 
                      for row, col in condition)
                  for condition in winning_conditions)
    
    def get_board(self):
        """
        Get current board state.
        
        Returns:
            list[list[int]]: Current game board matrix
        """
        return self.board

    def get_current_player(self):
        """
        Get current player number.
        
        Returns:
            int: Current player (1: White, 2: Black)
        """
        return self.current_player
    
    def is_board_full(self):
        """
        Check if the board is full (no empty cells).
        
        Returns:
            bool: True if all cells are occupied, False otherwise
        """
        return all(all(cell != 0 for cell in row) for row in self.board)
        
    def reset_game(self):
        """
        Reset game to initial state.
        
        This includes:
        - Clearing the board
        - Setting White as first player
        - Resetting move tracking
        """
        self.board = self.init_game()
        self.current_player = 1
        self.move_made = False