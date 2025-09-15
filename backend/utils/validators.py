"""
Validation Utilities
Input validation helpers for API endpoints and services.
"""

import re
from typing import List, Optional
from models.board_state import BoardState

def validate_tiles(tiles: List[str]) -> Optional[str]:
    """
    Validate user tiles input.
    
    Args:
        tiles: List of tile letters (A-Z, _ for blanks)
        
    Returns:
        None if valid, error message if invalid
    """
    if not tiles:
        return "Tiles list cannot be empty"
    
    if len(tiles) > 7:
        return "Cannot have more than 7 tiles"
    
    valid_pattern = re.compile(r'^[A-Z_]$')
    
    for i, tile in enumerate(tiles):
        if not isinstance(tile, str):
            return f"Tile {i+1} must be a string"
        
        if len(tile) != 1:
            return f"Tile {i+1} must be a single character"
        
        tile_upper = tile.upper()
        if not valid_pattern.match(tile_upper):
            return f"Tile {i+1} must be A-Z or _ (blank): got '{tile}'"
        
        # Update the tile to be uppercase
        tiles[i] = tile_upper
    
    return None

def validate_board_state(board_state: BoardState) -> Optional[str]:
    """
    Validate board state.
    
    Args:
        board_state: BoardState object to validate
        
    Returns:
        None if valid, error message if invalid
    """
    if not board_state:
        return "Board state cannot be None"
    
    try:
        # Check board dimensions
        if len(board_state.board) != BoardState.BOARD_SIZE:
            return f"Invalid board height: expected {BoardState.BOARD_SIZE}, got {len(board_state.board)}"
        
        for i, row in enumerate(board_state.board):
            if len(row) != BoardState.BOARD_SIZE:
                return f"Invalid board width at row {i}: expected {BoardState.BOARD_SIZE}, got {len(row)}"
        
        # Validate each tile
        letter_pattern = re.compile(r'^[A-Z]$')
        premium_pattern = re.compile(r'^(TW|DW|TL|DL)$')
        
        for r in range(BoardState.BOARD_SIZE):
            for c in range(BoardState.BOARD_SIZE):
                tile = board_state.board[r][c]
                
                # Validate letter
                if tile.letter is not None:
                    if not isinstance(tile.letter, str):
                        return f"Invalid letter type at ({r}, {c}): must be string"
                    
                    if not letter_pattern.match(tile.letter):
                        return f"Invalid letter at ({r}, {c}): '{tile.letter}' (must be A-Z)"
                
                # Validate premium
                if tile.premium is not None:
                    if not isinstance(tile.premium, str):
                        return f"Invalid premium type at ({r}, {c}): must be string"
                    
                    if not premium_pattern.match(tile.premium):
                        return f"Invalid premium at ({r}, {c}): '{tile.premium}' (must be TW, DW, TL, or DL)"
                
                # Validate is_blank
                if not isinstance(tile.is_blank, bool):
                    return f"Invalid is_blank type at ({r}, {c}): must be boolean"
        
        return None
        
    except Exception as e:
        return f"Error validating board state: {str(e)}"

def validate_image_file(filename: str, max_size_mb: int = 10) -> Optional[str]:
    """
    Validate uploaded image file.
    
    Args:
        filename: Name of uploaded file
        max_size_mb: Maximum file size in MB
        
    Returns:
        None if valid, error message if invalid
    """
    if not filename:
        return "Filename cannot be empty"
    
    # Check file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    filename_lower = filename.lower()
    
    if not any(filename_lower.endswith(ext) for ext in allowed_extensions):
        return f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    # Note: File size validation would be done at the Flask level
    # using request.content_length or similar
    
    return None

def sanitize_input(text: str, max_length: int = 100) -> str:
    """
    Sanitize text input.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove non-printable characters
    sanitized = ''.join(char for char in text if char.isprintable())
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()
