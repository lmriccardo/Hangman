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

		self.__processes: List[multiprocessing.Process] = [self.__bckgrd_music_thread]

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
		conductor_window, conductor_pad = Conductor.initialize_container()
		self.__conductor.window = conductor_window
		self.__conductor.conductor_pad = conductor_pad

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

		ask_pad = self.__game.add_query_game()
		self.__game.query_game_pad = ask_pad

		curses.doupdate()

		diff = self.__game.get_difficulty(self.__stdscr)
		self.__game.game_settings.change_game_difficulty(diff)
		self.__game.update_window_title()

		game_hangman_pad = self.__game.add_hangman_pad()
		self.__game.hangman_pad = game_hangman_pad

		game_settings_pad = self.__game.add_game_setting_pad()
		self.__game.game_setting_pad = game_settings_pad

		game_status_pad = self.__game.add_game_status_pad()
		self.__game.game_status_pad = game_status_pad
		self.__game.update_status()

		game_log_pad = self.__game.add_log_pad()
		self.__game.game_log_pad = game_log_pad

		game_word_pad = self.__game.add_word_pad()
		self.__game.game_word_pad = game_word_pad

		curses.doupdate()

	def _start_game(self) -> None:
		""" Start the game """
		try:
			# Start the music
			# self.__bckgrd_music_thread.start()

			self.__stdscr.clear()

			# Let's show the game's title
			self.__show_title()

			# Let's show the conductor
			self.__show_conductor()

			# Let's introduce the game
			self.__show_game()

			# Start the game
			min_len_w, max_len_w = self.__game.game_settings.get_word_lenght()
			n_round = self.__game.game_settings.get_total_round_number()
			for current_word in self.__word_generator.get_word(n_times=n_round, min_length=min_len_w, max_length=max_len_w):
				# Update the state
				self.__game.game_status.next_round(word=current_word)
				self.__game.update_status()
				self.__game.update_word_pad(reset_cursor=True)
				curses.doupdate()

				current_position = 0
				tmp_position = current_position

				key = None
				while key != "\n":
					try:
						key = self.__stdscr.getkey()
						# If it is a normal char then write it (temp)
						if key in Char.NORMAL_CHAR and self.__game.game_status.word_state[current_position] == " ":
							self.__game.write_log(message=LogMessages.CHAR_INSERTION, insert=key)
							if self.__game.game_status.word[current_position] == key:
								self.__game.write_guess_letter(current_pos=current_position, key=key)
								self.__game.write_log(message=LogMessages.RIGTH_GUESS, insert=key)
							else:
								self.__conductor.print(section="ON ERROR")
								self.__game.write_log(message=LogMessages.WRONG_GUESS, insert=key)

						# Otherwise could be an arrows
						if key == "KEY_LEFT" and current_position > 0:
							tmp_position -= 1
						elif key == "KEY_RIGHT" and current_position < len(current_word) - 1:
							tmp_position += 1

						if tmp_position != current_position:
							current_position = tmp_position
							self.__game.write_log(message=LogMessages.BOX_SELECTION, insert=str(current_position))
							self.__game.move_cursor(current_position)

						# Else use hint
						if key == "1":
							if self.__game.game_status.number_of_used_hints < self.__game.game_settings.map_wordlen_maxhints(wordlen=len(current_word)):
								self.__game.game_status.number_of_used_hints += 1
								self.__game.write_guess_letter(current_pos=current_position, key=self.__game.game_status.word[current_position])
								self.__game.write_log(message=LogMessages.HINT_USED, insert=str(self.__game.game_status.number_of_used_hints))
								self.__game.update_status()
							else:
								self.__conductor.print(section="NO HINT")

						curses.doupdate()
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
			... # process.terminate()

		# Return to the main screen settings
		curses.endwin()


def main(stdscr) -> None:
	t = TerminalHangman(stdscr)
	t.run()


if __name__ == "__main__":
	curses.wrapper(main)
