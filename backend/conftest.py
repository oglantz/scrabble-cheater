"""
Pytest configuration and shared fixtures for backend tests.

Sets up import paths and provides helpers to quickly create boards and services.
"""

import os
import sys
from pathlib import Path
import pytest


@pytest.fixture(scope="session", autouse=True)
def add_project_to_path():
    """Ensure project root and backend are importable during tests."""
    project_root = Path(__file__).resolve().parents[1]
    backend_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(backend_dir))
    yield
    # No teardown needed


@pytest.fixture()
def board_state():
    """Provide a fresh empty `BoardState` for each test."""
    from models.board_state import BoardState
    return BoardState.create_empty()


@pytest.fixture()
def solver_service():
    """Provide a `SolverService` instance with dictionary loaded."""
    from services.solver_service import SolverService
    return SolverService()


@pytest.fixture()
def board_service():
    """Provide a `BoardService` instance for helper operations."""
    from services.board_service import BoardService
    return BoardService()


@pytest.fixture()
def small_wordset_solver(monkeypatch):
    """
    Provide a `SolverService` whose wordset is a tiny, deterministic Trie
    to make tests stable and fast.
    """
    from services.solver_service import SolverService
    from core.wordset_trie import Trie

    svc = SolverService()

    trie = Trie()
    # Core words for testing various scenarios (crosses, overlaps, blanks)
    for w in [
        "A", "I", "IN", "ON", "AT", "TO", "HE", "SHE",
        "HELLO", "HELL", "HELP", "HOPE", "HOP", "HERO",
        "WORLD", "WORD", "WORDS", "ROW", "OWL",
        "CAT", "CATS", "ACT", "TACT", "TACTIC", "TACTICS",
        "TREE", "REEF", "FREE", "FREED", "FEED",
        "DOG", "GOD", "GO", "ODO", "DO",
        "QUIZ", "JAZZ", "JAZZY", "FIZZ", "BUZZ",
        "TILE", "TILES", "BOARD", "SCORE",
    ]:
        trie.insert(w)

    svc.wordset = trie
    return svc


