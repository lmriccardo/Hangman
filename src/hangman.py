import multiprocessing
import time
from typing import List
from src.conductor.conductor import Conductor
from src.word.oracle import WordOracle
from src.game.game import Game
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
		self.__game 		  = Game(self.__conductor)			# The game object

		# Get the background music
		self.__background_music = pydub.AudioSegment.from_mp3(System.SCIFI_MUSIC)
		self.__background_music -= 20
		self.__bckgrd_music_thread = multiprocessing.Process(target=playbck.play, args=(self.__background_music,))

		self.__processes: List[multiprocessing.Process] = [self.__bckgrd_music_thread, self.__conductor.music_thread]

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
		conductor_window = Conductor.initialize_container()
		self.__conductor.window = conductor_window

		# Create the pad in which insert the ASCII Art of the conductor
		self.__conductor.add_condactor_art()

		# Update the window
		curses.doupdate()

		time.sleep(0.5)

		# Print the introduction from the Conductor
		self.__conductor.print(section="START GAME")

	def __show_game(self) -> None:
		""" Show the game window """
		# Initialize the game window
		game_window = self.__game.initialize_window()
		self.__game.window = game_window

		curses.doupdate()

		game_hangman_pad = self.__game.add_hangman_pad()
		self.__game.hangman_pad = game_hangman_pad

		game_settings_pad = self.__game.add_game_setting_pad()
		self.__game.game_setting_pad = game_settings_pad

		curses.doupdate()

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

			# Let's introduce the game
			self.__show_game()

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
			self.terminate()

	def run(self) -> None:
		""" Run the game """
		# Start the game
		self._start_game()

	def terminate(self) -> None:
		""" Terminate all the secondary processes and return to the main window """
		# Kill processes
		for process in self.__processes:
			process.terminate()

		# Return to the main screen settings
		curses.endwin()


def main(stdscr) -> None:
	t = TerminalHangman(stdscr)
	t.run()


if __name__ == "__main__":
	curses.wrapper(main)
