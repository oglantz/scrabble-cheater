
class WordProcessor():

    def __init__(self, file_name):
        self.file_name = file_name
        self.word_list = []
        self._process_file()

    def _process_file(self):
        with open(self.file_name, 'r') as word_file:
            wordset = word_file.readlines()
            for i in wordset:
                x = i.split("\t")
                self.word_list.append(x)
    
    

x = WordProcessor("wordset.txt")

