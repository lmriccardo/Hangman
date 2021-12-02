from src.conductor.conductor import Conductor
from src.word.oracle import WordOracle
from src.game_state import GameStatus
from src.util.config import *
import curses


class TerminalHangman:
    def __init__(self, stdscr: curses.window) -> None:
        """ The init method """
        self.__stdscr = stdscr  # The standard screen for curses

        # Setupping colors
        Colors.setup_colors()

        self.__word_generator = WordOracle()                    # The word generator oracle
        self.__conductor      = Conductor()                     # The conductor of the game
        self.__game_status    = GameStatus(round=0, word="")    # The status of the game

    def __show_title(self) -> None:
        """ Show the title of the game """
        # curses.init_pair(1, Colors.TITLE[0], curses.COLOR_BLACK)
        self.__stdscr.addstr(0, 0, AsciiArt.TITLE, Colors.return_pair_for_index(1))

    def _start_game(self) -> None:
        """ Start the game """
        self.__stdscr.clear()

        # Let's show the game's title
        self.__show_title()

        # Show conductor
        self.__conductor.print(self.__stdscr, section="START GAME")

        # show hangman
        self.__stdscr.addstr(19, 0, AsciiArt.HANGMAN.format(
            head=AsciiArt.HANGMAN_HEAD, larm=AsciiArt.HANGMAN_LEFT_ARM, body=AsciiArt.HANGMAN_BODY,
            rarm=AsciiArt.HANGMAN_RIGHT_ARM, lleg=AsciiArt.HANGMAN_LEFT_LEG, rleg=AsciiArt.HANGMAN_RIGHT_LEG,
            lfoot=AsciiArt.HANGMAN_FOOT, rfoot=AsciiArt.HANGMAN_FOOT
        ))

        self.__stdscr.getch()

        # Refresh the screen
        self.__stdscr.refresh()

    def run(self) -> None:
        """ Run the game """
        # Start the game
        self._start_game()


def hangman(stdscr) -> None:
    t = TerminalHangman(stdscr)
    t.run()


if __name__ == "__main__":
    curses.wrapper(hangman)
