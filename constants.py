"""What's that Phrase? game constants."""

# points earned on each occurrence of a correctly guessed consonant
POINTS_PER_GUESS = 1

# cost of buying a vowel, does not depend on the number of occurrences
COST_OF_VOWEL = 1

# points earned on each occurrence of consonant mystery characters at
# the time of solving the puzzle
BONUS_POINTS = 2

# players' names
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# menu options
GUESS = 'G'      # guess a consonant
BUY = 'B'        # buy a vowel
SOLVE = 'S'      # try to solve the puzzle
QUIT = 'Q'       # quit the game

# symbol used for mystery characters
MYSTERY_CHAR = '^'

# Game types
SINGLE_PLAYER = 'SP'  # one player
PVP = 'PVP'           # two players, player vs player
PVE = 'PVE'           # two players, player vs environment

# computer difficulty levels
EASY = 'E'  # computer plays the "easy" strategy
HARD = 'H'  # computer plays the "hard" strategy

# all consonants and all vowels
ALL_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALL_VOWELS = 'aeiou'

# the order in which a computer player, hard difficulty level, will
# guess consonants
PRIORITY_CONSONANTS = 'tnrslhdcmpfygbwvkqxjz'
