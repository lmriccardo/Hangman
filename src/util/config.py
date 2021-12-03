from typing import Tuple, Optional
import sys
from dataclasses import dataclass
from art import *
import curses
import os.path as osp


# Splitter for path in python, wrt the operating system
@dataclass
class System:
    PATH_SPLITTER   : str = "\\" if sys.platform == "win32" else "/"
    SCIFI_MUSIC     : str = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-2]), "music/scifi.mp3")
    TYPEWRITER_MUSIC: str = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-2]), "music/writer.mp3")
    MESSAGES_FILE   : str = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-2]), "conductor/messages.txt")
    WORDS_FILE      : str = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-2]), "word/660000_parole_italiane.txt")


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
    TITLE            : str = text2art("CMD-Line HANGMAN", font="contrast")
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
    CONDUCTOR        : str = "───────▄██████▄───────\n" + \
                             "──────▐▀▀▀▀▀▀▀▀▌──────\n" + \
                             "──────▌▌▀▀▌▐▀▀▐▐──────\n" + \
                             "──────▐──▄▄▄▄──▌──────\n" + \
                             "───────▌▐▌──▐▌▐───────\n"


# Constant for specified colors
@dataclass
class Colors:
    __black: int  = curses.COLOR_BLACK
    __setup: bool = False

    TITLE             : Tuple[int, int, Optional[int]] = (curses.COLOR_YELLOW, 1)
    START_GAME        : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  2)
    START_ROUND       : Tuple[int, int, Optional[int]] = (curses.COLOR_YELLOW, 1)
    ON_ERROR          : Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    3)
    END_POSITIVE_ROUND: Tuple[int, int, Optional[int]] = (curses.COLOR_BLUE,   4)
    END_NEGATIVE_ROUND: Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    3)
    END_GAME          : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  2)
    HANGMAN_CORRECT   : Tuple[int, int, Optional[int]] = (curses.COLOR_GREEN,  2)
    HANGMAN_ERROR     : Tuple[int, int, Optional[int]] = (curses.COLOR_RED,    3)

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
    def setup_colors(cls) -> None:
        """ Setup the colors generating the pairs """
        if not cls.setup():
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

            cls.set_setup(True)

    @classmethod
    def return_pair_for_index(cls, color_index: int) -> int:
        """ Return the corresponding pair identifier """
        return curses.color_pair(color_index)