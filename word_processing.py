from collections import Counter



class WordProcessor():

    def __init__(self, file_name:str, characters:str, wild_count:int):
        self.file_name = file_name
        self.word_list = []
        self.character_counter = Counter(characters)
        self.characters = characters
        self.valid_words_with_def = {}
        self.valid_word_with_pts = {}
        self.wild_count = wild_count
        self.character_values = {"E": 1, "A": 1,
                                 "I": 1, "O": 1,
                                 "N": 1, "R": 1, 
                                 "T": 1, "L": 1,
                                 "S": 1, "U": 1,
                                 "D": 2, "G": 2,
                                 "B": 3, "C": 3,
                                 "M": 3, "P": 3,
                                 "F": 4, "H": 4,
                                 "V": 4, "W": 4,
                                 "Y": 4, "K": 5,
                                 "J": 8, "X": 8,
                                 "Q": 10, "Z": 10}

        self._process_file()

    def _process_file(self):
        with open(self.file_name, 'r') as word_file:
            wordset = word_file.readlines()
            for i in wordset:
                x = i.split("\t")
                self.word_list.append(x)

    def _valid_word_checker(self, str1:Counter, str2:Counter):
        for char, count in str1.items():
            if str2[char] < count:
                needed = count - str2[char]
            
                # Check if we have enough wild tiles to compensate
                if self.wild_count >= needed:
                    self.wild_count -= needed  # Use the wild tiles
                else:
                    return False
        return True
    
    def calculate_pts(self):
        for word in self.valid_words_with_def.keys():
            temp_chars = list(self.characters)
            total = 0
            for char in word:
                if char in temp_chars:
                    total += self.character_values[char]
                    temp_chars.remove(char)
            self.valid_word_with_pts[word] = total

    def generate_valid_words(self):
        for word_and_def in self.word_list:
            current_word_counter = Counter(word_and_def[0])
            if(self._valid_word_checker(current_word_counter, self.character_counter)):
                self.valid_words_with_def[word_and_def[0]] = word_and_def[1]


# characters = "AHFJD**"
# x = WordProcessor("wordset.txt", characters, 1)
# x.generate_valid_words()
# x.calculate_pts()
# print(x.valid_word_with_pts)
# print(x.valid_words_with_def)

