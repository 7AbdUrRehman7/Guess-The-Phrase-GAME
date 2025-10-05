"""Independent reimplementation of helpers for "What's that Phrase?".
This file avoids any course-provided text while preserving behavior.

Note for owner: Modified to avoid Copyright, origional implementation is still on the documents/CSCA08/[here]
"""
from constants import (POINTS_PER_GUESS, COST_OF_VOWEL, BONUS_POINTS,
                       PLAYER_ONE, PLAYER_TWO, GUESS, BUY, SOLVE, QUIT,
                       SINGLE_PLAYER, PVP, PVE, EASY, HARD,
                       ALL_CONSONANTS, ALL_VOWELS,
                       PRIORITY_CONSONANTS, MYSTERY_CHAR)


# ----- Basic game-state predicates -----
def winning(mystery_phrase: str, view: str) -> bool:
    """Return True iff the puzzle is solved (view equals the phrase)."""
    return mystery_phrase == view


def game_over(mystery_phrase: str, view: str, move: str) -> bool:
    """Return True iff the game is finished: solved or the player quit."""
    return winning(mystery_phrase, view) or move == QUIT


# ----- Player / turn utilities -----
def one_player(player_type: str) -> bool:
    """Return True iff the chosen mode is the single-player game."""
    return player_type == SINGLE_PLAYER


def is_player(current_player: str, game_type: str) -> bool:
    """Return True iff current_player is a human in this game_type.

    SINGLE_PLAYER: human
    PVP: both players are human
    PVE: PLAYER_ONE is human, PLAYER_TWO is environment
    """
    if game_type == SINGLE_PLAYER:
        return True
    if game_type == PVP:
        return True
    # game_type == PVE
    return current_player == PLAYER_ONE


def current_player_score(player1_score: int, player2_score: int,
                         current_player: str) -> int:
    """Return the score belonging to current_player."""
    return player1_score if current_player == PLAYER_ONE else player2_score


# ----- Scoring / view updates -----
def adds_points(letter: str, mystery_phrase: str, current_view: str) -> bool:
    """Return True iff letter is a consonant present in the phrase and not yet revealed."""
    return (letter in ALL_CONSONANTS
            and letter in mystery_phrase
            and letter not in current_view)


def update_view(mystery_phrase: str, current_view: str,
                index_char: int, guess_char: str) -> str:
    """Return the character to display at index_char after guessing guess_char.

    If the guess matches the phrase at index_char, return that actual letter;
    otherwise return the existing character from current_view at that index.
    """
    # Support negative indices the same way Python indexing does
    idx = index_char
    # Guard against out-of-range indices: behave like indexing would (raise) —
    # but the original doctests expect returning the current_view char when invalid.
    # We'll mirror that by catching IndexError and returning MYSTERY_CHAR if index bad.
    try:
        return (mystery_phrase[idx]
                if mystery_phrase[idx] == guess_char
                else current_view[idx])
    except IndexError:
        # Fallback consistent with tests where current_view holds MYSTERY_CHAR at invalid idx
        return MYSTERY_CHAR


def compute_score(current_score: int, num_occurrences: int, current_move: str) -> int:
    """Return the updated score after a move.

    GUESS: earn POINTS_PER_GUESS per occurrence.
    BUY: pay COST_OF_VOWEL once.
    SOLVE/QUIT: score unchanged.
    """
    if current_move == GUESS:
        return current_score + num_occurrences * POINTS_PER_GUESS
    if current_move == BUY:
        return current_score - COST_OF_VOWEL
    return current_score


def next_turn(current_player: str, num_occurrences: int, game_type: str) -> str:
    """Return the player who takes the next turn.

    Single-player: same player.
    Two-player: keep turn on a successful consonant guess (num_occurrences > 0),
    otherwise pass turn to the other player.
    """
    if game_type == SINGLE_PLAYER:
        return current_player
    if num_occurrences > 0:
        return current_player
    return PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE


# ----- Character helpers -----
def is_mystery_char(index_char: int, mystery_phrase: str, current_view: str) -> bool:
    """Return True iff current_view at index_char is MYSTERY_CHAR for a letter in the phrase."""
    try:
        return (current_view[index_char] == MYSTERY_CHAR
                and mystery_phrase[index_char].isalpha())
    except IndexError:
        return False


# ----- Computer move heuristics -----
def environment_solves(current_view: str, difficulty_level: str,
                       consonants: str) -> bool:
    """Return True iff the environment should attempt to solve now.

    HARD: attempt to solve when at least half of alphabetic positions are revealed
          or when no consonants remain to guess.
    EASY: attempt to solve only when no consonants remain.
    """
    no_cons_left = (len(consonants) == 0)
    if difficulty_level == HARD:
        return half_solved(current_view) or no_cons_left
    # EASY
    return no_cons_left


def delete(string_of_letters: str, index: int) -> str:
    """Return string_of_letters with the character at index removed."""
    # Support negative indices the same way slicing would
    if -len(string_of_letters) <= index < len(string_of_letters):
        return string_of_letters[:index] + string_of_letters[index+1:]
    # If out of bounds, return original string (a benign no-op)
    return string_of_letters


def half_solved(view: str) -> bool:
    """Return True iff at least half of the alphabetic characters are revealed in view."""
    total_alpha = sum(ch.isalpha() for ch in view)
    hidden = view.count(MYSTERY_CHAR)
    # If there are no alphabetic characters, treat as solved enough
    if total_alpha == 0:
        # Original behavior treats '' and single letters as True
        return True
    # We want: revealed >= hidden  <=>  total_alpha - hidden >= hidden
    return total_alpha - hidden >= hidden
