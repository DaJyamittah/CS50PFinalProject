"""Test for final project."""

import numpy as np
import pytest

from project import get_xyz, inspect, update


def test_inspect():
    board = np.full((7, 7), False)
    board[1, 1] = True
    board[2, 1] = True
    assert inspect(board, 1, 1) == [False, False, False,
                                    False, False, False,
                                    True, False]

    board = [[False, False, False],
             [False, True, False],
             [False, True, False]]
    with pytest.raises(ValueError):
        assert inspect(board, 1, 1)

    board = "blah blah blah"
    with pytest.raises(ValueError):
        assert inspect(board, 1, 1)

    board = np.full((3, 3), False)
    board[1, 0] = True
    with pytest.raises(ValueError):
        assert inspect(board, 2, 1)


def test_update():
    board = np.full((7, 7), False)
    board[2, 2] = True
    board[2, 3] = True
    board[2, 4] = True
    new_board = np.full((7, 7), False)
    new_board[1, 3] = True
    new_board[2, 3] = True
    new_board[3, 3] = True
    assert np.all(update(board)) == np.all(new_board)

def test_get_xyz():
    board = np.full((7, 7), False)
    board[2, 2] = True
    board[2, 3] = True
    board[2, 4] = True
    assert get_xyz(board, 5) == ([2, 2, 2, 1, 2, 3, 2, 2, 2, 1, 2, 3, 2, 2, 2],
                                [2, 3, 4, 3, 3, 3, 2, 3, 4, 3, 3, 3, 2, 3, 4],
                                [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])

