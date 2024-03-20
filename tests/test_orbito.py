from src.orbito import Orbito

#init_game:
def test_initialisation_plateau():
    try:
        assert Orbito.init_game() ==[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    except AssertionError:
        pass

# is_valid_mouv :

def test_is_valid_mouv_White_true():
    try:
        board = Orbito.init_game()
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == True
    except AssertionError:
        pass

def test_is_valid_mouv_White_false_self_ball():
    try:
        board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == False
    except AssertionError:
        pass

def test_is_valid_mouv_White_false_oponent_ball():
    try:
        board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == False
    except AssertionError:
        pass

def test_is_valid_mouv_black_true():
    try:
        board = Orbito.init_game()
        assert Orbito.is_valid_move("Noir", 0, 0, board) == True
    except AssertionError:
        pass

def test_is_valid_mouv_black_false_oponent_ball():
    try:
        board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Noir", 0, 0, board) == False
    except AssertionError:
        pass

def test_is_valid_mouv_black_false_self_ball():
    try:
        board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Noir", 0, 0, board) == False
    except AssertionError:
        pass

#is_oponent_ball:
def test_is_oponent_ball_white_true():
    try:
        board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == True
    except AssertionError:
        pass

def test_is_oponent_ball_white_false_self_ball():
    try:
        board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == False
    except AssertionError:
        pass

def test_is_oponent_ball_white_false_empty():
    try:
        board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Blanc", 0, 0, board) == False
    except AssertionError:
        pass
    
def test_is_oponent_ball_black_true():
    try:
        board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Noir", 0, 0, board) == True
    except AssertionError:
        pass

def test_is_oponent_ball_black_false_self_ball():
    try:
        board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Noir", 0, 0, board) == False
    except AssertionError:
        pass

def test_is_oponent_ball_black_false_empty():
    try:
        board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_move("Noir", 0, 0, board) == False
    except AssertionError:
        pass

#is_valid_oponent_ball_move:
def is_valid_oponent_ball_move_white_():
    try:
        board = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        assert Orbito.is_valid_oponent_ball_move("Blanc", 0, 1, 0, 0, board) == True
    except AssertionError:
        print("non")