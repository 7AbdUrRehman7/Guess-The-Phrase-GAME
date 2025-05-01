"""What's that Phrase? game main program."""

import random

from constants import (COST_OF_VOWEL, BONUS_POINTS, PLAYER_ONE,
                       PLAYER_TWO, GUESS, BUY, SOLVE, QUIT,
                       SINGLE_PLAYER, PVP, PVE, EASY, HARD,
                       ALL_CONSONANTS, ALL_VOWELS,
                       PRIORITY_CONSONANTS, MYSTERY_CHAR)

import game_functions as gf


################################ The Game: #################################
def play_game(mystery_phrase: str, mystery_phrases: list[str],
              game_type: str) -> None:
    """Play the game!"""

    view = make_view(mystery_phrase)
    consonants, vowels = ALL_CONSONANTS, ALL_VOWELS
    player_one_score, player_two_score = 0, 0
    current_player = PLAYER_ONE

    if game_type == PVE:
        difficulty = select_computer_difficulty()

    move = ''
    while not gf.game_over(mystery_phrase, view, move):
        score = gf.current_player_score(player_one_score,
                                        player_two_score,
                                        current_player)
        num_occurrences = 0

        display_move_prompt(current_player, score, view)

        if gf.is_player(current_player, game_type):
            (move, guess) = player_move(score, consonants, vowels)
        else:
            (move, guess) = computer_move(view, mystery_phrases, difficulty,
                                          consonants)

        if move == QUIT:
            print('You chose to quit the game!')
            winner = 'No winner'

        elif move == SOLVE:
            if guess == mystery_phrase:
                score = compute_score(mystery_phrase, view, score)
                view = mystery_phrase
                winner = current_player
            else:
                print(f"The solution '{guess}' is incorrect. Keep playing!")

        else:  # guess vowel or consonant
            view = update_view(mystery_phrase, view, guess)
            num_occurrences = mystery_phrase.count(guess)
            score = gf.compute_score(score, num_occurrences, move)

            consonants = gf.delete(consonants, consonants.find(guess))
            vowels = gf.delete(vowels, vowels.find(guess))

            winner = current_player

            print(f'{current_player} guesses {guess}, which occurs '
                  f'{num_occurrences} time(s) in the mystery phrase.')
            print(f"{current_player}'s score is now {score}.")

        if current_player == PLAYER_ONE:
            player_one_score = score
        else:
            player_two_score = score
        current_player = gf.next_turn(
            current_player, num_occurrences, game_type)

    # The game is over.
    display_outcome(winner, mystery_phrase, game_type, player_one_score,
                    player_two_score)


def update_view(mystery_phrase: str, view: str, guess: str) -> str:
    """Return a new view of mystery_phrase: a view in which each
    occurrence of guess in mystery_phrase is revealed.

    view is a valid game view for mystery_phrase
    guess is one character long

    >>> update_view('apple', '^^^le', 'a')
    'a^^le'
    >>> update_view('apple', '^^^le', 'p')
    '^pple'
    >>> update_view('apple', '^^^le', 'z')
    '^^^le'

    """

    new_view = ''
    for index in range(len(mystery_phrase)):
        new_view += gf.update_view(mystery_phrase, view, index, guess)
    return new_view


def compute_score(mystery_phrase: str, view: str, current_score: int) -> int:
    """Return the final score, calculated by adding constants.BONUS_POINTS
    points to current_score for each occurrence of a consonant in
    mystery_phrase that appears as consonants.MYSTERY_CHAR in view.

    view is a valid game view for mystery_phrase
    current_score is non-negative

    >>> compute_score('apple pies', '^pple p^es', 0)
    0
    >>> compute_score('apple pies', '^^^le ^^e^', 0)
    8

    """

    final_score = current_score
    for letter in ALL_CONSONANTS:
        if gf.adds_points(letter, mystery_phrase, view):
            final_score += BONUS_POINTS * mystery_phrase.count(letter)
    return final_score


########################## Game Play: Computer Moves #######################
def computer_move(view: str, mystery_phrases: list[str], difficulty: str,
                  consonants: str) -> (str, str):
    """Return the computer's next move:
    (constants.SOLVE, solution-guess) or (constants.GUESS, letter-guess)

    If difficulty is constants.HARD, the computer chooses to solve if
    at least half of the letters in view are revealed (not
    constants.MYSTERY_CHAR). Otherwise, the computer opts to guess a
    consonant.

    """

    if gf.environment_solves(view, difficulty, consonants):
        move = SOLVE
        guess = get_match(view, mystery_phrases)
        print(f'\tI choose to solve: {guess}.')
    else:
        move = GUESS
        guess = environment_guess_letter(consonants, difficulty)
        print(f'\tI choose to guess letter: {guess}.')
    return move, guess


