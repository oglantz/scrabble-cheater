"""
Minimal Trie and loader for the legacy solver path.

Kept intentionally simple; the backend uses an enhanced version under
`backend/core/wordset_trie.py` and `backend/core/wordset_loader.py`.
"""

import tqdm

class TrieNode:
    """Node in a prefix tree mapping characters to child nodes."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """Simple Trie supporting insert, is_word, and starts_with."""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert an uppercase word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def is_word(self, word):
        """Return True if the full word exists in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Return True if any word in the trie begins with the prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def load_dictionary(file_path):
    """Load words from a text file into a Trie and return it."""
    trie = Trie()
    with open(file_path, 'r') as file:

        for line in file:
            word = line.strip().upper().split()[0]  # Convert to uppercase
            if word:  # Ensure the word is not empty
                trie.insert(word)
    return trie


if __name__ == "__main__":
    # Example usage
    trie = load_dictionary('wordset.txt')
    print(trie.is_word('HELLO'))  # Check if 'HELLO' is a valid word
    print(trie.starts_with('HE'))   # Check if any word starts with 'HE'
    print(trie.is_word('WORLD'))     # Check if 'WORLD' is a valid word
    print(trie.starts_with('WOR'))    # Check if any word starts with 'WOR'
