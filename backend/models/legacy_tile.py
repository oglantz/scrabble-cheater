"""
Legacy Tile class for compatibility with existing solver code.

This mirrors a subset of the legacy `board.Tile` interface so the backend's
enhanced components can interoperate with older solver logic as needed.
"""

class LegacyTile:
    """
    Compatibility class that matches the interface of your existing Tile class.
    Allows existing solver code to work with new BoardState system.
    """
    
    def __init__(self, letter=None, premium=None, is_blank=False):
        self.letter = letter  # E.g. 'A', 'B', None
        self.premium = premium  # E.g. 'TW', 'DL', None  
        self.is_blank = is_blank  # If a blank tile was used
