import pygame
from PIL import Image

from util import cursor_types
from util.clickable import Clickable


class PaintingArea(Clickable):

    def __init__(self, editor, position: tuple[int, int], size: tuple[int, int]):
        super().__init__(editor, position, size)
        self.zoom = 0
        self.offset = 0, 0
        self.editing_image = None
        self.showing_image = None

    def get_zoom(self) -> float:
        return self.zoom

    def set_zoom(self, zoom: float, auto_offset: bool = True) -> None:
        self.zoom = zoom
        image = self.editing_image
        image = Image.frombytes("RGBA", image.get_size(), pygame.image.tostring(image, "RGBA")).resize(
            (int(image.get_size()[0] * (1 + self.zoom)), int(image.get_size()[1] * (1 + self.zoom))), Image.NEAREST)
        self.showing_image = pygame.image.fromstring(image.tobytes(), image.size, "RGBA")

        if auto_offset and self.is_mouse_over():
            position = self.editor.get_responsive_mouse_position()
            position = position[0] - self.position[0], position[1] - self.position[1]
            pixel_size = 1 + self.zoom
            offset_x = (self.size[0] / pixel_size / 2 - position[0] / pixel_size) * 0.25 + self.offset[0]
            offset_y = (self.size[1] / pixel_size / 2 - position[1] / pixel_size) * 0.25 + self.offset[1]
            self.set_offset((int(offset_x), int(offset_y)))

    def get_offset(self) -> tuple[int, int]:
        return self.offset

    def set_offset(self, offset: tuple[int, int]) -> None:
        self.offset = offset

    def get_editing_image(self) -> pygame.image:
        return self.editing_image

    def set_editing_image(self, name: str) -> None:
        self.editing_image = self.editor.get_texture_manager().get_texture(name)
        self.showing_image = self.editing_image

    def render(self) -> None:
        responsive_drawer = self.editor.get_responsive_drawer()

        self.editor.screen.set_clip((responsive_drawer.scale_number(self.position[0]),
                                     responsive_drawer.scale_number(self.position[1], True),
                                     responsive_drawer.scale_number(self.size[0]),
                                     responsive_drawer.scale_number(self.size[1], True)))

        pixel_size = 1 + self.zoom

        size = self.editing_image.get_size()

        responsive_drawer.draw_rect((80, 80, 80), (self.position[0], self.position[1], self.size[0], self.size[1]))

        if self.editor.is_debug_enabled():
            responsive_drawer.draw_rect((255, 255, 255), (self.position[0] + (self.offset[0] * pixel_size),
                                                          self.position[1] + (self.offset[1] * pixel_size),
                                                          size[0] * pixel_size, size[1] * pixel_size))

        responsive_drawer.draw_image(self.showing_image, (self.position[0] + (self.offset[0] * pixel_size),
                                     self.position[1] + (self.offset[1] * pixel_size)),
                                     nearest_neighbor_scaling=True)

        self.editor.screen.set_clip(None)

    def set_pixel_at(self, color: tuple[int, int, int], position: tuple[int, int]) -> None:
        self.editing_image.set_at(position, color)
        self.set_zoom(self.zoom, False)
        self.render()

    def get_pixel_at(self,  position: tuple[int, int]) -> tuple[int, int, int] or None:
        try:
            return self.editing_image.get_at(position)
        except IndexError:
            return None

    def on_mouse_over(self) -> None:
        cursor = cursor_types.PAINT
        pygame.mouse.set_cursor(cursor["size"], (cursor["hotspot"]), *pygame.cursors.compile(cursor["strings"]))

    def on_mouse_left(self) -> None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
