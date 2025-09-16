"""
Cross-word validation tests

Ensure that every generated move only creates valid perpendicular words.
"""

from typing import Tuple


def place_word(board_state, word: str, row: int, col: int, direction: str) -> None:
    """Helper: place an existing word on the board as pre-existing tiles."""
    if direction == 'right':
        for i, ch in enumerate(word):
            assert board_state.place_tile(row, col + i, ch, is_blank=False, is_placed_this_turn=False)
    else:
        for i, ch in enumerate(word):
            assert board_state.place_tile(row + i, col, ch, is_blank=False, is_placed_this_turn=False)
    board_state.find_anchors()


def build_perpendicular_word(board_state, pos: Tuple[int, int], ch: str, direction: str) -> str:
    """Construct the perpendicular word for a hypothetical placement at pos with ch."""
    row, col = pos
    if direction == 'right':
        dr_back, dc_back = -1, 0
        dr_fwd, dc_fwd = 1, 0
    else:  # down
        dr_back, dc_back = 0, -1
        dr_fwd, dc_fwd = 0, 1

    # Move to start
    r, c = row, col
    while 0 <= r + dr_back < 15 and 0 <= c + dc_back < 15:
        tile = board_state.get_tile(r + dr_back, c + dc_back)
        if tile is None or tile.is_empty():
            break
        r += dr_back
        c += dc_back

    # Collect
    chars = []
    cur_r, cur_c = r, c
    while 0 <= cur_r < 15 and 0 <= cur_c < 15:
        if cur_r == row and cur_c == col:
            chars.append(ch)
        else:
            tile = board_state.get_tile(cur_r, cur_c)
            if tile is None or tile.is_empty():
                break
            chars.append(tile.letter)
        cur_r += dr_fwd
        cur_c += dc_fwd

    return ''.join(chars)


def test_all_generated_moves_have_valid_cross_words(board_state, small_wordset_solver):
    """For a board with existing words, every move must have valid perpendicular crosses."""
    # Pre-place a common word to force crossings
    place_word(board_state, 'HELLO', 7, 5, 'right')

    rack = list('WORLD__')
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=100)

    # For each move, validate every perpendicular cross word
    for mv in moves:
        for r, c, ch, _ in mv.tiles:
            cross = build_perpendicular_word(board_state, (r, c), ch, mv.direction)
            if len(cross) > 1:
                assert small_wordset_solver.wordset.is_word(cross), f"Invalid cross '{cross}' at {(r,c)} for move {mv.word}"


def test_moves_avoid_invalid_crosses(board_state, small_wordset_solver):
    """Build a setup that would create an invalid cross like 'AG'; ensure such moves are absent."""
    # Place a single letter to the left of a common anchor position
    assert board_state.place_tile(10, 6, 'A', is_blank=False, is_placed_this_turn=False)
    board_state.find_anchors()

    rack = list('DOG___')
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=200)

    # There should be no move that places 'G' at (10,7) going down, since that would make cross 'AG'
    forbidden = []
    for mv in moves:
        for r, c, ch, _ in mv.tiles:
            if (r, c) == (10, 7) and ch == 'G' and mv.direction == 'down':
                cross = build_perpendicular_word(board_state, (r, c), ch, mv.direction)
                if len(cross) > 1 and not small_wordset_solver.wordset.is_word(cross):
                    forbidden.append((mv.word, mv.tiles, mv.direction))

    assert not forbidden, f"Generated moves with invalid cross detected: {forbidden}"


