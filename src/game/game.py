from src.conductor.conductor import Conductor
from src.game.game_state import GameStatus
from src.util.config import *
import curses


class Game:
    """ The effective game object """
    def __init__(self, conductor: Conductor) -> None:
        """ The init method """
        self.__conductor = conductor  # The conductor object

        self.__gwin_w, self.__gwin_h = curses.COLS - 2, curses.LINES - 21
        self.__gwin_x, self.__gwin_y = 1, 21

        self.__game_status = GameStatus(round=0, word="")  # The status of the game
        self.__window = None

    @property
    def window(self):
        """ Return the window of the game """
        return self.__window

    @window.setter
    def window(self, new_value) -> None:
        """ Set the new value for the attribute window """
        self.__window = new_value

    def initialize_window(self) -> curses.window:
        """ Initialize the game creating the game window """
        game_window = curses.newwin(self.__gwin_h, self.__gwin_w, self.__gwin_y, self.__gwin_x)
        game_window.nodelay(True)
        game_window.clear()
        game_window.box()
        game_window.addstr(0, 3, "Hangman Game", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        game_window.noutrefresh()
        return game_window

    def add_hangman(self) -> None:
        """ Add the hangman """
        self.__window.addstr(2, 2, AsciiArt.HANGMAN.format(
        	head=AsciiArt.HANGMAN_HEAD, larm=AsciiArt.HANGMAN_LEFT_ARM, body=AsciiArt.HANGMAN_BODY,
        	rarm=AsciiArt.HANGMAN_RIGHT_ARM, lleg=AsciiArt.HANGMAN_LEFT_LEG, rleg=AsciiArt.HANGMAN_RIGHT_LEG,
        	lfoot=AsciiArt.HANGMAN_FOOT, rfoot=AsciiArt.HANGMAN_FOOT
        ), curses.A_BOLD)
        self.__window.noutrefresh()