from typing import Tuple, Dict, Union
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
    WORDS_FILE      : str = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-2]), "word/words_ita.txt")


# Constant name for conductor message
@dataclass
class Messages:
    START_GAME        : Tuple[str] = (
        "Hi, Welcome in the Hangman game!",
        "In each round a word will be selected",
        "Some of its letters are yet shown",
        "Your goal is to guess as many words as you can",
        "Be careful! You have limited time",
        "Select the char textbox using arrows",
        "Write a letter using the corresponding key"
    )

    START_ROUND       : Tuple[str] = (
        "The game has started",
        "Go! Remember, you have limited time"
    )

    ON_ERROR          : Tuple[str] = (
        "Oh No! You miss that"
    )

    END_POSITIVE_ROUND: Tuple[str] = (
        "Well done! Let start another round"
    )

    END_NEGATIVE_ROUND: Tuple[str] = (
        "Don't give up!",
        "You will do better in the next round"
    )

    END_GAME          : Tuple[str] = (
        "The game has ended.",
        "Score: "
    )

    ASK_DIFFICULTY    : Tuple[str] = (
        "Choose which difficulty you wanna play with"
    )

    INFO_DIFFICULTY   : Tuple[str] = (
        "{intro} ... Do You wanna something {diff}?",
        "Ok, Let's do it ... Remember you have {time_per_round} minute per round",
        "Up to {nround} round, with max score each of {max_score} (in percentage)",
        "The word queried can be {length} lenght, and for each wrong guess {penalty}",
        "part of the body will be added to the hangman.",
        "You can have {hints} hint, and for each used hint you will have {hint_penalty}"
    )


# Constant for ascii art of the game
@dataclass
class AsciiArt:
    TITLE            : str = text2art("CMD-Line HANGMAN", font="contrast")
    HANGMAN          : str = "-------------\n"\
                             "=============\n" + \
                             "|█          |\n" + \
                             "|█          {head}\n" + \
                             "|█         {larm}{body}{rarm}\n" + \
                             "|█        {lfoot}{lleg} {rleg}{rfoot}\n" + \
                             "|█          \n" + \
                             "|█          \n" + \
                             "|█          \n" + \
                             "|█          \n" + \
                             "|█          \n" + \
                             "|█          \n" + \
                             "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n" + \
                             "###################\n"
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

    TITLE             : Tuple[int, int] = (curses.COLOR_YELLOW, 1)
    START_GAME        : Tuple[int, int] = (curses.COLOR_GREEN,  2)
    START_ROUND       : Tuple[int, int] = (curses.COLOR_YELLOW, 1)
    ON_ERROR          : Tuple[int, int] = (curses.COLOR_RED,    3)
    END_POSITIVE_ROUND: Tuple[int, int] = (curses.COLOR_BLUE,   4)
    END_NEGATIVE_ROUND: Tuple[int, int] = (curses.COLOR_RED,    3)
    END_GAME          : Tuple[int, int] = (curses.COLOR_GREEN,  2)
    HANGMAN_CORRECT   : Tuple[int, int] = (curses.COLOR_GREEN,  2)
    HANGMAN_ERROR     : Tuple[int, int] = (curses.COLOR_RED,    3)
    GAME_BORDER_WIN   : Tuple[int, int] = (curses.COLOR_RED,    3)

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


# Recall all the settings for each game's difficulty
@dataclass
class GameSettings:
    __SettingDictType = Tuple[Tuple[str, Union[str, int, Tuple[int, int]]]]

    MAX_ROUND_TIME:   str = "MAX ROUND TIME"
    TOT_ROUND_NUMBER: str = "TOT ROUND NUMBER"
    GAME_DIFFICULTY:  str = "GAME DIFFICULTY"
    MAX_ROUND_SCORE:  str = "MAX ROUND SCORE"
    WORD_LENGTH:      str = "WORD LENGHT"
    PENALTY:          str = "PENALTY"
    HINT_NUMBER:      str = "HINT NUMBER"
    HINT_PENALTY:     str = "HINT PENALTY"
    INTRO:            str = "INTRO"

    EASY_SETUP: __SettingDictType = (
        ("MAX ROUND TIME",        60),
        ("TOT ROUND NUMBER",      10),
        ("GAME DIFFICULTY",   "Easy"),
        ("MAX ROUND SCORE",      100),
        ("WORD LENGHT",       (5, 7)),
        ("PENALTY",                1),
        ("HINT NUMBER",       (3, 5)),
        ("HINT PENALTY",           0),
        ("INTRO","You stupid newbie")
    )

    MEDIUM_SETUP: __SettingDictType = (
        ("MAX ROUND TIME",       300),
        ("TOT ROUND NUMBER",      10),
        ("GAME DIFFICULTY", "Medium"),
        ("MAX ROUND SCORE",      100),
        ("WORD LENGHT",       (7, 9)),
        ("PENALTY",                1),
        ("HINT NUMBER",       (2, 4)),
        ("HINT PENALTY",           0),
        ("INTRO","You that avoid difficulties")
    )

    HARD_SETUP: __SettingDictType = (
        ("MAX ROUND TIME",       600),
        ("TOT ROUND NUMBER",      10),
        ("GAME DIFFICULTY",   "Hard"),
        ("MAX ROUND SCORE",      100),
        ("WORD LENGHT",      (9, 11)),
        ("PENALTY",                1),
        ("HINT NUMBER",       (1, 3)),
        ("HINT PENALTY",           0),
        ("INTRO",      "You foolish")
    )

    VERY_HARD_SETUP: __SettingDictType = (
        ("MAX ROUND TIME",           1200),
        ("TOT ROUND NUMBER",           10),
        ("GAME DIFFICULTY",   "Very Hard"),
        ("MAX ROUND SCORE",           100),
        ("WORD LENGHT",          (11, 20)), # -1 means maximum
        ("PENALTY",                     2),
        ("HINT NUMBER",          (1,   3)),
        ("HINT PENALTY",                1),  # Final score -= len(word) / (max_hint * 100)
        ("INTRO",    "You stupid foolish")
    )

    @classmethod
    def get_settings(cls, difficulty: str) -> Dict[str, Union[str, int, Tuple[int, int]]]:
        """ Return the setting of the corresponding difficulty """
        return dict(
            {
                "Easy": cls.EASY_SETUP,
                "Medium": cls.MEDIUM_SETUP,
                "Hard": cls.HARD_SETUP,
                "Very Hard": cls.VERY_HARD_SETUP
            }.get(difficulty)
        )