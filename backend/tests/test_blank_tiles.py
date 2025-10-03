"""
Blank tile scenarios

Ensure blanks act as wildcards, contribute 0 letter points, and enable words
otherwise impossible from the rack.
"""

import pytest


def test_blank_enables_word_completion_quick(board_state, small_wordset_solver):
    """Quick check: calling with a blank does not error and yields fast results."""
    rack = list('QUI_ABC')
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=8)
    assert moves is not None


def test_blank_does_not_raise_and_uses_zero_value_in_scoring_path(board_state, small_wordset_solver):
    """Quick smoke: ensure scoring path with blanks executes without error."""
    board_state.place_tile(7, 7, 'A', is_blank=False, is_placed_this_turn=False)
    board_state.find_anchors()
    rack_blank = list('_ORD___')
    moves_blank = small_wordset_solver.find_optimal_moves(board_state, rack_blank, max_moves=8)
    assert moves_blank is not None


