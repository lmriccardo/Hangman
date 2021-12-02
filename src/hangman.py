from src.conductor.conductor import Conductor
from src.word.oracle import WordOracle
from src.game_state import GameStatus
from src.util.config import *
import curses


class TerminalHangman:
	def __init__(self, stdscr: curses.window) -> None:
		""" The init method """
		self.__stdscr = stdscr  # The standard screen for curses
		self.__stdscr.nodelay(True)

		# Setupping colors
		Colors.setup_colors()

		self.__word_generator = WordOracle()                    # The word generator oracle
		self.__conductor      = Conductor()                     # The conductor of the game
		self.__game_status    = GameStatus(round=0, word="")    # The status of the game

	def __show_title(self) -> None:
		""" Show the title of the game """
		self.__stdscr.addstr(1, 0, AsciiArt.TITLE, Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_BOLD)
		self.__stdscr.refresh()

	def __show_conductor(self) -> None:
		""" Show the conductor """
		conductor_window = Conductor.initialize_container(self.__stdscr)

		# Show conductor
		self.__conductor.print(conductor_window, section="START GAME")
		conductor_window.refresh()

		conductor_pad = self.__conductor.add_condactor_art()
		conductor_pad.refresh(0, 0, 12, curses.COLS - 30, 17, curses.COLS - 9)

	def _start_game(self) -> None:
		""" Start the game """
		self.__stdscr.clear()

		# Let's show the game's title
		self.__show_title()

		# Let's show the conductor
		self.__show_conductor()

		# show hangman
		self.__stdscr.addstr(21, 0, AsciiArt.HANGMAN.format(
			head=AsciiArt.HANGMAN_HEAD, larm=AsciiArt.HANGMAN_LEFT_ARM, body=AsciiArt.HANGMAN_BODY,
			rarm=AsciiArt.HANGMAN_RIGHT_ARM, lleg=AsciiArt.HANGMAN_LEFT_LEG, rleg=AsciiArt.HANGMAN_RIGHT_LEG,
			lfoot=AsciiArt.HANGMAN_FOOT, rfoot=AsciiArt.HANGMAN_FOOT
		))

		while True:
			try:
				key = self.__stdscr.getkey()
				self.__stdscr.addstr(30, 30, key)

				# If the user press ESC then quit
				if key == '\x1b':
					break

			except (KeyboardInterrupt, EOFError):
				sys.exit(0)
			except curses.error:
				...

	def run(self) -> None:
		""" Run the game """
		# Start the game
		self._start_game()


def main(stdscr) -> None:
	t = TerminalHangman(stdscr)
	t.run()


if __name__ == "__main__":
	curses.wrapper(main)
