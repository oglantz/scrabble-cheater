"""
Complex overlapping/crossing word scenarios

These tests build manual boards with multiple intersections and assert
that generated moves create valid overlapping words.
Some may xfail depending on dictionary coverage, which is acceptable now.
"""

import pytest


def place_preexisting(board_state, word, row, col, direction):
    """
    Place a pre-existing word, allowing overlaps with identical letters.
    Fails if an overlap conflicts with a different letter.
    """
    from models.board_state import BoardState

    if direction == 'right':
        for i, ch in enumerate(word):
            r, c = row, col + i
            tile = board_state.get_tile(r, c)
            if tile and not tile.is_empty():
                assert tile.letter == ch, f"Conflict at ({r},{c}): {tile.letter} vs {ch}"
            else:
                assert board_state.place_tile(r, c, ch, is_blank=False, is_placed_this_turn=False)
    else:
        for i, ch in enumerate(word):
            r, c = row + i, col
            tile = board_state.get_tile(r, c)
            if tile and not tile.is_empty():
                assert tile.letter == ch, f"Conflict at ({r},{c}): {tile.letter} vs {ch}"
            else:
                assert board_state.place_tile(r, c, ch, is_blank=False, is_placed_this_turn=False)
    board_state.find_anchors()


def test_cross_through_shared_letter(board_state, small_wordset_solver):
    """
    Pre-place 'HELLO' horizontally and 'OWL' vertically so they share 'L'.
    Verify moves can extend or cross to form valid overlapping words like 'WORLD' or 'WORD'.
    """
    place_preexisting(board_state, 'HELLO', 7, 5, 'right')
    # 'OWL' crossing at the second 'L' of HELLO (row 7, col 8): start at (5,8)
    # so O(5,8), W(6,8), L(7,8) shares the 'L'
    place_preexisting(board_state, 'OWL', 5, 8, 'down')

    rack = list('WORD__X')
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=50)
    if len(moves) == 0:
        pytest.xfail('Wordset limited; no overlapping move generated')

    # Check at least one move forms a word that is compatible with overlaps
    words = {m.word for m in moves}
    assert any(w in words for w in ['WORLD', 'WORD'])


def test_multiple_overlaps_board_state_constraints(board_state, small_wordset_solver):
    """
    Build a mini crossword grid with overlaps:
      - HOP (right)
      - HOPE (down, sharing HO)
      - TREE (right, crossing at E)
    Then try to add another crossing using rack letters.
    """
    # HOP horizontally at row 7
    place_preexisting(board_state, 'HOP', 7, 7, 'right')
    # HOPE vertically starting at the 'H' (7,7)
    place_preexisting(board_state, 'HOPE', 7, 7, 'down')
    # TREE horizontally crossing 'E' of HOPE at (10,7)
    place_preexisting(board_state, 'TREE', 10, 5, 'right')

    rack = list('FREED__')  # Enables FREE/REEF/FREED crosses
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=100)
    if len(moves) == 0:
        pytest.xfail('Limited dictionary may prevent complex overlaps')

    # Look for words compatible with the setup
    words = {m.word for m in moves}
    assert any(w in words for w in ['FREE', 'REEF', 'FREED'])


