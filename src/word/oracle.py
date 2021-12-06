from typing import List, Union, Generator
from src.util.config import System
import random


class WordOracle:

    def __init__(self) -> None:
        """ The init method """
        self.__words: List[str] = []  # A list of italian words

        with open(System.WORDS_FILE, mode="r") as stream:
            while word := stream.readline():
                self.__words.append(word)

    def _filter(self, min_length: float = float('-inf'), max_length: float = float('inf')) -> List[str]:
        """
        Returns a new list of words s.t. each w in the new list min_length <= |w| <= max_lenght w starts with suffix and ends with prefix.

        :param min_length: The min length of the new words
        :param max_length: The max length of the new words
        :return: A list of words
        """
        return list(
            filter(
                lambda x: (min_length <= len(x) <= max_length),
                self.__words
            )
        )

    def get_word(self, max_length: int, min_length: int, n_times: int = 1) -> Generator:
        """
        For n times yield a new word, each time with different or equal length.

        :param n_times: Number of generated words
        :param max_length: Max word length
        :param min_length: Min word length
        :return: a generator
        """
        already_taken: List[str] = []
        i = 0
        while i < n_times:
            current_word: str = random.choice(self._filter(min_length=min_length,max_length=max_length))[:-1]
            if current_word not in already_taken:
                already_taken.append(current_word)
                i += 1
                yield current_word