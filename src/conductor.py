from typing import Tuple, List, Dict, Generator
import os.path as osp
import pygame
import sys
import os


# CONSTANTS
PATH_SPLITTER = "\\" if sys.platform == "win32" else "/"
ASSETS_DIRECTORY = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-1]), "assets")


class Message:

    SPECIAL_CHAR_MAPPING: Dict[str,str] = {
        "\\xc3\\xa8" : osp.join(ASSETS_DIRECTORY, "letters/special/letter_e_accentata.png"),
        "\\xc3\\xa0" : osp.join(ASSETS_DIRECTORY, "letters/special/letter_a_accentata.png"),
        "\\xc3\\xb2" : osp.join(ASSETS_DIRECTORY, "letters/special/letter_o_accentata.png"),
        "\\xc3\\xb9" : osp.join(ASSETS_DIRECTORY, "letters/special/letter_u_accentata.png"),
        ","          : osp.join(ASSETS_DIRECTORY, "letters/special/letter_virgola.png"),
        "'"          : osp.join(ASSETS_DIRECTORY, "letters/special/letter_apostrofo.png"),
        "!"          : osp.join(ASSETS_DIRECTORY, "letters/special/letter_puntoesclamativo.png"),
        "."          : osp.join(ASSETS_DIRECTORY, "letters/special/letter_punto.png"),
        "?"          : osp.join(ASSETS_DIRECTORY, "letters/special/letter_puntointerrogativo.png")
    }
    LOWER_CASE_MAPPING: Dict[str, str] = {chr(x) : osp.join(ASSETS_DIRECTORY, f"letters{PATH_SPLITTER}small{PATH_SPLITTER}letter_{chr(x)}_small.png") for x in range(ord("a"), ord("z") + 1)}
    UPPER_CASE_MAPPING: Dict[str, str] = {chr(x).upper() : osp.join(ASSETS_DIRECTORY, f"letters{PATH_SPLITTER}big{PATH_SPLITTER}letter_{chr(x)}.png") for x in range(ord("a"), ord("z") + 1)}
    NUMBER_MAPPING    : Dict[str, str] = {str(x) : osp.join(ASSETS_DIRECTORY, f"letters{PATH_SPLITTER}numbers{PATH_SPLITTER}{x}.png") for x in range(10)}

    LENGHT_SECTIONS: Dict[str, int] = {
        "start_game"         : 7,
        "start_round"        : 2,
        "on_error"           : 1,
        "end_positive_round" : 1,
        "end_negative_round" : 2,
        "end_game"           : 2
    }

    def __init__(self) -> None:
        """ An init method """
        self.__msgs_file = open(osp.join(ASSETS_DIRECTORY, "conductor/messages.txt"))

        self.__start_game: List[str] = []          # Messages when the game start
        self.__start_round: List[str] = []         # Messages when a new round start
        self.__on_error: List[str] = []            # Messages when an error occure
        self.__end_positive_round: List[str] = []  # Messages when a positive round end
        self.__end_negative_round: List[str] = []  # Messages when a negative round end
        self.__end_game: List[str] = []            # Messages when the game end

        self.__fullfil()

    def __fullfil(self) -> None:
        """ Fill the list for each section of the message file """
        start_game = start_round = on_error = end_positive_round = end_negative_round = end_game = False
        while line := self.__msgs_file.readline():
            if line.isupper():
                start_game         = line == "START GAME:\n"
                start_round        = line == "START ROUND:\n"
                on_error           = line == "ON ERROR:\n"
                end_positive_round = line == "END POSITIVE ROUND:\n"
                end_negative_round = line == "END WRONG ROUND:\n"
                end_game           = line == "END GAME:\n"
                continue

            if start_game and line != "\n": self.__start_game.append(line[2:-1])
            if start_round and line != "\n": self.__start_round.append(line[2:-1])
            if on_error and line != "\n": self.__on_error.append(line[2:-1])
            if end_positive_round and line != "\n": self.__end_positive_round.append(line[2:-1])
            if end_negative_round and line != "\n": self.__end_negative_round.append(line[2:-1])
            if end_game and line != "\n": self.__end_game.append(line[2:-1])

    def _get_mapping(self, char: str) -> str:
        """
        Return the abspath of the corresponding PNG image in the assets directory.
        Note that for special char such as è, à, ò or ù, it will return None since
        the length of the ASCII representation is different from the length of the classic one.
        :param char: the char that has to be checked
        :return: the abspath
        """
        mapping: str = None

        # If I have the space, simply return "space".
        # This will be interpreted as some padding when
        # drawing the phrase on the window
        if char == " ":
            mapping = "space"

        # Otherwise are letter or numbers
        if len(ascii(char)[1:-1]) == len(char):
            if char in self.LOWER_CASE_MAPPING:
                mapping = self.LOWER_CASE_MAPPING[char]
            if char in self.UPPER_CASE_MAPPING:
                mapping = self.UPPER_CASE_MAPPING[char]
            if char in self.NUMBER_MAPPING:
                mapping = self.NUMBER_MAPPING[char]
            if char in self.SPECIAL_CHAR_MAPPING:
                mapping = self.SPECIAL_CHAR_MAPPING[char]

        return mapping

    def generate_messages(self, section: str = "", line: int = 0) -> Generator:
        attribute: str = f"_Message__{section}"
        msg: str = self.__dict__[attribute][line]
        i = 0
        phrase: List[str] = []
        while i < len(msg):
            char = msg[i]
            mapping: str = self._get_mapping(char)
            i += 1

            # It the mapping return None, It means that is a special char either è,à,ò or ù.
            if not mapping:
                mapping = self.SPECIAL_CHAR_MAPPING[ascii(char)[1:-1] + ascii(msg[i])[1:-1]]
                i += 1

            phrase.append(mapping)
            yield phrase

    def get_len_section(self, section: str = "") -> int:
        """ Return the number of lines of a section in the message file """
        return len(self.__dict__[f"_Message__{section}"])


