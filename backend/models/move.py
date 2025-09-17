"""
Move Model
Represents a possible Scrabble move structured for API responses and services.
"""

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class TileScore:
    """Detailed scoring information for a single tile."""
    letter: str
    base_value: int
    premium_multiplier: int
    final_value: int
    premium_type: Optional[str]  # 'DL', 'TL', 'DW', 'TW', or None
    position: Tuple[int, int]
    is_blank: bool

@dataclass
class ScoreBreakdown:
    """Detailed breakdown of how a move's score was calculated."""
    tile_scores: List[TileScore]
    word_multiplier: int
    base_word_score: int
    final_word_score: int
    bingo_bonus: int
    # Additional scoring from cross words created this turn
    cross_words_total: int = 0
    cross_words: List[Dict[str, Any]] = field(default_factory=list)
    # Overall total including crosses and bingo
    total_score: int = 0

@dataclass
class Move:
    """Represents a Scrabble move with all necessary information."""
    
    word: str  # The word to be played
    score: int  # Points scored for this move
    tiles: List[Tuple[int, int, str, bool]]  # (row, col, letter, is_blank) for each tile placed
    direction: str  # 'right' or 'down'
    start: Tuple[int, int]  # (row, col) starting position
    score_breakdown: Optional[ScoreBreakdown] = None  # Detailed scoring information
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert move to dictionary for JSON serialization."""
        result = {
            "word": self.word,
            "score": self.score,
            "tiles": self.tiles,
            "direction": self.direction,
            "start": list(self.start)
        }
        
        if self.score_breakdown:
            result["score_breakdown"] = {
                "tile_scores": [
                    {
                        "letter": ts.letter,
                        "base_value": ts.base_value,
                        "premium_multiplier": ts.premium_multiplier,
                        "final_value": ts.final_value,
                        "premium_type": ts.premium_type,
                        "position": list(ts.position),
                        "is_blank": ts.is_blank
                    }
                    for ts in self.score_breakdown.tile_scores
                ],
                "word_multiplier": self.score_breakdown.word_multiplier,
                "base_word_score": self.score_breakdown.base_word_score,
                "final_word_score": self.score_breakdown.final_word_score,
                "bingo_bonus": self.score_breakdown.bingo_bonus,
                "cross_words_total": self.score_breakdown.cross_words_total,
                "cross_words": self.score_breakdown.cross_words,
                "total_score": self.score_breakdown.total_score
            }
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Move':
        """Create Move from dictionary."""
        score_breakdown = None
        if "score_breakdown" in data and data["score_breakdown"]:
            sb_data = data["score_breakdown"]
            tile_scores = [
                TileScore(
                    letter=ts["letter"],
                    base_value=ts["base_value"],
                    premium_multiplier=ts["premium_multiplier"],
                    final_value=ts["final_value"],
                    premium_type=ts["premium_type"],
                    position=tuple(ts["position"]),
                    is_blank=ts["is_blank"]
                )
                for ts in sb_data["tile_scores"]
            ]
            score_breakdown = ScoreBreakdown(
                tile_scores=tile_scores,
                word_multiplier=sb_data["word_multiplier"],
                base_word_score=sb_data["base_word_score"],
                final_word_score=sb_data["final_word_score"],
                bingo_bonus=sb_data["bingo_bonus"],
                cross_words_total=sb_data.get("cross_words_total", 0),
                cross_words=sb_data.get("cross_words", []),
                total_score=sb_data["total_score"]
            )
        
        return cls(
            word=data["word"],
            score=data["score"],
            tiles=data["tiles"],
            direction=data["direction"],
            start=tuple(data["start"]),
            score_breakdown=score_breakdown
        )
    
    @classmethod
    def from_legacy(cls, legacy_move: Dict[str, Any]) -> 'Move':
        """Convert from legacy solver output format."""
        score_breakdown = None
        if "score_breakdown" in legacy_move and legacy_move["score_breakdown"]:
            sb_data = legacy_move["score_breakdown"]
            
            # Check if it's already a ScoreBreakdown object or a dictionary
            if isinstance(sb_data, ScoreBreakdown):
                score_breakdown = sb_data
            else:
                # It's a dictionary, convert it
                tile_scores = [
                    TileScore(
                        letter=ts["letter"],
                        base_value=ts["base_value"],
                        premium_multiplier=ts["premium_multiplier"],
                        final_value=ts["final_value"],
                        premium_type=ts["premium_type"],
                        position=tuple(ts["position"]),
                        is_blank=ts["is_blank"]
                    )
                    for ts in sb_data["tile_scores"]
                ]
                score_breakdown = ScoreBreakdown(
                    tile_scores=tile_scores,
                    word_multiplier=sb_data["word_multiplier"],
                    base_word_score=sb_data["base_word_score"],
                    final_word_score=sb_data["final_word_score"],
                    bingo_bonus=sb_data["bingo_bonus"],
                    cross_words_total=sb_data.get("cross_words_total", 0),
                    cross_words=sb_data.get("cross_words", []),
                    total_score=sb_data["total_score"]
                )
        
        return cls(
            word=legacy_move["word"],
            score=legacy_move["score"],
            tiles=legacy_move["tiles"],
            direction=legacy_move["direction"],
            start=legacy_move["start"],
            score_breakdown=score_breakdown
        )
