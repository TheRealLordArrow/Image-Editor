from typing import Callable

from util.clickable import Clickable


class Button(Clickable):

    def __init__(self, editor, position: tuple[int, int], size: tuple[int, int], image: str, on_press: Callable,
                 image_on_mouse_over: str = None):
        super().__init__(editor, position, size)
        self.image = image
        self.press_callback = on_press
        self.image_on_mouse_over = image_on_mouse_over

    def render(self) -> None:
        responsive_drawer = self.editor.get_responsive_drawer()
        if self.editor.is_debug_enabled():
            responsive_drawer.draw_rect((255, 255, 255), (self.position[0], self.position[1]
                                                          , self.size[0], self.size[1]))
        else:
            responsive_drawer.draw_rect((100, 100, 100), (self.position[0], self.position[1]
                                                          , self.size[0], self.size[1]))
        if self.image_on_mouse_over is not None and self.is_mouse_over():
            responsive_drawer.draw_image(self.image_on_mouse_over, self.position, self.size)
        else:
            responsive_drawer.draw_image(self.image, self.position, self.size)

    def on_mouse_over(self) -> None:
        self.render()

    def on_mouse_left(self) -> None:
        self.render()

    def on_press(self):
        self.press_callback()
