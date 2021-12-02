from typing import List, Dict
from rich.console import Console
from src.util.config import *
from time import sleep
import os.path as osp
import curses


class Conductor:
    def __init__(self) -> None:
        """ The init method """
        self.__msgs_file = open(osp.join(System.PATH_SPLITTER.join(__file__.split(System.PATH_SPLITTER)[:-1]), "messages.txt"))

        # Define color pair and get the respective number
        stg_pair, str_pair, oner_pair, endposrnd_pair, endnegrnd_pair, endgame_pair = [Colors.return_pair_for_index(i) for i in range(2, 8)]

        self.__msg_dict: Dict[str, Tuple[List[str], str]] = {  # Messages for each section of the conductor
            MsgSection.START_GAME         : ([], stg_pair),
            MsgSection.START_ROUND        : ([], str_pair),
            MsgSection.ON_ERROR           : ([], oner_pair),
            MsgSection.END_POSITIVE_ROUND : ([], endposrnd_pair),
            MsgSection.END_NEGATIVE_ROUND : ([], endnegrnd_pair),
            MsgSection.END_GAME           : ([], endgame_pair)
        }

        self._fulfill()  # Fill the message dict

    @staticmethod
    def _setup_colors() -> List[int]:
        """ Setup the colors for each sections and retursn  """
        # curses.init_pair(Colors.START_GAME[1], Colors.START_GAME[0], Colors.black)  # For start_game
        # curses.init_pair(Colors.START_ROUND[1], Colors.START_ROUND[0], Colors.black)  # For START_round
        # curses.init_pair(Colors.ON_ERROR[1], Colors.ON_ERROR[0], Colors.black)  # For ON_ERROR
        # curses.init_pair(Colors.END_POSITIVE_ROUND[1], Colors.END_POSITIVE_ROUND[0], Colors.black)  # For END_POSITIVE_ROUND
        # curses.init_pair(Colors.END_NEGATIVE_ROUND[1], Colors.END_NEGATIVE_ROUND[0], Colors.black)  # For END_NEGATIVE_ROUND
        # curses.init_pair(Colors.END_GAME[1], Colors.END_GAME[0], Colors.black)  # For END_GAME

        # return [curses.color_pair(i) for i in range(2, 8)]
        ...

    def _fulfill(self) -> None:
        """ Fill the list for each section of the message file """
        start_game = start_round = on_error = end_positive_round = end_negative_round = end_game = False
        while line := self.__msgs_file.readline():
            if line.isupper():
                start_game = line == MsgSection.START_GAME + ":\n"
                start_round = line == MsgSection.START_ROUND + ":\n"
                on_error = line == MsgSection.ON_ERROR + ":\n"
                end_positive_round = line == MsgSection.END_POSITIVE_ROUND + ":\n"
                end_negative_round = line == MsgSection.END_NEGATIVE_ROUND + ":\n"
                end_game = line == MsgSection.END_GAME + ":\n"
                continue

            if start_game and line != "\n": self.__msg_dict[MsgSection.START_GAME][0].append(line[2:-1])
            if start_round and line != "\n": self.__msg_dict[MsgSection.START_ROUND][0].append(line[2:-1])
            if on_error and line != "\n": self.__msg_dict[MsgSection.ON_ERROR][0].append(line[2:-1])
            if end_positive_round and line != "\n": self.__msg_dict[MsgSection.END_POSITIVE_ROUND][0].append(line[2:-1])
            if end_negative_round and line != "\n": self.__msg_dict[MsgSection.END_NEGATIVE_ROUND][0].append(line[2:-1])
            if end_game and line != "\n": self.__msg_dict[MsgSection.END_GAME][0].append(line[2:-1])

    def print(self, stdscr: curses.window, section: str) -> None:
        """ Print the messages of the corresponding section """
        try:

            lines, color = self.__msg_dict[section]
            for i, line in enumerate(lines):
                stdscr.addstr(10 + i,10, line, color | curses.A_BOLD)

        except (KeyboardInterrupt, EOFError):
            sys.exit(0)