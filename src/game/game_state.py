from typing import List, Optional, Tuple
from util.config import GameSettings


class GameSetting:
    """
    Describe the setting of the current game in terms of:
    - Max time per round (sec)
    - Total Number of round
    - Game difficulty (Easy, Medium, Hard, Very Hard)
    - Max round score
    - Word lenght range (min, max)
    - Penalty (how many parts of the body to add)
    - Number of hint's range (min, max), obv depends upon the len of the word
    - Hint penalty (drop a scalar from the max score of the current word)
    """
    def __init__(self, game_difficulty: Optional[str] = "Hard", **kargs) -> None:
        """ The init method """
        # If the game difficulty is given then take the default settings
        if game_difficulty is not None:
            self.__settings = GameSettings.get_settings(game_difficulty)
        else:
            GameSetting.check_correctness_custom_settings(kargs)
            self.__settings = kargs

    @staticmethod
    def check_correctness_custom_settings(custom_settings) -> None:
        """ Raise AssertionError is the custom settings are not valid """
        assert GameSettings.MAX_ROUND_TIME in custom_settings.keys(), "Missing MAX ROUND TIME"      # Check for the MAX ROUND TIME
        assert GameSettings.TOT_ROUND_NUMBER in custom_settings.keys(), "Missing TOT ROUND NUMBER"  # Check for the TOT ROUND NUMBER
        assert GameSettings.GAME_DIFFICULTY in custom_settings.keys(), "Missing GAME DIFFICULTY"    # Check for the GAME DIFFICULTY
        assert GameSettings.MAX_ROUND_SCORE in custom_settings.keys(), "Missing MAX ROUND SCORE"    # Check for the MAX ROUND SCORE
        assert GameSettings.WORD_LENGTH in custom_settings.keys(), "Missing WORD LENGHT"            # Check for the WORD LENGHT
        assert GameSettings.PENALTY in custom_settings.keys(), "Missing PENALTY"                    # Check for the PENALTY
        assert GameSettings.HINT_NUMBER in custom_settings.keys(), "Missing HINT NUMBER"            # Check for the HINT NUMBER
        assert GameSettings.HINT_PENALTY in custom_settings.keys(), "Missing HINT PENALTY"          # Check for the HINT PENALTY
        assert GameSettings.INTRO in custom_settings.keys(), "Missing INTRO"                        # Check for intro message

    def get_max_time_per_round(self) -> int:
        """ Return the maximum time per round in seconds """
        return self.__settings[GameSettings.MAX_ROUND_TIME]

    def get_total_round_number(self) -> int:
        """ Return the total number of round for the game """
        return self.__settings[GameSettings.TOT_ROUND_NUMBER]

    def get_game_difficulty(self) -> str:
        """ Return the game difficulty """
        return self.__settings[GameSettings.GAME_DIFFICULTY]

    def get_max_round_score(self) -> int:
        """ Return the maximum score that a user could get from a single round (in %) """
        return self.__settings[GameSettings.MAX_ROUND_SCORE]

    def get_word_lenght(self) -> Tuple[int, int]:
        """ Return the min and the max word lenght for the current difficulty """
        return self.__settings[GameSettings.WORD_LENGTH]

    def get_penalty(self) -> int:
        """ Return the penalty (in terms on number of body part to add) """
        return self.__settings[GameSettings.PENALTY]

    def get_number_of_hints(self) -> Tuple[int, int]:
        """ Return the min and the max number of hint available depends on the current word lenght """
        return self.__settings[GameSettings.HINT_NUMBER]

    def get_hint_penalty(self) -> int:
        """ Return a bit 0/1. If 0 no penalty, otherwise tot_score = tot_score - (word_len) / (max_hint * 100) """
        return self.__settings[GameSettings.HINT_PENALTY]

    def get_intro(self)-> str:
        """ Return the intro message """
        return self.__settings[GameSettings.INTRO]

    def change_game_difficulty(self, new_difficulty: str) -> None:
        """ Change the game difficulty and set new settings """
        self.__settings = GameSettings.get_settings(new_difficulty)

    def map_wordlen_maxhints(self, wordlen: int) -> int:
        """ Return the maximum number of hints for a given word len """
        wordlen_sett = self.__settings[GameSettings.WORD_LENGTH]
        wordlen_ranges = list(range(wordlen_sett[0], wordlen_sett[1] + 1))

        hints_sett = self.__settings[GameSettings.HINT_NUMBER]
        hints_range = list(range(hints_sett[0], hints_sett[1] + 1))

        try:
            word_len_index = wordlen_ranges.index(wordlen)
            return hints_range[word_len_index]
        except (ValueError, IndexError):
            return hints_range[-1]


