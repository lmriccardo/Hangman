from src.conductor.conductor import Conductor
from src.game.game_state import GameStatus
from src.util.config import *
import curses


class Game:
    """ The effective game object """
    def __init__(self, conductor: Conductor) -> None:
        """ The init method """
        self.__conductor = conductor  # The conductor object
        self.__game_status = GameStatus(round=0, word="")  # The status of the game

        self.__gwin_w, self.__gwin_h = curses.COLS - 2, curses.LINES - 21
        self.__gwin_x, self.__gwin_y = 1, 21

        # Window and paddings
        self.__window = None
        self.__hangman_pad = None
        self.__game_setting_pad = None

    @property
    def window(self):
        """ Return the window of the game """
        return self.__window

    @window.setter
    def window(self, new_value) -> None:
        """ Set the new value for the attribute window """
        self.__window = new_value

    @property
    def hangman_pad(self):
        """ Return the hangman pad of the game """
        return self.__hangman_pad

    @hangman_pad.setter
    def hangman_pad(self, new_value) -> None:
        """ Set the new value for the attribute hangman_pad """
        self.__hangman_pad = new_value

    @property
    def game_setting_pad(self):
        """ Return the pad containing the setting of the game """
        return self.__game_setting_pad

    @game_setting_pad.setter
    def game_setting_pad(self, new_value) -> None:
        """ Set a new value to the attribute game_setting_pad """
        self.__game_setting_pad = new_value

    def initialize_window(self) -> curses.window:
        """ Initialize the game creating the game window """
        game_window = curses.newwin(self.__gwin_h - 1, self.__gwin_w, self.__gwin_y, self.__gwin_x)
        game_window.nodelay(True)
        game_window.clear()

        # color the border red
        color_pair = Colors.return_pair_for_index(Colors.GAME_BORDER_WIN[1])
        game_window.attron(color_pair)
        game_window.box()
        game_window.attroff(color_pair)

        game_window.addstr(0, 3, "Hangman Game", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        game_window.noutrefresh()

        return game_window

    def add_hangman_pad(self) -> curses.window:
        """ Add the pad for the hangman """
        hangman_pad = curses.newpad(100, 100)
        hangman_pad.nodelay(True)
        hangman_pad.clear()
        hangman_pad.addstr(AsciiArt.HANGMAN.format(
        	head=AsciiArt.HANGMAN_HEAD, larm=AsciiArt.HANGMAN_LEFT_ARM, body=AsciiArt.HANGMAN_BODY,
        	rarm=AsciiArt.HANGMAN_RIGHT_ARM, lleg=AsciiArt.HANGMAN_LEFT_LEG, rleg=AsciiArt.HANGMAN_RIGHT_LEG,
        	lfoot=AsciiArt.HANGMAN_FOOT, rfoot=AsciiArt.HANGMAN_FOOT
        ), curses.A_BOLD)
        hangman_pad.noutrefresh(0, 0, self.__gwin_y + 2, self.__gwin_x + 4, self.__gwin_y + 16, self.__gwin_x + 22)

        return hangman_pad