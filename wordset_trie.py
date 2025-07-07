import tqdm

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def is_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def load_dictionary(file_path):
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
