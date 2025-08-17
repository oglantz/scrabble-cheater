"""
Wordset Loader
Loads dictionary into Trie structure for word validation
Enhanced version of your existing wordset_trie.py
"""

import logging
from pathlib import Path
from core.wordset_trie import Trie

logger = logging.getLogger(__name__)

def load_dictionary(file_path: str) -> Trie:
    """
    Load dictionary from file into Trie structure
    Enhanced version with better error handling and path resolution
    """
    trie = Trie()
    
    # Try multiple possible paths for the wordset file
    possible_paths = [
        file_path,  # Direct path
        Path(file_path),  # Current directory
        Path(__file__).parent.parent / file_path,  # Backend directory
        Path(__file__).parent.parent.parent / file_path,  # Project root
        Path("wordset.txt"),  # Default name in current dir
        Path("backend") / "wordset.txt",  # Backend subdirectory
    ]
    
    wordset_file = None
    for path in possible_paths:
        if Path(path).exists():
            wordset_file = Path(path)
            break
    
    if not wordset_file:
        logger.error(f"Could not find wordset file. Searched: {[str(p) for p in possible_paths]}")
        raise FileNotFoundError(f"Wordset file not found: {file_path}")
    
    try:
        word_count = 0
        with open(wordset_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    # Handle different line formats
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Extract word (first word on line, in case of score format)
                    word = line.split()[0].upper()
                    
                    # Validate word (only letters)
                    if word and all(c.isalpha() for c in word):
                        trie.insert(word)
                        word_count += 1
                    
                except Exception as e:
                    logger.warning(f"Error processing line {line_num}: {e}")
                    continue
        
        logger.info(f"Loaded {word_count} words from {wordset_file}")
        return trie
        
    except Exception as e:
        logger.error(f"Error loading dictionary from {wordset_file}: {e}")
        raise
