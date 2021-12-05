from src.conductor.conductor import Conductor
from src.game.game_state import GameStatus, GameSetting
from src.util.config import *
import curses
from curses.textpad import rectangle


class Game:
    """ The effective game object """
    def __init__(self, conductor: Conductor) -> None:
        """ The init method """
        self.__conductor = conductor  # The conductor object
        self.__game_status = GameStatus(round=0, word="")  # The status of the game
        self.__game_settings = GameSetting()

        self.__gwin_w, self.__gwin_h = curses.COLS - 2, curses.LINES - 21
        self.__gwin_x, self.__gwin_y = 1, 21

        # Window and paddings
        self.__window = None
        self.__hangman_pad = None
        self.__game_setting_pad = None
        self.__query_game_pad = None

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

    @property
    def query_game_pad(self):
        """ Return the pad of the ask difficulty query """
        return self.__query_game_pad

    @query_game_pad.setter
    def query_game_pad(self, new_value) -> None:
        """ Set a new value for the attribute query_game_pad """
        self.__query_game_pad = new_value

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

        game_window.addstr(
            0, 3, f"Hangman Game - {self.__game_settings.get_game_difficulty()} Mode",
            Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE
        )

        game_window.noutrefresh()

        return game_window

    def add_query_game(self) -> curses.window:
        """ Ask the user if he is ready to start the game and ask also the difficulty """
        ask_pad = curses.newpad(100, 100)
        ask_pad.clear()
        ask_pad.nodelay(True)

        difficulties = ["Easy", "Medium", "Hard", "Very Hard"]
        ask_pad.addstr(0, 0, Messages.ASK_DIFFICULTY + ":", curses.A_BOLD)

        initial_pos = pos_x = (len(Messages.ASK_DIFFICULTY) - len("   ".join(difficulties))) // 2
        for i, diff in enumerate(difficulties):
            if i == 0:
                ask_pad.attron(curses.A_BLINK | curses.A_REVERSE)

            ask_pad.addstr(2, pos_x, diff.upper())

            if i == 0:
                ask_pad.attroff(curses.A_BLINK | curses.A_REVERSE)

            pos_x += len(diff) + 3

        ask_pad.move(2, initial_pos - 1)

        y, x = self.__gwin_y + 2, (self.__gwin_w - len(Messages.ASK_DIFFICULTY)) // 2
        ask_pad.noutrefresh(0, 0, y, x, y + 2, x + len(Messages.ASK_DIFFICULTY))

        return ask_pad

    def get_difficulty(self, stdscr: curses.window) -> str:
        """ Get the user input to choose the difficulty """
        difficulties = ["Easy", "Medium", "Hard", "Very Hard"]
        current_diff_idx = previous_diff_idx = 0
        current_position_x = previous_position_x = (len(Messages.ASK_DIFFICULTY) - len("   ".join(difficulties))) // 2
        while True:
            try:

                key = stdscr.getkey()

                # If the user has pressed ENTER, return the current difficulty
                if key == "\n":
                    return difficulties[current_diff_idx].upper()

                previous_diff_idx = current_diff_idx
                previous_position_x = current_position_x

                if key == "KEY_LEFT" and current_diff_idx > 0:
                    current_diff_idx -= 1
                    current_position_x -= (3 + len(difficulties[current_diff_idx]))
                elif key == "KEY_RIGHT" and current_diff_idx < len(difficulties) - 1:
                    current_diff_idx += 1
                    current_position_x += len(difficulties[previous_diff_idx]) + 3

                # We have to reverse and blink the current diff, and unset the attr
                # of the previous selected difficulty
                if previous_diff_idx != current_diff_idx:
                    # Set the attribute
                    self.__query_game_pad.addstr(2, current_position_x, difficulties[current_diff_idx].upper(),
                                                 curses.A_BLINK | curses.A_REVERSE)
                    # Unset attribute
                    self.__query_game_pad.addstr(2, previous_position_x, difficulties[previous_diff_idx].upper())

                    y, x = self.__gwin_y + 2, (self.__gwin_w - len(Messages.ASK_DIFFICULTY)) // 2
                    self.__query_game_pad.refresh(0, 0, y, x, y + 2, x + len(Messages.ASK_DIFFICULTY))

            except curses.error:
                ...

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

    def add_game_setting_pad(self) -> curses.window:
        """ Add the pad for displaying the game settings """
        settings_pad = curses.newpad(100, 100)
        settings_pad.nodelay(True)
        rectangle(self.__window, 2, self.__gwin_w // 2, 12, self.__gwin_w - 7)
        self.__window.addstr(2, self.__gwin_w // 2 + 3, f"GAME SETTINGS", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        self.__window.noutrefresh()

        settings_pad.clear()

        # From sec to h::m::s
        hour   = self.__game_settings.get_max_time_per_round() // 3600
        minute = (self.__game_settings.get_max_time_per_round() % 3600) // 60
        second = self.__game_settings.get_max_time_per_round() % 60
        settings_pad.addstr(1, 0, f"{GameSettings.MAX_ROUND_TIME}: {hour}H:{minute}M:{second}S")
        settings_pad.addstr(2, 0, f"{GameSettings.TOT_ROUND_NUMBER}: {self.__game_settings.get_total_round_number()}")
        settings_pad.addstr(3, 0, f"{GameSettings.GAME_DIFFICULTY}: {self.__game_settings.get_game_difficulty()}")
        settings_pad.addstr(4, 0, f"{GameSettings.MAX_ROUND_SCORE}: {self.__game_settings.get_max_round_score()}")

        word_len_min, word_len_max = self.__game_settings.get_word_lenght()
        word_len_range = ', '.join(list(map(str, list(range(word_len_min, word_len_max + 1)))))
        settings_pad.addstr(5, 0, f"{GameSettings.WORD_LENGTH} Range: {word_len_range}")
        settings_pad.addstr(6, 0, f"{GameSettings.PENALTY}: {self.__game_settings.get_penalty()}")

        hint_num_min, hint_num_max = self.__game_settings.get_number_of_hints()
        hints_range = ', '.join(list(map(str, list(range(hint_num_min, hint_num_max + 1)))))
        settings_pad.addstr(7, 0, f"{GameSettings.HINT_NUMBER} Range: {hints_range}")
        settings_pad.addstr(8, 0, f"{GameSettings.HINT_PENALTY}: x{self.__game_settings.get_hint_penalty()}")

        settings_pad.noutrefresh(0, 0, self.__gwin_y + 3, self.__gwin_w // 2 + 4, self.__gwin_y + 10, self.__gwin_w - 8)

        return settings_pad