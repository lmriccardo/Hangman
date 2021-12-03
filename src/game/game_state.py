from typing import List
import random


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
    def __init__(self, round: int, word: str, nguessed_char: int = 0, game_diff: str = "Hard") -> None:
        """ The init method """
        self.__round = round                                     # The current round
        self.__word  = word                                      # The current word to guess
        self.__number_of_guessed_lettes = nguessed_char          # How many letters the player has guessed
        self.__word_state: List[str] = ["_"] * len(self.__word)  # The state of the current word = _ for unknow letters, chr for known or guessed
        self.__game_difficulty = game_diff                       # The game difficulty



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
    def game_difficulty(self) -> str:
        """ Return the game difficulty """
        return self.__game_difficulty

    @game_difficulty.setter
    def game_difficulty(self, new_diff) -> None:
        """ Set a new difficulty for the game """
        self.__game_difficulty = new_diff

