import random
import sys
import time

# Pictorial representation of various stages of the game
HANGMAN = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']


def get_animals_list(filename):
    """
    Gets the list of animals from the given file.

    :param filename: File containing animal names
    :return: A list of all animal names found in the file
    """

    f = open(filename, 'r')
    text = f.read()
    f.close()
    animals = text.split('\n')
    animals = [animal for animal in animals if animal != '' and len(animal) > 1]
    return sorted(animals)


def choose_word(word_list):
    """
    Chooses a random word from the given list

    :param word_list: A list of words to choose from
    :return: A word at random
    """
    word = random.choice(word_list)
    word = word.lower()
    return word


def welcome():
    """
    Welcomes the user to the game of hangman

    :return: The name of the user.
    """
    name = input("Please enter your name... ")
    print("Hello " + name + '!', "Let's play...")
    const = 'HANGMAN'
    for ch in const:
        print(ch, end = ' ')
        sys.stdout.flush()
        time.sleep(0.5)
    return name


def display(missed_letters, correct_letters, secret_word):
    """
    The items to be displayed to the player
    :param missed_letters: Missed letters to be displayed
    :param correct_letters: Correct letters to be displayed
    :param secret_word:  Secret word with guessed letteres and dashes
    :return: None
    """
    print(HANGMAN[len(missed_letters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    dashed_entry = ''

    for letter in secret_word:
        if letter == ' ':
            dashed_entry += ' '
        elif letter in correct_letters:
            dashed_entry += letter
        else:
            dashed_entry += '-'

    for letter in dashed_entry:  # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()


def get_guess(already_guessed):
    """
    Check and get the input from the user
    :param already_guessed: List of already guessed items
    :return: A valid user guess from screen
    """

    while True:
        print('Guess a letter.')
        guess = (input()).lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess == ' ':
            print('Space is not a valid entry. Please enter a single letter.')
        elif guess in already_guessed:
            print('"Already guessed the letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess


def play_again():
    """
    Does the player want to play again?
    :return: True if the player wants to play again; otherwise, it returns False.
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def start_playing(name, words):
    """

    :param name:
    :param words:
    :return:
    """
    while True:
        secret_word = choose_word(words)
        missed_letters = ''
        correct_letters = ''
        game_over = False

        while not game_over:
            display(missed_letters, correct_letters, secret_word)
            guessed_letter = get_guess(missed_letters + correct_letters)

            if guessed_letter in secret_word:
                correct_letters = correct_letters + guessed_letter
                found_all_letters = True
                for letter in secret_word:
                    if letter not in correct_letters:
                        found_all_letters = False
                        break
                if found_all_letters:
                    print('Yes! The secret word is "' + secret_word + '"! ' + name.capitalize() + ',you won!')
                    game_over = True
            else:
                missed_letters = missed_letters + guessed_letter

                # Check if player has guessed too many times and lost.
                if len(missed_letters) == len(HANGMAN) - 1:
                    display(missed_letters, correct_letters, secret_word)
                    print(name.capitalize() + ', you ran out of guesses!\n)')
                    print('After ' + str(len(missed_letters)) + ' missed guesses and ' + str(
                        len(correct_letters)) + ' correct guesses, the word was "' + secret_word.capitalize() + '"')
                    game_over = True

        if game_over:
            if not play_again():
                break

def main():

    # The required command-line argument for execution is animal_list.txt, the filename.
    if len(sys.argv) != 2:
        print('File name not entered!')
        sys.exit(1)

    words = get_animals_list(sys.argv[1])
    name = welcome()
    start_playing(name, words)


if __name__ == '__main__':
    main()
