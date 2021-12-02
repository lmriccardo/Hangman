import pygame
from typing import Optional


class Button:
    def __init__(self, w: int, h: int, image_file: str, target: pygame.Surface = None) -> None:
        """ An init method """
        self.__button = pygame.transform.scale(pygame.image.load(image_file), (w, h))
        self.__surface = target
        self.__clicked = False
        self.__pos_x, self.__pos_y = 0, 0

    def convert_alpha(self) -> None:
        self.__button.convert_alpha()

    def get_width(self) -> int:
        return self.__button.get_width()

    def get_height(self) -> int:
        return self.__button.get_height()

    @property
    def surface(self) -> Optional[pygame.Surface]:
        return self.__surface

    @surface.setter
    def surface(self, new_surface) -> None:
        self.__surface = new_surface

    @property
    def clicked(self) -> bool:
        return self.__clicked

    @clicked.setter
    def clicked(self, new_value: bool) -> None:
        self.__clicked = new_value

    def check_click(self, event_button_down: pygame.event.Event, click_one_time: bool = False) -> None:
        """
        Check if the mouse position is in the correct rectangle of the button image. If it is
        then change the state of clicked in True or False. This depends also on the value of
        click_one_time. For example, in the game the start button must be pressed only one time
        (if obv we just have paused the game and not quitted it), while the pause button can be
        pressed more than one time since we can pause the game multiple time.

        :param event_button_down: the pygame.Event obj corresponding with the event of mouse pressinfd
        :param click_one_time: True if the click of the mouse can be done only one time.
        :return:
        """
        mouse_pos_down = event_button_down.__dict__["pos"]
        if self.__button.get_rect(topleft=(self.__pos_x, self.__pos_y)).collidepoint(mouse_pos_down) and \
                (not click_one_time or not self.__clicked):
            self.__clicked = not self.__clicked


    def blit(self, pos_x: int , pos_y: int) -> None:
        """
        Essentially replace the blit call of the method of the pygame.Surface
        in order to have a better and clean code.

        :param pos_x: Position along the x-axis
        :param pos_y: Position along the y-axis
        :return:
        """
        self.__surface.blit(self.__button, (pos_x, pos_y))
        self.__pos_x, self.__pos_y = pos_x, pos_y