def get_match(view: str, mystery_phrases: list[str]) -> str:
    """Return a mystery_phrase from mystery_phrases that could be
    represented by view. If no such mystery_phrase exists, return the
    empty string.

    >>> get_match('^^^ ro^k^', ['abc', 'csc rocks', 'math is cool'])
    'csc rocks'
    >>> get_match('^^^ ro^ks', ['abc', 'csc rocks', 'math is cool'])
    ''

    """

    for mystery_phrase in mystery_phrases:
        if is_match(mystery_phrase, view):
            return mystery_phrase
    return ''


def is_match(mystery_phrase: str, view: str) -> bool:
    """Return True if and only if view is a valid mystery phrase view of
    mystery_phrase.

    >>> is_match('', '')
    True
    >>> is_match('a', 'a')
    True
    >>> is_match('bb', 'b^')
    False
    >>> is_match('abcde', 'ab^^e')
    True
    >>> is_match('axyzb', 'ab^^e')
    False
    >>> is_match('abcdefg', 'ab^^e')
    False

    """

    if len(mystery_phrase) != len(view):
        return False

    for index in range(len(mystery_phrase)):
        if (mystery_phrase[index] != view[index] and
            not gf.is_mystery_char(index, mystery_phrase, view)):
            return False
    return True


def environment_guess_letter(consonants: str, difficulty: str) -> str:
    """Return a letter from consonants. If difficulty is constants.EASY,
    select the letter randomly. If difficulty is constants.HARD,
    select the first letter from constants.PRIORITY_CONSONANTS that
    occurs in consonants.

    len(consonants) > 0;
    at least one character in consonants is in consonants.PRIORITY_CONSONANTS.
    difficulty in (constants.EASY, constants.HARD)

    >>> environment_guess_letter('bcdfg', 'H')
    'd'

    """

    if difficulty == HARD:
        for consonant in PRIORITY_CONSONANTS:
            if consonant in consonants:
                return consonant
    return random.choice(consonants)


########################## Game Play: User Interaction: ####################
def player_move(player_score: int, consonants: str, vowels: str) -> tuple:
    """Ask the user to make a complete move:

    1) Repeatedly ask to choose a move (constants.GUESS,
    constants.BUY, constants.SOLVE, or constants.QUIT), until a valid
    input is entered.

    2) Upon receiving constants.BUY or constants.GUESS, repeatedly
    prompt to choose a corresponding letter, until a valid input is
    entered.

    3) Upon receiving constants.SOLVE, prompt for a solution word.

    Return the user input guess, or the empty string is the first
    choice was constants.QUIT.

    """

    move = select_move(player_score, consonants, vowels)

    if move == QUIT:
        guess = ''
    if move == BUY:
        guess = select_letter(vowels)
    if move == GUESS:
        guess = select_letter(consonants)
    if move == SOLVE:
        guess = input('Input your solution guess: ')

    return (move, guess)


def select_move(score: int, consonants: str, vowels: str) -> str:
    """Repeatedly prompt current_player to choose a move until a valid
    selection is made. Return the selected move. Move validity is
    defined by is_valid_move(selected-move-type, score, consonants,
    vowels).

    (Note: Docstring examples not given since result depends on input
    data.)

    """

    prompt = make_move_prompt()

    move = input(prompt)
    while not is_valid_move(move.strip(), score, consonants, vowels):
        move = input(prompt)

    return move.strip()


def select_letter(letters: str) -> str:
    """Repeatedly prompt the user for a letter, until a valid input is
    received. Return the letter. Valid options are characters from
    letters.

    (Note: Docstring examples not given since result depends on input
    data.)

    """

    prompt = f"Choose a letter from [{','.join(['{}'] * len(letters))}]: "
    valid_options = tuple(letters)
    return prompt_for_selection(prompt, valid_options)


def prompt_for_selection(prompt_format: str, valid_options: tuple) -> str:
    """Repeatedly ask the user for a selection, until one of valid_options
    is received. The user prompt is created as
    prompt_format.format(valid_option). Return the user input with
    leading and trailing whitespace removed.

    (Note: Docstring examples not given since result depends on input
    data.)

    """

    prompt = prompt_format.format(*valid_options)

    selection = input(prompt)
    while selection.strip() not in valid_options:
        selection = input(f'Invalid choice.\n{prompt}')

    return selection.strip()


def display_move_prompt(current_player: str, player_score: int,
                        view: str) -> None:
    """Display a prompt for the player to select the next move."""

    print('=' * 50)
    print(f'{current_player}, it is your turn. You have {player_score} points.')
    print(f'\n{view}\n')


def make_move_prompt() -> str:
    """Return a prompt for the player to select the next move."""

    prompt = f'''Select move type:
    [{BUY}] - Buy a vowel,
    [{GUESS}] - Guess a consonant,
    [{SOLVE}] - Solve the phrase,
    [{QUIT}] - Quit.\n'''

    return prompt


