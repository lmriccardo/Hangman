from typing import List
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
        self.__game_settings = GameSetting()
        self.__game_status = GameStatus(settings=self.__game_settings)  # The status of the game

        self.__gwin_w, self.__gwin_h = curses.COLS - 2, curses.LINES - 21
        self.__gwin_x, self.__gwin_y = 1, 21

        # Window and paddings
        self.__window = None
        self.__hangman_pad = None
        self.__game_setting_pad = None
        self.__query_game_pad = None
        self.__description_diff_game_pad = None
        self.__game_status_pad = None
        self.__game_log_pad = None
        self.__game_word_pad = None

        self.__log_messages: List[str] = []

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

    @property
    def game_settings(self) -> GameSetting:
        """ Return the game setting object """
        return self.__game_settings

    @property
    def game_status(self) -> GameStatus:
        """ Return the status of the game """
        return self.__game_status

    @property
    def game_status_pad(self):
        """ Return the pad of the game status """
        return self.__game_status_pad

    @game_status_pad.setter
    def game_status_pad(self, new_value) -> None:
        """ Set the value for the attribute game_status_pad """
        self.__game_status_pad = new_value

    @property
    def game_log_pad(self):
        """ Return the log pad of the game """
        return self.__game_log_pad

    @game_log_pad.setter
    def game_log_pad(self, new_value) -> None:
        """ Set a new value for the attribute game_log_pad """
        self.__game_log_pad = new_value

    @property
    def game_word_pad(self):
        """ Return the pad in which insert the word """
        return self.__game_word_pad

    @game_word_pad.setter
    def game_word_pad(self, new_value) -> None:
        """ Set a new value for the attribute game_word_pad """
        self.__game_word_pad = new_value

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
            0, 3, "Hangman Game",
            Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE
        )

        game_window.noutrefresh()

        return game_window

    def add_query_game(self) -> curses.window:
        """ Ask the user if he is ready to start the game and ask also the difficulty """
        ask_pad = curses.newpad(100, self.__gwin_w)
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
        self.__description_diff_game_pad = curses.newpad(100, self.__gwin_w)
        while True:
            try:

                key = stdscr.getkey()

                # If the user has pressed ENTER, return the current difficulty
                if key == "\n":
                    self.clear_select_diff()
                    return difficulties[current_diff_idx]

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

                    diff_infos = Messages.INFO_DIFFICULTY
                    tmp_game_settings = GameSetting(difficulties[current_diff_idx])
                    w_len = tmp_game_settings.get_word_lenght()
                    n_hint = tmp_game_settings.get_number_of_hints()
                    formatting_value = (
                        (tmp_game_settings.get_intro(), tmp_game_settings.get_game_difficulty()),
                        (tmp_game_settings.get_max_time_per_round(),),
                        (tmp_game_settings.get_total_round_number(), tmp_game_settings.get_max_round_score()),
                        (", ".join(list(map(str, range(w_len[0], w_len[1] + 1)))), tmp_game_settings.get_penalty()),
                        (),
                        (", ".join(list(map(str, range(n_hint[0], n_hint[1] + 1)))), tmp_game_settings.get_hint_penalty()),
                        (),
                        ()
                    )

                    y, x = self.__gwin_y + 2, (self.__gwin_w - len(Messages.ASK_DIFFICULTY)) // 2
                    self.__query_game_pad.refresh(0, 0, y, x, y + 2, x + len(Messages.ASK_DIFFICULTY))

                    self.__description_diff_game_pad.erase()
                    for i, current_info in enumerate(diff_infos):
                        formatted_info = current_info
                        if formatting_value[i] != ():
                            formatted_info = formatted_info.format(*list(formatting_value[i]))

                        self.__description_diff_game_pad.addstr(i, 0, formatted_info, curses.A_BOLD)

                    # 97 is the maximum length of the maximum description line upon all descrs.
                    descr_pos_y, descr_pos_x = y + 10, (curses.COLS - 1 - 97) // 2
                    descr_pos_by, descr_pos_bx = descr_pos_y + len(formatting_value), descr_pos_x + 97
                    self.__description_diff_game_pad.refresh(0, 0, descr_pos_y, descr_pos_x, descr_pos_by, descr_pos_bx)

            except curses.error:
                ...

    def update_window_title(self) -> None:
        """ simply update the title of the window with the right difficulty """
        self.__window.addstr(
            0, 3, f"Hangman Game - {self.__game_settings.get_game_difficulty()} Mode - <1 Use Hint> - <CTRL-c To quit the game>",
            Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE
        )
        self.__window.noutrefresh()

    def clear_select_diff(self) -> None:
        """ Clear and delete the pads used for the diffculty selection """
        self.__query_game_pad.clear()
        self.__description_diff_game_pad.clear()

        upper_left_y, upper_left_x = self.__gwin_y + 1, self.__gwin_x + 1
        botton_right, botton_right_x = self.__gwin_y + self.__gwin_h - 3, self.__gwin_x + self.__gwin_w - 2
        self.__description_diff_game_pad.refresh(0, 0, upper_left_y, upper_left_x, botton_right, botton_right_x)
        self.__query_game_pad.refresh(0, 0, upper_left_y, upper_left_x, botton_right, botton_right_x)
        del self.__description_diff_game_pad
        del self.__query_game_pad

    def add_hangman_pad(self) -> curses.window:
        """ Add the pad for the hangman """
        hangman_pad = curses.newpad(100, 100)
        hangman_pad.nodelay(True)
        hangman_pad.clear()
        hangman_pad.addstr(AsciiArt.HANGMAN.format(
        	head="", larm="", body="",
        	rarm="", lleg="", rleg="",
        	lfoot="", rfoot=""
        ), curses.A_BOLD)
        hangman_pad.noutrefresh(0, 0, self.__gwin_y + 4, self.__gwin_x + 5, self.__gwin_y + 15, self.__gwin_x + 23)

        return hangman_pad

    def update_hangman(self, body_dict: Dict[str, str]) -> None:
        """
        Update the hangman inserting the part of the body specified in the input paramter kargs.
        So we have a dictionary of parameter that will be by default
        {
            "head" : "",
            "larm" : "",
            "body" : "",
            "rarm" : "",
            "lleg" : "",
            "rleg" : "",
            "lfoot": "",
            "rfoot": ""
        }
        """
        self.__hangman_pad.clear()
        self.__hangman_pad.addstr(AsciiArt.HANGMAN.format(
            head=body_dict["head"], larm=body_dict["larm"], body=body_dict["body"],
            rarm=body_dict["rarm"], lleg=body_dict["lleg"], rleg=body_dict["rleg"],
            lfoot=body_dict["lfoot"], rfoot=body_dict["rfoot"]
        ), curses.A_BOLD)
        self.__hangman_pad.noutrefresh(0, 0, self.__gwin_y + 4, self.__gwin_x + 5, self.__gwin_y + 15, self.__gwin_x + 23)

    @staticmethod
    def update_body_dict(body_dict: Dict[str, str], current_wrong_try: int, is_veryhard: bool) -> None:
        """ Update the body dict """
        if current_wrong_try == 1:
            body_dict["head"] = AsciiArt.HANGMAN_HEAD
            if is_veryhard:
                body_dict["body"] = AsciiArt.HANGMAN_BODY
        elif current_wrong_try == 2 and not is_veryhard:
            body_dict["body"] = AsciiArt.HANGMAN_BODY
        elif current_wrong_try == 3:
            body_dict["rarm"] = AsciiArt.HANGMAN_RIGHT_ARM
            if is_veryhard:
                body_dict["larm"] = AsciiArt.HANGMAN_LEFT_ARM
        elif current_wrong_try == 4 and not is_veryhard:
            body_dict["larm"] = AsciiArt.HANGMAN_LEFT_ARM
        elif current_wrong_try == 5:
            body_dict["rleg"] = AsciiArt.HANGMAN_RIGHT_LEG
            if is_veryhard:
                body_dict["lleg"] = AsciiArt.HANGMAN_LEFT_LEG
        elif current_wrong_try == 6 and not is_veryhard:
            body_dict["lleg"] = AsciiArt.HANGMAN_LEFT_LEG
        elif current_wrong_try == 7:
            body_dict["rfoot"] = AsciiArt.HANGMAN_FOOT
            if is_veryhard:
                body_dict["lfoot"] = AsciiArt.HANGMAN_FOOT
        elif current_wrong_try == 8 and not is_veryhard:
            body_dict["lfoot"] = AsciiArt.HANGMAN_FOOT

    def add_game_setting_pad(self) -> curses.window:
        """ Add the pad for displaying the game settings """
        settings_pad = curses.newpad(100, 100)
        settings_pad.nodelay(True)
        rectangle(self.__window, 4, self.__gwin_w // 2 + 27, 14, self.__gwin_w - 7)
        self.__window.addstr(4, self.__gwin_w // 2 + 29, "GAME SETTINGS", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
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

        settings_pad.noutrefresh(0, 0, self.__gwin_y + 5, self.__gwin_w // 2 + 31, self.__gwin_y + 12, self.__gwin_w - 8)

        return settings_pad

    def add_game_status_pad(self) -> curses.window:
        """ Add the pad for displaying the current status of the game """
        game_status_pad = curses.newpad(100, 100)
        game_status_pad.nodelay(True)
        rectangle(self.__window, 19, self.__gwin_w // 2 + 27, 28, self.__gwin_w - 7)
        self.__window.addstr(19, self.__gwin_w // 2 + 29, "GAME STATUS", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        self.__window.noutrefresh()

        return game_status_pad

    def update_status(self) -> None:
        """ Update the status of the game_status_pad adding the new value """
        current_round     = self.__game_status.round
        n_guessed_letters = self.__game_status.number_of_guessed_letters
        n_wrong_try       = self.__game_status.number_of_wrong_letters
        word_len          = self.__game_status.len_current_word
        n_used_hints      = self.__game_status.number_of_used_hints
        current_score     = self.__game_status.score

        self.__game_status_pad.clear()
        self.__game_status_pad.addstr(0, 2, f"CURRENT ROUND: {current_round}")
        self.__game_status_pad.addstr(1, 2, f"NUMBER OF GUESSED LETTERS: {n_guessed_letters}")
        self.__game_status_pad.addstr(2, 2, f"NUMBER OF WRONG TRY: {n_wrong_try}")
        self.__game_status_pad.addstr(3, 2, f"CURRENT WORD LENGTH: {word_len}")
        self.__game_status_pad.addstr(4, 2, f"NUMBER OF USED HINTS: {n_used_hints}")
        self.__game_status_pad.addstr(5, 2, f"CURRENT TOTAL SCORE: {current_score}")

        self.__game_status_pad.noutrefresh(0, 0, self.__gwin_y + 21, self.__gwin_w // 2 + 29, self.__gwin_y + 27, self.__gwin_w - 8)

    def add_log_pad(self) -> curses.window:
        """ Add the pad for logging what the user has done """
        log_pad = curses.newpad(100, 100)
        log_pad.nodelay(True)
        rectangle(self.__window, 19, 4, 28, self.__gwin_w // 2 + 20)
        self.__window.addstr(19, 6, "GAME LOG", Colors.return_pair_for_index(Colors.TITLE[1]) | curses.A_UNDERLINE)
        self.__window.noutrefresh()

        return log_pad

    def write_log(self, message: str, insert: str) -> None:
        """
        Write a log in the log pad

        :param message: the message (see src.util.config.LogMessages)
        :param insert: The string that complete the message (by formatting)
        :return: None
        """
        log_message = message % insert
        self.__log_messages.append(log_message)

        starting_point = len(self.__log_messages) - 6 if len(self.__log_messages) > 6 else 0
        self.__game_log_pad.addstr(len(self.__log_messages) - 1, 0, log_message, curses.A_BOLD)

        self.__game_log_pad.refresh(starting_point, 0, self.__gwin_y + 21, 7, self.__gwin_y + 26, self.__gwin_w // 2 + 20)

    @staticmethod
    def add_word_pad() -> curses.window:
        """ Add the pad for the word to guess """
        word_pad = curses.newpad(100, 100)
        word_pad.nodelay(True)
        return word_pad

    def update_word_pad(self, reset_cursor: bool = False, default_lett: Dict[int, str] = None, cursor_position: int = None) -> None:
        """
        Update with the new word

        :param reset_cursor: True if we want that the cursor go back to the start of the word
        :param default_lett: A dictionary containing default value for some position of the word. Can be used to indicate an update
        :param cursor_position: An integer representing the position of the cursor in the word
        :return: None
        """
        # Add the word
        self.__game_word_pad.clear()
        pos_y = self.__gwin_y + 15 - 15//2
        pos_x = self.__gwin_x + 35
        for i, state in enumerate(self.__game_status.word_state):
            current_state = state
            if default_lett is not None and i in default_lett:
                current_state = default_lett[i]

            self.__game_word_pad.addstr(0, 3 * i, current_state.upper(), curses.A_BOLD | curses.A_UNDERLINE)

        if cursor_position is not None:
            self.__game_word_pad.move(0, cursor_position)

        if reset_cursor:
            self.__game_word_pad.move(0, 0)

        self.__game_word_pad.noutrefresh(0, 0, pos_y, pos_x, pos_y + 1, pos_x + self.__game_status.len_current_word * 3)

    def clear_word_pad(self) -> None:
        """ Clear the pad of the word """
        pos_x = self.__gwin_x + 35
        pos_y = self.__gwin_y + 15 - 15 // 2
        current_word_len = self.__game_status.len_current_word
        self.__game_word_pad.clear()
        self.__game_word_pad.noutrefresh(0, 0, pos_y, pos_x, pos_y + 1, pos_x + current_word_len * 3)

    def write_guess_letter(self, current_pos: int, key: str) -> None:
        """
        Write a letter in the current position

        :param current_pos: the current position of the cursor WRT the word
        :param key: the pressed key
        :return: None
        """
        # First clear the pad
        self.clear_word_pad()

        # Then update the state and rewrite
        self.__game_status.update_word_state(current_pos, key)
        current_state_dict: Dict[int, str] = {idx : x for idx, x in enumerate(self.__game_status.word_state) if x != " "}
        self.update_word_pad(default_lett=current_state_dict, cursor_position=current_pos * 3)

    def move_cursor(self, position: int) -> None:
        """ Move the cursor in the window word pad """
        pos_x = self.__gwin_x + 35
        pos_y = self.__gwin_y + 15 - 15 // 2
        self.__game_word_pad.move(0, position * 3)
        self.__game_word_pad.noutrefresh(0, 0, pos_y, pos_x, pos_y + 1, pos_x + self.__game_status.len_current_word * 3)