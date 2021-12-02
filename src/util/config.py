from typing import Tuple, List, Optional
import sys
from dataclasses import dataclass
from art import *
import curses


# Splitter for path in python, wrt the operating system
@dataclass
class System:
    PATH_SPLITTER: str = "\\" if sys.platform == "win32" else "/"

# Constant name for conductor message
@dataclass
class MsgSection:
    START_GAME        : str = "START GAME"
    START_ROUND       : str = "START ROUND"
    ON_ERROR          : str = "ON ERROR"
    END_POSITIVE_ROUND: str = "END POSITIVE ROUND"
    END_NEGATIVE_ROUND: str = "END NEGATIVE ROUND"
    END_GAME          : str = "END GAME"

# Constant for ascii art of the game
@dataclass
class AsciiArt:
    TITLE            : str = text2art("CMD-Line HANGMAN")
    HANGMAN          : str = "  -------\n" + \
                             "  |     |\n" + \
                             "  |     {head}\n" + \
                             "  |    {larm}{body}{rarm}\n" + \
                             "  |   {lfoot}{lleg} {rleg}{rfoot}\n" + \
                             "  |      \n" + \
                             "############\n"
    HANGMAN_HEAD     : str = "O"
    HANGMAN_BODY     : str = "|"
    HANGMAN_LEFT_ARM : str = "/"
    HANGMAN_LEFT_LEG : str = "/"
    HANGMAN_RIGHT_ARM: str = "\\"
    HANGMAN_RIGHT_LEG: str = "\\"
    HANGMAN_FOOT     : str = "_"

# Constant for specified colors
@dataclass
class Colors:
    __black: int  = curses.COLOR_BLACK
    __setup: bool = False

    TITLE             : Tuple[int, int, Optional[int]] = (curses.COLOR_YELLOW, 1)
    START_GAME        : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  2)
    START_ROUND       : Tuple[int, int, Optional[int]] = (curses.COLOR_YELLOW, 3)
    ON_ERROR          : Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    4)
    END_POSITIVE_ROUND: Tuple[int, int, Optional[int]] = (curses.COLOR_BLUE,   5)
    END_NEGATIVE_ROUND: Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    6)
    END_GAME          : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  7)
    HANGMAN_CORRECT   : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  8)
    HANGMAN_ERROR     : Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    9)

    @classmethod
    def black(cls) -> int:
        return cls.__black

    @classmethod
    def setup(cls) -> bool:
        return cls.__setup

    @classmethod
    def set_setup(cls, new_value: bool) -> None:
        cls.__setup = new_value

    @classmethod
    def setup_colors(cls) -> List[int]:
        """ Setup the colors generating the pairs """
        if not cls.setup():
            curses.init_pair(cls.TITLE[1], cls.TITLE[0], cls.black())  # For the title
            curses.init_pair(cls.START_GAME[1], cls.START_GAME[0], cls.black())  # For start_game
            curses.init_pair(cls.START_ROUND[1], cls.START_ROUND[0], cls.black())  # For START_round
            curses.init_pair(cls.ON_ERROR[1], cls.ON_ERROR[0], cls.black())  # For ON_ERROR
            curses.init_pair(cls.END_POSITIVE_ROUND[1], cls.END_POSITIVE_ROUND[0], cls.black())  # For END_POSITIVE_ROUND
            curses.init_pair(cls.END_NEGATIVE_ROUND[1], cls.END_NEGATIVE_ROUND[0], cls.black())  # For END_NEGATIVE_ROUND
            curses.init_pair(cls.END_GAME[1], cls.END_GAME[0], cls.black())  # For END_GAME
            curses.init_pair(cls.HANGMAN_CORRECT[0], cls.HANGMAN_CORRECT[1], cls.black())  # For correct guess
            curses.init_pair(cls.HANGMAN_ERROR[0], cls.HANGMAN_ERROR[1], cls.black())  # For wrong guess

            cls.set_setup(True)

    @classmethod
    def return_pair_for_index(cls, color_index: int) -> int:
        """ Return the corresponding pair identifier """
        return curses.color_pair(color_index)