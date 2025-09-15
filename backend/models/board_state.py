"""
Board State Model
Represents the current state of a Scrabble board.
Designed to be easily populated from either manual input or photo processing.
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import copy

@dataclass
class BoardTile:
    """Represents a single tile on the board."""
    letter: Optional[str] = None  # None for empty, A-Z for letters
    is_blank: bool = False  # True if this was placed as a blank tile
    premium: Optional[str] = None  # TW, DW, TL, DL, or None
    is_placed_this_turn: bool = False  # Track newly placed tiles
    
    def is_empty(self) -> bool:
        return self.letter is None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "letter": self.letter,
            "is_blank": self.is_blank,
            "premium": self.premium,
            "is_placed_this_turn": self.is_placed_this_turn
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoardTile':
        return cls(
            letter=data.get('letter'),
            is_blank=data.get('is_blank', False),
            premium=data.get('premium'),
            is_placed_this_turn=data.get('is_placed_this_turn', False)
        )


class BoardState:
    """Represents the complete state of a Scrabble board."""
    
    BOARD_SIZE = 15
    
    # Premium square mappings (same as your original)
    PREMIUM_MAP = {
        # Triple Word (TW) - dark red
        (0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW',
        (7, 0): 'TW', (7, 14): 'TW',
        (14, 0): 'TW', (14, 7): 'TW', (14, 14): 'TW',

        # Double Word (DW) - light red  
        (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW',
        (10, 10): 'DW', (11, 11): 'DW', (12, 12): 'DW', (13, 13): 'DW',
        (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW',
        (10, 4): 'DW', (11, 3): 'DW', (12, 2): 'DW', (13, 1): 'DW',
        (7, 7): 'DW',  # Center star tile

        # Triple Letter (TL) - dark blue
        (1, 5): 'TL', (1, 9): 'TL',
        (5, 1): 'TL', (5, 5): 'TL', (5, 9): 'TL', (5, 13): 'TL',
        (9, 1): 'TL', (9, 5): 'TL', (9, 9): 'TL', (9, 13): 'TL',
        (13, 5): 'TL', (13, 9): 'TL',

        # Double Letter (DL) - light blue
        (0, 3): 'DL', (0, 11): 'DL',
        (2, 6): 'DL', (2, 8): 'DL',
        (3, 0): 'DL', (3, 7): 'DL', (3, 14): 'DL',
        (6, 2): 'DL', (6, 6): 'DL', (6, 8): 'DL', (6, 12): 'DL',
        (7, 3): 'DL', (7, 11): 'DL',
        (8, 2): 'DL', (8, 6): 'DL', (8, 8): 'DL', (8, 12): 'DL',
        (11, 0): 'DL', (11, 7): 'DL', (11, 14): 'DL',
        (12, 6): 'DL', (12, 8): 'DL',
        (14, 3): 'DL', (14, 11): 'DL',
    }
    
    def __init__(self):
        self.board: List[List[BoardTile]] = []
        self.anchors: set = set()
        self._initialize_board()
    
    def _initialize_board(self):
        """Initialize empty board with premium squares."""
        self.board = [[BoardTile() for _ in range(self.BOARD_SIZE)] 
                     for _ in range(self.BOARD_SIZE)]
        
        # Set premium squares
        for (row, col), premium in self.PREMIUM_MAP.items():
            self.board[row][col].premium = premium
    
    def place_tile(self, row: int, col: int, letter: str, is_blank: bool = False, 
                   is_placed_this_turn: bool = True) -> bool:
        """Place a tile on the board."""
        if not self._is_valid_position(row, col):
            return False
        
        if not self.board[row][col].is_empty():
            return False  # Position already occupied
        
        self.board[row][col].letter = letter.upper()
        self.board[row][col].is_blank = is_blank
        self.board[row][col].is_placed_this_turn = is_placed_this_turn
        return True
    
    def remove_tile(self, row: int, col: int) -> bool:
        """Remove a tile from the board."""
        if not self._is_valid_position(row, col):
            return False
        
        premium = self.board[row][col].premium  # Preserve premium
        self.board[row][col] = BoardTile(premium=premium)
        return True
    
    def get_tile(self, row: int, col: int) -> Optional[BoardTile]:
        """Get tile at position."""
        if not self._is_valid_position(row, col):
            return None
        return self.board[row][col]
    
    def is_empty(self) -> bool:
        """Check if board is completely empty."""
        for row in self.board:
            for tile in row:
                if not tile.is_empty():
                    return False
        return True
    
    def find_anchors(self) -> set:
        """Find anchor positions (empty squares adjacent to placed tiles)."""
        self.anchors = set()
        
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if not self.board[r][c].is_empty():
                    # Check adjacent squares
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if (self._is_valid_position(nr, nc) and 
                            self.board[nr][nc].is_empty()):
                            self.anchors.add((nr, nc))
        
        # Special case: empty board, center is anchor
        if self.is_empty():
            self.anchors.add((7, 7))  # Center of board
        
        return self.anchors
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "board": [[tile.to_dict() for tile in row] for row in self.board],
            "anchors": list(self.anchors),
            "size": self.BOARD_SIZE
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoardState':
        """Create BoardState from dictionary."""
        board_state = cls()
        
        if "board" in data:
            board_data = data["board"]
            for r in range(min(len(board_data), cls.BOARD_SIZE)):
                for c in range(min(len(board_data[r]), cls.BOARD_SIZE)):
                    tile_data = board_data[r][c]
                    board_state.board[r][c] = BoardTile.from_dict(tile_data)
        
        if "anchors" in data:
            board_state.anchors = set(tuple(anchor) for anchor in data["anchors"])
        else:
            board_state.find_anchors()
        
        return board_state
    
    @classmethod
    def create_empty(cls) -> 'BoardState':
        """Create an empty board."""
        return cls()
    
    @classmethod
    def create_test_board(cls) -> 'BoardState':
        """Create a board with some test tiles for development."""
        board = cls()
        # Place "HELLO" horizontally starting at center
        test_word = "HELLO"
        start_row, start_col = 7, 6
        
        for i, letter in enumerate(test_word):
            board.place_tile(start_row, start_col + i, letter, is_placed_this_turn=False)
        
        board.find_anchors()
        return board
    
    def get_legacy_board(self) -> List[List]:
        """
        Convert to legacy board format for compatibility with existing solver code.
        Returns List[List[Tile]] where Tile has letter, premium, is_blank attributes.
        """
        # Import here to avoid circular imports
        from .legacy_tile import LegacyTile
        
        legacy_board = []
        for row in self.board:
            legacy_row = []
            for tile in row:
                legacy_tile = LegacyTile(
                    letter=tile.letter,
                    premium=tile.premium,
                    is_blank=tile.is_blank
                )
                legacy_row.append(legacy_tile)
            legacy_board.append(legacy_row)
        
        return legacy_board
    
    def print_board(self):
        """Print board state for debugging."""
        print("\nCurrent Board State:")
        for r in range(self.BOARD_SIZE):
            row_str = ""
            for c in range(self.BOARD_SIZE):
                tile = self.board[r][c]
                if tile.letter:
                    row_str += f" {tile.letter} "
                elif tile.premium:
                    row_str += f"{tile.premium}"
                else:
                    row_str += " - "
            print(row_str)
        print(f"Anchors: {self.anchors}")
        print()
