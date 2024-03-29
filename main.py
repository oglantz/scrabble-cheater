from word_processing import WordProcessor



def main():
    inputted_chars = input(
        "Please enter your scrabble letters, plus one from the board (use * for blank tiles)")
    inputted_chars.strip()
    wild_count = inputted_chars.count("*")

    characters = inputted_chars.replace("*", "")
    print(characters)
    wp = WordProcessor("wordset.txt", inputted_chars, wild_count)
    wp.generate_valid_words()
    print(wp.valid_words)

if __name__ == "__main__":
    main()