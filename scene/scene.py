import pygame.event

from util.responsive_drawer import ResponsiveDrawer


class Scene:

    def __init__(self, editor):
        self.editor = editor

    def get_name(self) -> str:
        return self.__class__.__name__

    def listen(self, event: pygame.event.Event):
        pass

    def handle(self) -> None:
        pass

    def render(self, responsive_drawer: ResponsiveDrawer) -> None:
        pass
