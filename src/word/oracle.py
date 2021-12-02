from typing import List, Tuple, Union
from src.util.config import System
import os.path as osp
import random
import sys


class WordOracle:

    def __init__(self) -> None:
        """ The init method """
        self.__words: List[str] = []  # A list of italian words

        path_words_prefix: str = System.PATH_SPLITTER.join(__file__.split(System.PATH_SPLITTER)[:-1])
        with open(osp.join(path_words_prefix, "660000_parole_italiane.txt"), mode="r") as stream:
            while word := stream.readline():
                self.__words.append(word)

        self.__lengths: List[Union[float, int]] = list(set([len(x) for x in self.__words]))  # Set of sizes of all the words in self.__words
        self.__lengths.append(float('inf'))                                                  # Add +inf to choose to not filter
        self.__lengths.append(float('-inf'))                                                 # Add -inf for the same above reason

    def get_rnd_length(self) -> Tuple[Union[int, float], Union[int, float]]:
        """ Returns a random length from the lengths set """
        x, y = random.choice(self.__lengths), random.choice(self.__lengths)
        return (x, y) if x > y else (y, x)  # Tuple (max, min)

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

    def get_word(self, n_times: int = 1, change_length: bool = True) -> Union[List[str],str]:
        """
        For n times yield a new word, each time with different or equal length.

        :param n_times: Number of generated words
        :param change_length: True if each word must has a different size
        :return: a generator
        """
        max_length, min_length = self.get_rnd_length()
        words: List[str] = []
        for _ in range(n_times):
            word: str = random.choice(self._filter(min_length=min_length,max_length=max_length))[:-1]

            if change_length:
                max_length, min_length = self.get_rnd_length()

            words.append(word)

        return words if n_times > 1 else words[-1]

