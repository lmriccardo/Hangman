import time
from typing import Dict, List
from src.util.config import *
import curses
import pydub
import pydub.playback as playbck
import multiprocessing


class Conductor:
    def __init__(self) -> None:
        """ The init method """
        self.__msgs_file = open(System.MESSAGES_FILE)

        self.__msg_dict: Dict[str, Tuple[List[str], str]] = {  # Messages for each section of the conductor
            MsgSection.START_GAME         : ([], Colors.return_pair_for_index(Colors.START_GAME[1])),
            MsgSection.START_ROUND        : ([], Colors.return_pair_for_index(Colors.START_ROUND[1])),
            MsgSection.ON_ERROR           : ([], Colors.return_pair_for_index(Colors.ON_ERROR[1])),
            MsgSection.END_POSITIVE_ROUND : ([], Colors.return_pair_for_index(Colors.END_POSITIVE_ROUND[1])),
            MsgSection.END_NEGATIVE_ROUND : ([], Colors.return_pair_for_index(Colors.END_NEGATIVE_ROUND[1])),
            MsgSection.END_GAME           : ([], Colors.return_pair_for_index(Colors.END_GAME[1]))
        }

        self.__window = None

        self._fulfill()  # Fill the message dict

        # Get the sound of the typewriter
        self.__type_writer_sound = pydub.AudioSegment.from_mp3(System.TYPEWRITER_MUSIC)[:-100]
        self.__type_writer_sound += self.__type_writer_sound * 6 + self.__type_writer_sound[:-1000]
        self.__type_writer_sound -= 30
        self.__music_thread = multiprocessing.Process(target=playbck.play, args=(self.__type_writer_sound,))

    @property
    def music_thread(self) -> multiprocessing.Process:
        """ Return the Process object for the music player """
        return self.__music_thread

    @property
    def window(self):
        """ Return the window of the conductor """
        return self.__window

    @window.setter
    def window(self, new_value) -> None:
        """ Set the new value for the attribute window """
        self.__window = new_value

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
    def initialize_container() -> curses.window:
        """ Initialize the new container for the conductor messages """
        y_postion = 2 + len(AsciiArt.TITLE.split("\n")) + 1 # The +2s are the padding
        conductor_window = curses.newwin(11, curses.COLS - 2, y_postion, 1)
        conductor_window.nodelay(True)
        conductor_window.box()
        conductor_window.addstr(0, 3, "Conductor", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        conductor_window.noutrefresh()

        return conductor_window

    @staticmethod
    def add_condactor_art() -> None:
        """ Add the Ascii Art of the conductor """
        conductor_pad = curses.newpad(100, 100)
        conductor_pad.clear()
        conductor_pad.addstr(AsciiArt.CONDUCTOR, curses.A_BOLD)
        conductor_pad.noutrefresh(0, 0, 13, curses.COLS - 30, 18, curses.COLS - 9)

    def print(self, section: str) -> None:
        """ Print the messages of the corresponding section """
        self.__music_thread.start()
        lines, color = self.__msg_dict[section]

        for i, line in enumerate(lines):
            j = 3
            for char in line:
                self.__window.addstr(2 + i, j, char, color | curses.A_BOLD)
                j += 1
                self.__window.refresh()
                time.sleep(0.05)

        # elf.__window.refresh()
        self.__music_thread.terminate()