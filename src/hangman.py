from src.words.wordoracle import WordOracle
from typing import Dict
from src.button import Button
from src.conductor import Conductor
from pygame.locals import *
import os.path as osp
import pygame
import sys

# CONSTANTS
PATH_SPLITTER = "\\" if sys.platform == "win32" else "/"
ASSETS_DIRECTORY = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-1]), "assets")
MUSIC_DIRECTORY = osp.join(PATH_SPLITTER.join(__file__.split(PATH_SPLITTER)[:-1]), "music")


class SpecialKeywordBtn:
    ESC_BUTTON = "\x1b"


class Hangman:
    def __init__(self) -> None:
        """ The init method """
        self.__running: bool = False                          # True if the App is running, False otherwise
        self.__size = self.__width, self.__height = 1000, 500  # The size of the window
        self.__display_surf: pygame.Surface = None            # The surface of the game
        self.__word_generator: WordOracle = WordOracle()      # The word generator

        self.__wallpaper = pygame.transform.scale(pygame.image.load(osp.join(ASSETS_DIRECTORY, "background/sfondo.png")), (1000, 500))        # Wallpaper
        self.__hangman_lazo = pygame.transform.scale(pygame.image.load(osp.join(ASSETS_DIRECTORY, "background/laccio.png")), (225, 225))      # The lazo for the hangman
        self.__text_box = pygame.transform.scale(pygame.image.load(osp.join(ASSETS_DIRECTORY, "game/text_box.png")), (60, 50))                # The assert for the letter box

        # Set the conductor for the game
        self.__conductor = Conductor()

        self.__start_button = Button(200, 100, osp.join(ASSETS_DIRECTORY, "buttons/start_button.png"))  # The start button
        self.__pause_button = Button(200, 100, osp.join(ASSETS_DIRECTORY, "buttons/pause_button.png"))  # The pause button
        self.__stop_button  = Button(200, 100, osp.join(ASSETS_DIRECTORY, "buttons/stop_button.png"))   # The stop button
        self.__button_dict: Dict[str, Button] = {
            "start" : self.__start_button,
            "pause" : self.__pause_button,
            "stop"  : self.__stop_button
        }

        self.__wallpaper_basex: int = 0                 # The base position of the wallpaper
        self.__lazo_basex, self.__lazo_basey = 50, 200  # Position of the hangman
        self.__fps: int = 10                            # Frame per seconds

        self.__is_correct: bool = False    # Check if the word inserted by the user is corrected or not
        self.__len_inserted_char: int = 0  # How many char has inserted the user
        self.__cnt_ended_play: int = 0     # Number of ended play-set
        self.__current_play: int = 0       # Current play-set

        self.__timestep: int = 0  # game's timestep. It is updated every time the player click on the cordinator's msg box

    def _on_init(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Hangman Game')

        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.__wallpaper.convert_alpha()
        self.__hangman_lazo.convert_alpha()
        self.__text_box.convert_alpha()
        self.__conductor.convert_alpha()

        # Correct alpha
        self.__start_button.convert_alpha()
        self.__pause_button.convert_alpha()
        self.__stop_button.convert_alpha()

        # Set correct surface
        self.__start_button.surface = self.__display_surf
        self.__pause_button.surface = self.__display_surf
        self.__stop_button.surface  = self.__display_surf
        self.__conductor.surface    = self.__display_surf

        self.__running = True

        self._draw_wallpaper()
        self._draw_btn(target_button="start")

        try:
            pygame.mixer.music.load(osp.join(MUSIC_DIRECTORY, "scifi.mp3"))
        except FileNotFoundError as fnfe:
            print(fnfe)

    def _draw_wallpaper(self) -> None:
        relative_x = self.__wallpaper_basex % self.__wallpaper.get_rect().width
        self.__display_surf.blit(self.__wallpaper, (relative_x - self.__wallpaper.get_rect().width, 0))

        if relative_x < 640:
            self.__display_surf.blit(self.__wallpaper, (relative_x, 0))

        self.__wallpaper_basex -= 1

    def _draw_lazo(self) -> None:
        self.__display_surf.blit(self.__hangman_lazo, (self.__lazo_basex, self.__lazo_basey))

    def _draw_btn(self, target_button: str) -> None:
        button: Button = self.__button_dict[target_button]
        button.blit(
            (self.__width - button.get_width()) // 2,
            (self.__height - button.get_height()) // 2
        )

    def _draw_lett_box(self, w_len: int) -> None:
        tb_w, tb_h = self.__text_box.get_width(), self.__text_box.get_height()
        start_pos_x, start_pos_y  = 100, 50
        epsilon = 1.15

        for i in range(w_len):
            self.__display_surf.blit(self.__text_box, (start_pos_x + i * epsilon * tb_w, start_pos_y))

    def _draw_conductor(self) -> None:
        self.__conductor.blit(cond_pos=(800, 320), msg_pos=(500, 160))

    def _update_pygame(self) -> None:
        pygame.display.update()
        pygame.time.Clock().tick(self.__fps)

    def _on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__start_button.clicked:
                self.__conductor.check_clicked(event)

            self.__start_button.check_click(event, click_one_time=True)

            # This is useful to avoid to be able to activate the pause mode
            # simply clicking with the mouse in the rectangle of the pause button
            if not self.__pause_button.clicked:
                tmp = self.__pause_button.clicked
                self.__pause_button.check_click(event)
                self.__pause_button.clicked = tmp
            else:
                self.__pause_button.check_click(event)

        if event.type == pygame.KEYDOWN:
            if event.__dict__["unicode"] == SpecialKeywordBtn.ESC_BUTTON and not self.__pause_button.clicked:
                self.__pause_button.clicked = True

    def on_execute(self) -> None:
        self._on_init()
        pygame.mixer.music.play(loops=-1, fade_ms=5000)
        word = None

        while self.__running:
            for event in pygame.event.get():
                self._on_event(event)

            if self.__current_play == self.__cnt_ended_play:
                word: str = self.__word_generator.get_word(n_times=1, change_length=True)
                self.__current_play += 1
                self.__is_correct = False
                # TODO: Do other things, like clear the board and the inserted char

            self._draw_wallpaper()

            if self.__start_button.clicked and not self.__pause_button.clicked:
                self._draw_lazo()
                self._draw_lett_box(w_len=len(word))
                self._draw_conductor()
                pygame.mixer.music.unpause()

            if not self.__start_button.clicked and not self.__pause_button.clicked:
                self._draw_btn(target_button="start")

            if self.__pause_button.clicked:
                self._draw_btn(target_button="pause")
                pygame.mixer.music.pause()

            self._update_pygame()

        pygame.quit()



if __name__ == '__main__':
    hm = Hangman()
    hm.on_execute()