def is_valid_move(move: str, score: int, consonants: str, vowels: str) -> bool:
    """Return whether move is valid. If invalid, print an explanatory
    message. A move is valid when:

    1) move is one of constants.GUESS, constants.BUY, constants.SOLVE,
    or constants.QUIT;

    2) If move is constants.BUY, score is high enough to buy a
    vowel(at least constants.COST_OF_VOWEL), and vowels has at least
    one character.

    3) If move is constants.GUESS, consonants has at least one
    character.

    >>> is_valid_move('X', 0, '', '')
    Valid moves are: G, B, S, and Q.
    False
    >>> is_valid_move('Q', 0, '', '')
    True
    >>> is_valid_move('S', 42, 'bdfrt', 'aeui')
    True
    >>> is_valid_move('G', 2, 'bcdfghjklmnpqstvwxyz', 'aeiou')
    True
    >>> is_valid_move('G', 2, '', 'aeiou')
    You do not have any more consonants to guess!
    False
    >>> is_valid_move('B', 1, 'bcdfghjklmnpqstvwxyz', 'aeiou')
    True
    >>> is_valid_move('B', 0, 'bcdfghjklmnpqstvwxyz', 'aeiou')
    You do not have enough points to reveal a vowel. Vowels cost 1 point(s).
    False
    >>> is_valid_move('B', 42, 'bcdfghjklmnpqstvwxyz', '')
    You do not have any more vowels to guess!
    False

    """

    if move not in (GUESS, BUY, SOLVE, QUIT):
        print(f'Valid moves are: {GUESS}, {BUY}, {SOLVE}, and {QUIT}.')
        return False

    if move == BUY and score < COST_OF_VOWEL:
        print('You do not have enough points to reveal a vowel. '
              f'Vowels cost {COST_OF_VOWEL} point(s).')
        return False

    if move == BUY and vowels == '':
        print('You do not have any more vowels to guess!')
        return False

    if move == GUESS and consonants == '':
        print('You do not have any more consonants to guess!')
        return False

    return True


############################# Game Setup: #############################
def select_game_type() -> str:
    """Repeatedly prompt the user for game type, until a valid input is
    received. Return the game type. Valid options are
    constants.SINGLE_PLAYER, constants.PVP, and constants.PVE.

    (Note: Docstring examples not given since result depends on input
    data.)

    """

    prompt = '''Choose the game type:
     [{}] - Single-player
     [{}] - PVP (player vs player)
     [{}] - PVE (player vs environment)\n'''
    valid_options = SINGLE_PLAYER, PVP, PVE
    return prompt_for_selection(prompt, valid_options)


def select_computer_difficulty() -> str:
    """Repeatedly prompt the user for computer difficulty, until a valid
    input is received. Return the computer difficulty. Valid options
    are constants.EASY and constants.HARD.

    (Note: Docstring examples not given since result depends on input
    data.)

    """

    prompt = 'Choose the game difficulty ([{}] - Easy or [{}] - Hard): '
    valid_options = EASY, HARD
    return prompt_for_selection(prompt, valid_options)


def make_view(mystery_phrase: str) -> str:
    """Return a string that is based on mystery_phrase, with each
    alphabetic character replaced by the constants.MYSTERY_CHAR
    character.

    >>> make_view('apple cake is great! #csca08')
    '^^^^^ ^^^^ ^^ ^^^^^! #^^^^08'
    >>> make_view('a08@#$&')
    '^08@#$&'

    """

    view = ''
    for char in mystery_phrase:
        if char.isalpha():
            view = view + MYSTERY_CHAR
        else:
            view = view + char
    return view


############################# Game Over: #############################
def display_outcome(winner: str, mystery_phrase: str, game_type: str,
                    player_one_score: int, player_two_score: int) -> None:
    """Display the outcome of game: who won and what the final scores are.
    """

    print(f'And the winner is... {winner}!')
    print(f'The solution to this game\'s mystery phrase is: {mystery_phrase}.')
    if gf.one_player(game_type):
        print(f'In this game, the player scored {player_one_score} point(s)')
    else:
        print(f'In this game, {PLAYER_ONE} scored {player_one_score} '
              f'and {PLAYER_TWO} scored {player_two_score} point(s)')


############################# The Program: #############################
if __name__ == '__main__':

    import doctest
    doctest.testmod()

    DATA_FILE = 'mystery_phrases_small.txt'

    MYSTERY_PHRASES = []
    with open(DATA_FILE, encoding='utf-8') as data_file:
        for line in data_file:
            MYSTERY_PHRASES.append(line.lower().strip())

    MYSTERY_PHRASE = random.choice(MYSTERY_PHRASES)

    print("Welcome to What's that Phrase!")

    print(f'***{MYSTERY_PHRASE}***')

    GAME_TYPE = select_game_type()
    play_game(MYSTERY_PHRASE, MYSTERY_PHRASES, GAME_TYPE)
