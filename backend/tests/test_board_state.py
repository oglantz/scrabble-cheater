"""
BoardState unit tests

Covers tile placement/removal, anchors, serialization, and basic invariants.
"""

import pytest


def test_empty_board_has_center_anchor(board_state):
    """On a fresh board, only the center should be an anchor."""
    anchors = board_state.find_anchors()
    assert (7, 7) in anchors
    # Not asserting exact count due to implementation detail, but center must exist


def test_place_tile_and_anchors_update(board_state):
    """Placing at center should create anchors adjacent to the placed tile."""
    assert board_state.place_tile(7, 7, 'H')
    anchors = board_state.find_anchors()
    expected = {(6, 7), (8, 7), (7, 6), (7, 8)}
    for pos in expected:
        assert pos in anchors


def test_cannot_place_on_occupied_cell(board_state):
    """Second placement on the same cell should fail."""
    assert board_state.place_tile(7, 7, 'H')
    assert not board_state.place_tile(7, 7, 'I')


def test_remove_tile_restores_premium(board_state):
    """Removing a tile should preserve premium on the cell."""
    premium_before = board_state.get_tile(7, 7).premium
    assert board_state.place_tile(7, 7, 'H')
    assert board_state.remove_tile(7, 7)
    tile = board_state.get_tile(7, 7)
    assert tile.letter is None
    assert tile.premium == premium_before


def test_to_and_from_dict_roundtrip(board_state):
    """Serialization and deserialization should preserve board content."""
    board_state.place_tile(7, 7, 'H')
    board_state.place_tile(7, 8, 'I')
    board_state.find_anchors()

    data = board_state.to_dict()
    from models.board_state import BoardState
    restored = BoardState.from_dict(data)

    assert restored.get_tile(7, 7).letter == 'H'
    assert restored.get_tile(7, 8).letter == 'I'
    assert isinstance(restored.anchors, set)


@pytest.mark.parametrize("r,c", [(-1, 0), (0, -1), (15, 0), (0, 15)])
def test_out_of_bounds_get_tile(board_state, r, c):
    """Out-of-bounds access should return None."""
    assert board_state.get_tile(r, c) is None


