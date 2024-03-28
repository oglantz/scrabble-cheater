from collections import Counter



class WordProcessor():

    def __init__(self, file_name, characters):
        self.file_name = file_name
        self.word_list = []
        self.character_counter = Counter(characters)
        self.characters = characters
        self.valid_words = []

        self._process_file()

    def _process_file(self):
        with open(self.file_name, 'r') as word_file:
            wordset = word_file.readlines()
            for i in wordset:
                x = i.split("\t")
                self.word_list.append(x)
    
    def generate_valid_words(self):
        for word_and_def in self.word_list:
            current_word_counter = Counter(word_and_def[0])
            if(self._valid_word_checker(current_word_counter, self.character_counter)):
                self.valid_words.append(word_and_def)

    def _valid_word_checker(self, str1:Counter, str2:Counter):
        for char, count in str1.items():
            if str2[char] < count:
                return False
        return True


characters = "AALSEFR"
x = WordProcessor("wordset.txt", characters)
x.generate_valid_words()
print(x.valid_words)

