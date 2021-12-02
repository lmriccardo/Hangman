from typing import Dict
from src.util.config import *
import os.path as osp
import curses
from curses.textpad import rectangle


class Conductor:
    def __init__(self) -> None:
        """ The init method """
        self.__msgs_file = open(osp.join(System.PATH_SPLITTER.join(__file__.split(System.PATH_SPLITTER)[:-1]), "messages.txt"))

        self.__msg_dict: Dict[str, Tuple[List[str], str]] = {  # Messages for each section of the conductor
            MsgSection.START_GAME         : ([], Colors.return_pair_for_index(Colors.START_GAME[1])),
            MsgSection.START_ROUND        : ([], Colors.return_pair_for_index(Colors.START_ROUND[1])),
            MsgSection.ON_ERROR           : ([], Colors.return_pair_for_index(Colors.ON_ERROR[1])),
            MsgSection.END_POSITIVE_ROUND : ([], Colors.return_pair_for_index(Colors.END_POSITIVE_ROUND[1])),
            MsgSection.END_NEGATIVE_ROUND : ([], Colors.return_pair_for_index(Colors.END_NEGATIVE_ROUND[1])),
            MsgSection.END_GAME           : ([], Colors.return_pair_for_index(Colors.END_GAME[1]))
        }

        self._fulfill()  # Fill the message dict

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

    @staticmethod
    def initialize_container(stdscr: curses.window) -> curses.window:
        """ Initialize the new container for the conductor messages """
        conductor_window = curses.newwin(11, curses.COLS - 2, 9, 1)
        stdscr.addstr(9, 3, "Conductor", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        conductor_window.clear()
        conductor_window.box()

        return conductor_window

    @staticmethod
    def add_condactor_art() -> curses.window:
        """ Add the Ascii Art of the conductor """
        conductor_pad = curses.newpad(100, 100)
        conductor_pad.clear()
        conductor_pad.addstr(AsciiArt.CONDUCTOR, curses.A_BOLD)

        return conductor_pad

    def print(self, cond_window: curses.window, section: str) -> None:
        """ Print the messages of the corresponding section """
        try:

            lines, color = self.__msg_dict[section]
            for i, line in enumerate(lines):
                cond_window.addstr(2 + i, 3, line, color | curses.A_BOLD)

        except (KeyboardInterrupt, EOFError):
            sys.exit(0)