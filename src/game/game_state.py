from typing import List, Optional, Tuple
from src.util.config import GameSettings
import random


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


class GameStatus:
    """
    Describe the current state of the game in terms of:
    - current round
    - current word
    - number of guessed letters
    - state of the word to guess
    - current selected "textbox"
    - game difficulty (Easy, Medium, Hard, Very Hard)
    """
    def __init__(self, round: int, word: str, nguessed_char: int = 0) -> None:
        """ The init method """
        self.__round = round                                     # The current round
        self.__word  = word                                      # The current word to guess
        self.__number_of_guessed_lettes = nguessed_char          # How many letters the player has guessed
        self.__word_state: List[str] = ["_"] * len(self.__word)  # The state of the current word = _ for unknow letters, chr for known or guessed
        self.__score = 0                                         # The user score

    @property
    def round(self) -> int:
        """ Return the current round of the game """
        return self.__round

    @round.setter
    def round(self, new_round) -> None:
        """ Set the value of round """
        self.__round = new_round

    @property
    def word(self) -> str:
        """ Return the current word to guess """
        return self.__word

    @word.setter
    def word(self, new_word) -> None:
        """ Set the value for word """
        self.__word = new_word

    @property
    def number_of_guessed_lettes(self) -> int:
        """ Return the number of letters the user has guessed """
        return self.__number_of_guessed_lettes

    @number_of_guessed_lettes.setter
    def number_of_guessed_lettes(self, new_value) -> None:
        """ Set the value of the number ... """
        self.__number_of_guessed_lettes = new_value

    @property
    def score(self) -> int:
        """ Return the score of the user """
        return self.__score

    @score.setter
    def score(self, new_score) -> None:
        """ Add a new score """
        self.__score += new_score