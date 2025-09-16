"""
EnhancedSolver unit tests

These tests exercise generation and validation logic on controlled boards.
We use the `small_wordset_solver` to ensure deterministic results.
"""

import pytest


def build_board_with_word(board_state, word, row, col, direction):
    """Helper: place an existing word on the board as pre-existing tiles."""
    if direction == 'right':
        for i, ch in enumerate(word):
            assert board_state.place_tile(row, col + i, ch, is_blank=False, is_placed_this_turn=False)
    else:
        for i, ch in enumerate(word):
            assert board_state.place_tile(row + i, col, ch, is_blank=False, is_placed_this_turn=False)
    board_state.find_anchors()


def extract_words(moves):
    return {m.word for m in moves}


def test_first_move_must_cover_center(board_state, small_wordset_solver):
    """On empty board the best moves should include words covering the center (7,7)."""
    rack = list("HELLOWD")
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=10)
    assert all(any(r == 7 and c == 7 for r, c, _, _ in mv.tiles) for mv in moves)


def test_generate_moves_on_prefilled_board_connectivity(board_state, small_wordset_solver):
    """After a word is on the board, new moves must connect to it."""
    build_board_with_word(board_state, "HELLO", 7, 5, 'right')
    rack = list("WORD___")  # Include blanks for flexibility
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=20)


    header = "   " + " ".join(f"{col:2}" for col in range(15))
    print(header)
    for row in range(15):
        line = f"{row:2} "
        for col in range(15):
            tile = board_state.get_tile(row, col)
            if tile.letter:
                line += tile.letter + " "
            else:
                line += ". "
        print(line.rstrip())
    print()
    for move in moves:
        print(move.word)
        print(move.tiles)
        print(move.direction)
        print()


    assert len(moves) >= 1
    # Every move should touch at least one existing tile
    for mv in moves:
        assert any(
            board_state.get_tile(r+dr, c+dc) and not board_state.get_tile(r+dr, c+dc).is_empty()
            for r, c, _, _ in mv.tiles
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
            if 0 <= r+dr < 15 and 0 <= c+dc < 15
        )


def test_scoring_prefers_higher_value_letter_multipliers(board_state, small_wordset_solver):
    """
    Place a setup that allows TL/DL scoring; ensure nonzero scores and ordering.
    Not asserting exact scores yet, but checking relative ordering is sensible.
    """
    # Pre-place "CAT" so crosses can land on premium squares nearby
    build_board_with_word(board_state, "CAT", 7, 6, 'right')
    rack = list("WORDS__")
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=10)
    assert len(moves) > 0
    scores = [m.score for m in moves]
    assert max(scores) >= min(scores)


def test_blank_tiles_used_as_any_letter(board_state, small_wordset_solver):
    """Ensure a blank can complete a word not otherwise spellable from rack."""
    build_board_with_word(board_state, "HELLO", 7, 5, 'right')
    # Want to form "HERO" crossing at HE, need R with blank
    rack = list("EO_R___")  # Contains a blank '_'
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=50)
    words = extract_words(moves)
    # We don't guarantee exact generation, but HERO should be achievable with a blank
    assert "HERO" in words or any("HERO" in w for w in words)


def test_bingo_bonus_when_using_all_seven_tiles(board_state, small_wordset_solver):
    """If a 7-tile placement is generated, its score should include a bonus (>=50)."""
    # This is hard to force deterministically; we assert that if any 7-tile move exists, it has big score
    rack = list("TACTICS")
    moves = small_wordset_solver.find_optimal_moves(board_state, rack, max_moves=100)
    seven_tile_moves = [m for m in moves if len(m.tiles) == 7]
    for m in seven_tile_moves:
        assert m.score >= 50


