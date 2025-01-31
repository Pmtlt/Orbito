"""Pytest configuration and fixtures."""

import pytest
from orbito.core import OrbitGame

@pytest.fixture
def empty_game():
    return OrbitGame()

@pytest.fixture
def game_with_moves():
    game = OrbitGame()
    game.make_move(0, 0)
    game.orbit_move()
    return game