"""Test suite for the Orbito game logic."""

import pytest
from orbito.core.game import OrbitGame

# Tests for game initialization
def test_initialisation_plateau():
    """Test if game board is correctly initialized."""
    game = OrbitGame()
    expected = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.get_board() == expected

# Tests for white player moves
def test_is_valid_mouv_White_true():
    """Test valid move for white player on empty cell."""
    game = OrbitGame()
    assert game.is_valid_move(0, 0) == True

def test_is_valid_mouv_White_false_self_ball():
    """Test invalid move for white player on own ball."""
    game = OrbitGame()
    game.board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

def test_is_valid_mouv_White_false_oponent_ball():
    """Test invalid move for white player on opponent's ball."""
    game = OrbitGame()
    game.board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

# Tests for black player moves
def test_is_valid_mouv_black_true():
    """Test valid move for black player on empty cell."""
    game = OrbitGame()
    game.current_player = 2
    assert game.is_valid_move(0, 0) == True

def test_is_valid_mouv_black_false_oponent_ball():
    """Test invalid move for black player on opponent's ball."""
    game = OrbitGame()
    game.current_player = 2
    game.board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

def test_is_valid_mouv_black_false_self_ball():
    """Test invalid move for black player on own ball."""
    game = OrbitGame()
    game.current_player = 2
    game.board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

# Tests for opponent ball detection - White player
def test_is_oponent_ball_white_true():
    """Test opponent ball detection for white player (true case)."""
    game = OrbitGame()
    game.board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False  # Changed according to new logic

def test_is_oponent_ball_white_false_self_ball():
    """Test opponent ball detection for white player with own ball."""
    game = OrbitGame()
    game.board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

def test_is_oponent_ball_white_false_empty():
    """Test opponent ball detection for white player with empty cell."""
    game = OrbitGame()
    assert game.is_valid_move(0, 0) == True  # Empty cell is valid move

# Tests for opponent ball detection - Black player
def test_is_oponent_ball_black_true():
    """Test opponent ball detection for black player (true case)."""
    game = OrbitGame()
    game.current_player = 2
    game.board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False  # Changed according to new logic

def test_is_oponent_ball_black_false_self_ball():
    """Test opponent ball detection for black player with own ball."""
    game = OrbitGame()
    game.current_player = 2
    game.board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    assert game.is_valid_move(0, 0) == False

def test_is_oponent_ball_black_false_empty():
    """Test opponent ball detection for black player with empty cell."""
    game = OrbitGame()
    game.current_player = 2
    assert game.is_valid_move(0, 0) == True  # Empty cell is valid move

# Additional game logic tests
def test_make_move_and_orbit():
    """Test complete move sequence including orbit."""
    game = OrbitGame()
    assert game.make_move(0, 0) == True
    white_wins, black_wins = game.orbit_move()
    assert not white_wins
    assert not black_wins
    assert game.current_player == 2

def test_win_condition_horizontal():
    """Test win detection for horizontal alignment."""
    game = OrbitGame()
    game.board = [
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    assert game.check_win_for_player(1) == True

def test_win_condition_vertical():
    """Test win detection for vertical alignment."""
    game = OrbitGame()
    game.board = [
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0]
    ]
    assert game.check_win_for_player(1) == True

def test_win_condition_diagonal():
    """Test win detection for diagonal alignment."""
    game = OrbitGame()
    game.board = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ]
    assert game.check_win_for_player(1) == True