class GameStatus:
    """
    Describe the current state of the game in terms of:
    - current round
    - current word
    - number of guessed letters
    - number of wrong guessed letters
    - state of the word to guess
    - game settings
    - length of the current word to guess
    - number of hints
    """
    def __init__(self, settings: GameSetting) -> None:
        """ The init method """
        self.__game_settings = settings  # The current settings of the game

        self.__round = 0                      # The current round
        self.__word  = ""                     # The current word to guess
        self.__number_of_guessed_letters = 0  # How many letters the player has guessed
        self.__number_of_wrong_letters = 0    # How many letters the player has guessed wrong
        self.__score = 0                      # The user score
        self.__penalty = 0                    # Number of obtained penalty

        self.__len_current_word = 0      # The length of the current word that has to be guessed
        self.__number_of_used_hints = 0  # Number of used hints

        # The state of the current word = _ for unknow letters, chr for known or guessed
        self.__word_state: List[str] = ["_"] * self.__len_current_word

    @property
    def game_settings(self):
        """ Return the current game settings """
        return self.__game_settings

    @property
    def round(self) -> int:
        """ Return the current round of the game """
        return self.__round

    @round.setter
    def round(self, new_value) -> None:
        """ Update the value of the attribute round """
        self.__round = new_value

    @property
    def word(self) -> str:
        """ Return the current word to guess """
        return self.__word

    @property
    def number_of_guessed_letters(self) -> int:
        """ Return the number of letters the user has guessed """
        return self.__number_of_guessed_letters

    @number_of_guessed_letters.setter
    def number_of_guessed_letters(self, new_value: int) -> None:
        """ Update the value of the attribute number_of_guessed_letters """
        self.__number_of_guessed_letters = new_value

    @property
    def number_of_wrong_letters(self) -> int:
        """ Return the number of wrong guess """
        return self.__number_of_wrong_letters

    @number_of_wrong_letters.setter
    def number_of_wrong_letters(self, new_value: int) -> None:
        """ Update the value of the attribute number_of_wrong_letters """
        self.__number_of_wrong_letters = new_value

    @property
    def word_state(self) -> List[str]:
        """ Return the state of the current word, i.e., which letters have been guessed """
        return self.__word_state

    def update_word_state(self, idx: int, letter: str) -> None:
        """ Update the state of the word inserting in the index idx the letter "letter" """
        self.__word_state[idx] = letter

    @property
    def score(self) -> int:
        """ Return the score of the user """
        return self.__score

    @score.setter
    def score(self, new_value) -> None:
        """ Set a new value for score """
        self.__score = new_value

    @property
    def penalty(self) -> int:
        """ Return the penalty counter """
        return self.__penalty

    @penalty.setter
    def penalty(self, new_value: int) -> None:
        """ Set a new value for the attribute penalty """
        self.__penalty = new_value

    @property
    def len_current_word(self) -> int:
        """ Return the length of the current word """
        return self.__len_current_word

    @property
    def number_of_used_hints(self) -> int:
        """ Return the number of used hint """
        return self.__number_of_used_hints

    @number_of_used_hints.setter
    def number_of_used_hints(self, new_value) -> None:
        """ Set a new value for the attribute number_of_used_hints """
        self.__number_of_used_hints = new_value

    def next_round(self, word: str) -> None:
        """
        Start a new round updating the current state with a new state:
        1. increments the round counter
        2. reset all the other counter
        3. do other useful but uninteresting stuff
        """
        self.__word = word
        self.__len_current_word = len(self.__word)
        self.__round += 1
        self.__number_of_used_hints = 0
        self.__number_of_wrong_letters = 0
        self.__number_of_guessed_letters = 0
        self.__penalty = 0

        # We set some letters of the word_state to clear depending on the difficulty
        self.__word_state = [" "] * self.__len_current_word
        if self.__game_settings.get_game_difficulty() in ["Hard", "Very Hard"]:
            self.__word_state[0] = self.__word[0]
            self.__word_state[len(self.__word)//2] = self.__word[len(self.__word) // 2]
            self.__word_state[-1] = self.__word[-1]
        elif self.__game_settings.get_game_difficulty() == "Easy":
            self.__word_state[0] = self.__word[0]
        else:
            self.__word_state[0] = self.__word[0]
            self.__word_state[-1] = self.__word[-1]