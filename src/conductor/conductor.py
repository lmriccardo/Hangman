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
        self.__msg_dict: Dict[str, Tuple[List[str], int]] = {  # Messages for each section of the conductor
            "START GAME"         : (list(Messages.START_GAME), Colors.return_pair_for_index(Colors.START_GAME[1])),
            "START ROUND"        : (list(Messages.START_ROUND), Colors.return_pair_for_index(Colors.START_ROUND[1])),
            "ON ERROR"           : (list(Messages.ON_ERROR), Colors.return_pair_for_index(Colors.ON_ERROR[1])),
            "NO HINT"            : (list(Messages.NO_HINT),  Colors.return_pair_for_index(Colors.NO_HINT[1])),
            "END POSITIVE ROUND" : (list(Messages.END_POSITIVE_ROUND), Colors.return_pair_for_index(Colors.END_POSITIVE_ROUND[1])),
            "END NEGATIVE ROUND" : (list(Messages.END_NEGATIVE_ROUND), Colors.return_pair_for_index(Colors.END_NEGATIVE_ROUND[1])),
            "END GAME"           : (list(Messages.END_GAME), Colors.return_pair_for_index(Colors.END_GAME[1]))
        }

        self.__window = None
        self.__conductor_pad = None

        # If there is at least a message in the pad
        self.__thereis_message: bool = False
        self.__messages_current_max_len: int = 0
        self.__messages_current_max_h: int = 0

        # Get the sound of the typewriter
        self.__type_writer_sound = pydub.AudioSegment.from_mp3(System.TYPEWRITER_MUSIC)[:-100]
        self.__type_writer_sound += self.__type_writer_sound * 6 + self.__type_writer_sound[:-1000]
        self.__type_writer_sound -= 30

    @property
    def window(self):
        """ Return the window of the conductor """
        return self.__window

    @window.setter
    def window(self, new_value) -> None:
        """ Set the new value for the attribute window """
        self.__window = new_value

    @property
    def conductor_pad(self):
        """ Return the pad where the conductor write messages """
        return self.__conductor_pad

    @conductor_pad.setter
    def conductor_pad(self, new_value) -> None:
        """ Set a new value for the attribute conductor_pad """
        self.__conductor_pad = new_value

    @staticmethod
    def initialize_container() -> Tuple[curses.window]:
        """ Initialize the new container for the conductor messages """
        y_postion = 2 + len(AsciiArt.TITLE.split("\n")) + 1 # The +2s are the padding
        conductor_window = curses.newwin(11, curses.COLS - 2, y_postion, 1)
        conductor_window.nodelay(True)
        conductor_window.box()
        conductor_window.addstr(0, 3, "Conductor", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        conductor_window.noutrefresh()

        conductor_pad = curses.newpad(100, 100)

        return conductor_window, conductor_pad

    @staticmethod
    def add_condactor_art() -> None:
        """ Add the Ascii Art of the conductor """
        conductor_pad = curses.newpad(100, 100)
        conductor_pad.clear()
        conductor_pad.addstr(AsciiArt.CONDUCTOR, curses.A_BOLD)
        conductor_pad.noutrefresh(0, 0, 13, curses.COLS - 30, 18, curses.COLS - 9)

    def print(self, section: str) -> None:
        """ Print the messages of the corresponding section """
        music_thread = multiprocessing.Process(target=playbck.play, args=(self.__type_writer_sound,))
        music_thread.start()
        lines, color = self.__msg_dict[section]
        y_postion = 2 + len(AsciiArt.TITLE.split("\n")) + 1
        max_len = 0
        max_heigth = 0

        # First clear
        if self.__thereis_message:
            self.__conductor_pad.clear()
            self.__conductor_pad.refresh(0, 0, y_postion + 2, 2, self.__messages_current_max_h, self.__messages_current_max_len + 1)

        for i, line in enumerate(lines):
            j = 3
            for char in line:
                self.__conductor_pad.addstr(i, j, char, color | curses.A_BOLD)
                j += 1
                if j > max_len:
                    max_len = j

                max_heigth = y_postion + 2 + i
                self.__conductor_pad.refresh(0, 0, y_postion + 2, 2, max_heigth, max_len + 1)
                time.sleep(0.005)

        self.__thereis_message = True
        self.__messages_current_max_len = max_len
        self.__messages_current_max_h = max_heigth

        music_thread.terminate()