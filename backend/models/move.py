"""
Move Model
Represents a possible Scrabble move structured for API responses and services.
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class Move:
    """Represents a Scrabble move with all necessary information."""
    
    word: str  # The word to be played
    score: int  # Points scored for this move
    tiles: List[Tuple[int, int, str, bool]]  # (row, col, letter, is_blank) for each tile placed
    direction: str  # 'right' or 'down'
    start: Tuple[int, int]  # (row, col) starting position
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert move to dictionary for JSON serialization."""
        return {
            "word": self.word,
            "score": self.score,
            "tiles": self.tiles,
            "direction": self.direction,
            "start": list(self.start)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Move':
        """Create Move from dictionary."""
        return cls(
            word=data["word"],
            score=data["score"],
            tiles=data["tiles"],
            direction=data["direction"],
            start=tuple(data["start"])
        )
    
    @classmethod
    def from_legacy(cls, legacy_move: Dict[str, Any]) -> 'Move':
        """Convert from legacy solver output format."""
        return cls(
            word=legacy_move["word"],
            score=legacy_move["score"],
            tiles=legacy_move["tiles"],
            direction=legacy_move["direction"],
            start=legacy_move["start"]
        )
