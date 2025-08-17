"""
Wordset Trie Implementation
Copied and enhanced from your existing wordset_trie.py
"""

import logging

logger = logging.getLogger(__name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def is_word(self, word):
        """Check if a word exists in the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Check if any word starts with the given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def get_words_with_prefix(self, prefix):
        """Get all words that start with the given prefix"""
        words = []
        node = self.root
        
        # Navigate to the prefix
        for char in prefix:
            if char not in node.children:
                return words
            node = node.children[char]
        
        # Collect all words from this point
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node, current_word, words):
        """Helper method to collect words from a node"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, words)
    
    def size(self):
        """Get the number of words in the trie"""
        return self._count_words(self.root)
    
    def _count_words(self, node):
        """Helper method to count words in the trie"""
        count = 1 if node.is_end_of_word else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count
