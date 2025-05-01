"""CSCA08: Fall 2022 -- Assignment 1: What's that Phrase?

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020-2022 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.

"""

from constants import (POINTS_PER_GUESS, COST_OF_VOWEL, BONUS_POINTS,
                       PLAYER_ONE, PLAYER_TWO, GUESS, BUY, SOLVE,
                       QUIT, SINGLE_PLAYER, PVP, PVE, EASY, HARD,
                       ALL_CONSONANTS, ALL_VOWELS,
                       PRIORITY_CONSONANTS, MYSTERY_CHAR)


# This function is provided as an example.
def winning(mystery_phrase: str, view: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination. That is, if and only if mystery_phrase and view are
    the same.

    >>> winning('banana', 'banana')
    True
    >>> winning('apple', 'a^^le')
    False
    >>> winning('apple', 'app')
    False

    """
    return mystery_phrase == view


# This function is partially provided as an example of calling another
# function as helper.
def game_over(mystery_phrase: str, view: str, move: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination or move is QUIT.

    >>> game_over('apple', 'apple', 'S')
    True
    >>> game_over('dog', '^^^', 'Q')
    True
    >>> game_over('build', 'b^^ld', 'B')
    False
    """
    return move == QUIT or winning(mystery_phrase, view)


def one_player(player_type: str) -> bool:
    """Return True if and only if the player_type is the single player game.

    >>> one_player('SP')
    True
    >>> one_player('PVP')
    False
    >>> one_player('PVE')
    False
    """
    return player_type == 'SP'


# This function is partially provided as an example of using constants
# in the docstring description and specific values in docstring
# examples.
def is_player(current_player: str, game_type: str) -> bool:
    """Return True if and only if the current_player represents a human player
    in a game of type game_type

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is SINGLE_PLAYER, PVP, or PVE.

    In a SINGLE_PLAYER game or a PVP game, a player is always a human
    player. In a PVE game, PLAYER_ONE is a human player and PLAYER_TWO
    is the environment.

    >>> is_player('Player One', 'SP')
    True
    >>> is_player('Player Two', 'PVE')
    False

    """
    return (current_player == PLAYER_ONE or game_type == SINGLE_PLAYER
            or game_type == PVP)


def current_player_score(player1_score: int, player2_score: int,
                         current_player: str) -> int:
    """Return the player1_score score if player one is taking the
    current_player turn, but if player two is taking the current_player turn,
    then return the player2_score score.

    >>> current_player_score(2, 6, 'Player One')
    2
    >>> current_player_score(3, 1, 'Player Two')
    1
    """
    if current_player == PLAYER_ONE:
        return player1_score
    return player2_score


def adds_points(letter: str, mystery_phrase: str, current_view: str) -> bool:
    """Return True if and only if the first argument letter letter is one of
    the consonants and is present in the myster_phrase phrase but is not
    already displayed in the current_view view.

    >>> adds_points('b', 'burger', '^^r^er')
    True
    >>> adds_points('c', 'pizza', '^izz^')
    False
    """
    return (letter in ALL_CONSONANTS and letter in mystery_phrase
            and letter not in current_view)


def update_view(mystery_phrase: str, current_view: str, index_char: int,
                guess_char: str) -> str:
    """Return the updated view of the character if the guess_char guess
    at a pertucular index_char index is guessed correctly in the myster_phrase
    phrase. Otherwize return the myster_phrase phrase as it is.

    >>> update_view('ronaldo', '^o^al^o',5 , 'd')
    'd'
    >>> update_view('football', '^^^^^^^^',-1 ,'c')
    '^'
    """
    if mystery_phrase[index_char] == guess_char:
        return guess_char
    return current_view[index_char]


def compute_score(current_score: int, num_occurrences: int,
                  current_move: str) -> int:
    """Return the new updated score. If the current_move move choosen is Guess
    then return the same number of points as the num_occurrences occurrences.
    if the current_move is buy a vowel then current_score score decreases.

    >>> compute_score(3 ,2 , 'G')
    5
    >>> compute_score(4, 1 , 'B')
    3
    """
    if current_move == GUESS:
        return current_score + (num_occurrences * POINTS_PER_GUESS)
    return current_score - COST_OF_VOWEL


def next_turn(current_player: str, num_occurrences: int,
              game_type: str) -> str:
    """Return to the other player to play the next turn, if and only if the
    current_player player in the game_type does not guess the consonant
    properly or not buys a vowel resulting in no num_occurrances occurrances.

    game_type is either player vs player or player vs environment

    >>> next_turn('Player One',0, 'SP')
    'Player One'
    >>> next_turn('Player One',1, 'SP')
    'Player One'
    >>> next_turn('Player Two',0, 'PVP')
    'Player One'
    >>> next_turn('Player Two',1, 'PVP')
    'Player Two'
    >>> next_turn('Player One',0, 'PVE')
    'Player Two'
    >>> next_turn('Player One',1, 'PVE')
    'Player One'

    """

    return ((PLAYER_TWO if current_player == PLAYER_ONE
            else PLAYER_ONE)
            if num_occurrences == 0 and (game_type in (PVE, PVP))
            else current_player)


def is_mystery_char(index_char: int, mystery_phrase: str,
                    current_view: str) -> bool:
    """Return True if and only if the character at the given index_char index
    is currently displayed as a mystery character of the myster_phrase phrase
    in the current_view view in the game.

    >>> is_mystery_char(1,'fruit','f^^it')
    True
    >>> is_mystery_char(5,'vegetables','ve^e^able^')
    False
    >>> is_mystery_char(1, 'apple', '^^ple')
    False

    """
    return (mystery_phrase[index_char] != current_view[index_char] and
            mystery_phrase[index_char] not in current_view)


def environment_solves(current_view: str, difficulty_level: str,
                       consonants: str) -> bool:
    """Return true if and only if difficulty_level is Hard and the
    current_view view is half solved using the characters from the consonants
    or if all the consonants have been guessed OR if difficulty_level is Easy
    and there are no more consonants consonants available to choose form.

    >>> environment_solves('com^^te^', 'H', 'bdfghjklnpqrsvwxyz')
    True
    >>> environment_solves('^o^tw^^e', 'E', '')
    True
    >>> environment_solves('communication','H','')
    True
    >>> environment_solves('telephone','E','bcdfgjkmqrsvwxyz')
    False
    """
    return (difficulty_level == HARD and half_solved(current_view) or
            consonants == '') or (difficulty_level == EASY and
                                  consonants == '')


def delete(string_of_letters: str, index: int) -> str:
    """Return the string_of_letters letters when the character at the index
    index is removed.

    >>> delete('ronaldo is the goat', 8)
    'ronaldo s the goat'
    >>> delete('messi is not the goat', 17)
    'messi is not the oat'
    """
    if 0 <= index <= len(string_of_letters) - 1:
        return string_of_letters[: index] + string_of_letters[index + 1:]
    return string_of_letters


# This function is provided as a helper for one of the required functions.
def half_solved(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_solved('')
    True
    >>> half_solved('x')
    True
    >>> half_solved('^')
    False
    >>> half_solved('a^,^c!')
    True
    >>> half_solved('a^b^^e ^c^d^^d')
    False
    """

    num_mystery_chars = view.count(MYSTERY_CHAR)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_mystery_chars


if __name__ == '__main__':
    import doctest
    doctest.testmod()
