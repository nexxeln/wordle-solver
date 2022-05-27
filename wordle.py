import random
import sys
from time import sleep
from rich import print
from rich.prompt import Prompt


def play():

    print("""[slate_blue1]

  _      ______  ___  ___  __   ____  
 | | /| / / __ \/ _ \/ _ \/ /  / __/  
 | |/ |/ / /_/ / , _/ // / /__/ _/    
 |__/|__/\____/_/|_/____/____/___/    
  / __/ __ \/ /| | / / __/ _ \        
 _\ \/ /_/ / /_| |/ / _// , _/        
/___/\____/____/___/___/_/|_|        

    [/slate_blue1]
    """)

    sleep(2)

    guess_results = ""
    answer_words, all_words = load_words()
    number_of_guesses = 0
    ignore_chars = ""

    while len(answer_words) > 0:
        if len(answer_words) > 1:
            print(f"[deep_sky_blue3]{len(answer_words)}[/deep_sky_blue3] [white]words remaining[/white]")
        else:
            print(f"[deep_sky_blue3]{len(answer_words)}[/deep_sky_blue3] [white]word remaining[/white]")

        current_guess = pick_word(all_words, answer_words, ignore_chars)

        print(f"[white]Current guess:[white] [deep_sky_blue3]{current_guess}[/deep_sky_blue3]")

        guess_results = Prompt.ask("[plum4]Guess result: [/plum4]")

        number_of_guesses += 1

        if len(guess_results) > 5:
            print("[red]Invalid guess result (guess result can't be longer than 5 characters)[/red]")
            number_of_guesses -= 1
            continue 
        elif len(guess_results) < 5:
            print("[red]Invalid guess result (guess result can't be shorter than 5 characters)[/red]")
            number_of_guesses -= 1
            continue 
            
        for i in range(len(guess_results)):
            if guess_results[i] not in ["g", "y", "x"]:
                print("[red]Invalid guess result (guess result can only contain g, y, or x)[/red]")
                sys.exit()

        if guess_results == "ggggg":
            break

        answer_words, ignore_chars = filter_words(answer_words, current_guess, guess_results, ignore_chars)

    if guess_results == "ggggg":
        pass
    else:
        print("[red]Could not guess word[/red]")
        sys.exit()

    return number_of_guesses

def load_words():
    answer_words = []
    all_words = []

    # load all answer words
    with open("answers.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                answer_words.append(word)

    # load all accepted words
    with open("accepted_words.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                all_words.append(word)

    return answer_words, all_words

def filter_words(words, guess_word, guess_result, ignore_chars):
    """
    filter remaining words based on last guess and guess results also ignoreany new letters that are part of the solution
    """
    new_ignore_chars = ignore_chars
    for i in range(len(guess_result)):
        if guess_result[i] != "x":
            if guess_word[i] in ignore_chars:
                ignore_chars = ignore_chars.replace(guess_word[i], "", 1)
            else:
                new_ignore_chars += guess_word[i]

    return [word for word in words if match_guess_result(word, guess_word, guess_result)], new_ignore_chars

def pick_word(all_words, answer_words, ignore_chars):
    letter_frequency = {}
    placement_frequency = [{}]*6

    if len(answer_words) <= 2:
        return answer_words[0]

    # count letter frequency, ignore letters that have already been guessed
    for word in answer_words:
        ignore_chars_copy = ignore_chars
        placement_index = 0
        for letter in word:
            if letter in ignore_chars_copy:
                ignore_chars_copy = ignore_chars_copy.replace(letter,"",1)
            else:
                if letter not in letter_frequency:
                    letter_frequency[letter] = 0

                letter_frequency[letter] += 1

            if letter not in placement_frequency[placement_index]:
                placement_frequency[placement_index][letter] = 0
            placement_frequency[placement_index][letter] += 1

            placement_index += 1

    best_word = answer_words[0]
    max_frequency = 0
    max_placement_score = 0

    # find best word based on letter frequency, ignore letters that have already been guessed
    for word in all_words:
        current_frequency = 0
        picked = set()
        ignore_chars_copy = ignore_chars
        for letter in word:
            if letter in ignore_chars_copy:
                ignore_chars_copy = ignore_chars_copy.replace(letter,"",1)
            else:
                if letter in picked:
                    continue
                picked.add(letter)
                if letter in letter_frequency:
                    current_frequency += letter_frequency[letter]

        if current_frequency > max_frequency:
            max_frequency = current_frequency
            best_word = word

            placement_score = 0
            for i in range(len(word)):
                if word[i] in placement_frequency[i]:
                    placement_score += placement_frequency[i][word[i]]
            max_placement_score = max_placement_score

        elif current_frequency == max_frequency:
            placement_score = 0
            for i in range(len(word)):
                if word[i] in placement_frequency[i]:
                    placement_score += placement_frequency[i][word[i]]

            if placement_score > max_placement_score:
                max_placement_score = placement_score
                best_word = word

    return best_word


def match_guess_result(word, guess_word, guess_result):
    """
    return True if word fits the same pattern as the guess & guess results
    SAMPLE INPUT:
        word: ABYSS
        guess_word: GUESS
        guess_result: xxxgg
        returns True
    """
    for i in range(len(guess_result)):
        if guess_result[i] == "g" and word[i] != guess_word[i]:
            return False
        elif guess_result[i] == "y":
            if guess_word[i] == word[i]:
                return False
            elif guess_word[i] not in word:
                return False
        elif guess_result[i] == "x":
            if word[i] == guess_word[i]:
                return False

            wrong_letter_instances_guess = find_letter_indexes_in_word(guess_word, guess_word[i])
            okCount = 0
            for j in wrong_letter_instances_guess:
                if guess_result[j] != "x":
                    okCount += 1
            wrong_letter_instances_word = find_letter_indexes_in_word(word, guess_word[i])
            if len(wrong_letter_instances_word) > okCount:
                return False

    return True

def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

# return guess results for a given word
def evaluate_guess_results(correct_word, guess):
    result = ""

    for i in range(len(correct_word)):
        if correct_word[i] == guess[i]:
            result += "g"
        else:
            if guess[i] in correct_word:
                result += "y"
            else:
                result += "x"

    return result

if __name__ == "__main__":
    total_guesses = 0
    max_guess_count = 0
    random.seed(1)

    current_guess_count = play()
    total_guesses += current_guess_count
    if current_guess_count > max_guess_count:
        max_guess_count = current_guess_count

    print(f"\n[green3]Solved in[/green3] [deep_sky_blue3]{total_guesses}[deep_sky_blue3] [green3]guesses[/green3]")
