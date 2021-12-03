import threading
import time

from src.conductor.conductor import Conductor
from src.word.oracle import WordOracle
from src.game_state import GameStatus
from src.util.config import *
import curses
import pydub
import pydub.playback as playbck


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

		# Get the background music
		self.__background_music = pydub.AudioSegment.from_mp3(System.SCIFI_MUSIC)
		self.__background_music -= 20
		self.__bckgrd_music_thread = threading.Thread(target=playbck.play, args=(self.__background_music,))

	def __show_title(self) -> None:
		""" Show the title of the game """
		# I wanna put the title at the center of the screen
		# I have to get the number of colums of the screen
		screen_ncols: int = curses.COLS - 1

		# Then, I have to take the length of the title (just the first row)
		title_len: int = len(AsciiArt.TITLE.split("\n")[0])

		# Then, take the middle point
		position: int = (screen_ncols - title_len) // 2

		# Refactor the title
		title: str = "\n".join([" " * position + x for x in AsciiArt.TITLE.split("\n")])

		self.__stdscr.addstr(2, 0, title, Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_BOLD)
		self.__stdscr.refresh()

	def __show_conductor(self) -> None:
		""" Show the conductor """
		# Initialize the conductor window
		conductor_window = Conductor.initialize_container(self.__stdscr)

		# Create the pad in which insert the ASCII Art of the conductor
		self.__conductor.add_condactor_art()

		# Update the window
		curses.doupdate()

		time.sleep(0.5)

		# Print the introduction from the Conductor
		self.__conductor.print(conductor_window, section="START GAME")

	def _start_game(self) -> None:
		""" Start the game """
		try:
			# Start the music
			self.__bckgrd_music_thread.start()

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
		except (KeyboardInterrupt, EOFError):
			sys.exit(0)

	def run(self) -> None:
		""" Run the game """
		# Start the game
		self._start_game()


def main(stdscr) -> None:
	t = TerminalHangman(stdscr)
	t.run()


if __name__ == "__main__":
	curses.wrapper(main)