class Conductor:
    def __init__(self, target: pygame.Surface = None) -> None:
        """ An init method """
        self.__surface = target

        self.__conductor_size = self.__cw, self.__ch = 100, 100
        self.__msg_box_size   = self.__mw, self.__mh = 450, 350

        self.__cond_pos: Tuple[int, int] = None
        self.__msg_pos : Tuple[int, int] = None

        # load image
        self.__conductor = pygame.transform.scale(pygame.image.load(osp.join(ASSETS_DIRECTORY, "conductor/conductor.png")), self.__conductor_size)
        self.__msg_box = pygame.transform.scale(pygame.image.load(osp.join(ASSETS_DIRECTORY, "conductor/message_box.png")), self.__msg_box_size)

        # flip the message box
        self.__msg_box = pygame.transform.flip(self.__msg_box, 1, 0)

        # Load the message generator
        self.__message_generator = Message()
        self.__current_line: int = 0
        self.__current_section: str = "start_game"

    def convert_alpha(self) -> None:
        self.__conductor.convert_alpha()
        self.__msg_box.convert_alpha()

    @property
    def current_line(self) -> int:
        return self.__current_line

    @property
    def current_section(self) -> str:
        return self.__current_section

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @surface.setter
    def surface(self, new_surface: pygame.Surface) -> None:
        self.__surface = new_surface

    def blit(self, cond_pos: Tuple[int, int], msg_pos: Tuple[int, int]) -> None:
        self.__cond_pos = cond_pos
        self.__msg_pos  = msg_pos
        self.__surface.blit(self.__conductor, cond_pos)
        self.__surface.blit(self.__msg_box, msg_pos)

        self.blit_messages()

    def blit_messages(self) -> None:
        images: List[Tuple[pygame.Surface, int]] = []
        image_names: List[str] = []
        pos_x, pos_y = self.__msg_pos[0] + 30, 270

        for gen in self.__message_generator.generate_messages(section=self.__current_section, line=self.__current_line):
            if gen[-1] != "space":
                w, h = 7, 10
                if gen[-1].endswith("letter_i_small.png") or \
                        gen[-1].endswith("letter_l_small.png") or \
                        gen[-1].endswith("letter_virgola.png") or \
                        gen[-1].endswith("letter_apostrofo.png") or \
                        gen[-1].endswith("letter_puntoesclamativo.png"):
                    w = 2
                loaded_image = pygame.transform.scale(pygame.image.load(gen[-1]), (w, h))
                loaded_image.convert_alpha()
                images.append((loaded_image, loaded_image.get_width()))
            else:
                images.append((gen[-1], images[-1][0].get_width()))

            image_names.append(gen[-1])

            for idx, (image, _) in enumerate(images):
                if idx > 0:
                    prev_w = images[idx - 1][1]
                    prev_w += 0 if prev_w != 2 else 2
                    if image == "space":
                        pos_x += prev_w - 5
                        continue

                    if image_names[idx].endswith("letter_virgola.png"):
                        pos_y += 5
                        pos_x += prev_w + 2
                        self.__surface.blit(image, (pos_x, pos_y))
                        pos_y -= 5
                    elif image_names[idx].endswith("letter_apostrofo.png"):
                        pos_y -= 5
                        pos_x += prev_w + 2
                        self.__surface.blit(image, (pos_x, pos_y))
                        pos_y += 5
                    else:
                        pos_x += prev_w + 2
                        self.__surface.blit(image, (pos_x, pos_y))

                    continue

                self.__surface.blit(image, (pos_x, pos_y))

            pos_x, pos_y = self.__msg_pos[0] + 30, 270

    def check_clicked(self, event_mouse_click: pygame.event.Event) -> None:
        mouse_pos_down = event_mouse_click.__dict__["pos"]
        if self.__msg_box.get_rect(topleft=(self.__msg_pos[0], self.__msg_pos[1])).collidepoint(mouse_pos_down):
            self.__current_line += 1
            if self.__message_generator.LENGHT_SECTIONS[self.__current_section] == self.__current_line:
                index_current_section = list(self.__message_generator.LENGHT_SECTIONS.keys()).index(self.__current_section)
                self.__current_section = list(self.__message_generator.LENGHT_SECTIONS.keys())[index_current_section + 1]
                self.__current_line = 0