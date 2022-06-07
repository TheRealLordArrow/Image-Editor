import pygame.mouse


class Clickable:

    def __init__(self, editor, position: tuple[int, int], size: tuple[int, int]):
        self.editor = editor
        self.position = position
        self.size = size
        self.pressed = True
        self.mouse_over = False

    def get_position(self) -> tuple[int, int]:
        return self.position

    def is_mouse_over(self) -> bool:
        mouse_position = self.editor.get_responsive_mouse_position()
        return self.position[0] <= mouse_position[0] <= (self.position[0] + self.size[0]) and self.position[1] <= \
            mouse_position[1] <= (self.position[1] + self.size[1])

    def handle(self) -> None:
        if self.is_mouse_over():
            if not self.mouse_over:
                self.mouse_over = True
                self.on_mouse_over()
            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    if self.mouse_over:
                        self.pressed = True
                        self.on_press()
                    else:
                        self.pressed = False
            else:
                self.pressed = False
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.pressed = True
                self.on_mouse_left()

    def on_mouse_over(self) -> None:
        pass

    def on_mouse_left(self) -> None:
        pass

    def on_press(self):
        pass
