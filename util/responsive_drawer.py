import pygame
from PIL import Image


class ResponsiveDrawer:

    def __init__(self, editor):
        self.editor = editor
        self.screen = editor.get_screen()
        self.current_scale = (1, 1)

    def get_current_scale(self) -> tuple[float, float]:
        return self.current_scale

    def set_current_scale(self, scale: tuple[float, float]) -> None:
        self.current_scale = scale
        self.editor.get_scene_manager().render(self)

    def scale_number(self, number: int, y: bool = False) -> int:
        if y:
            return number * self.current_scale[1]
        else:
            return number * self.current_scale[0]

    def draw_rect(self, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        x = self.scale_number(rect[0])
        y = self.scale_number(rect[1], True)
        width = self.scale_number(rect[2])
        height = self.scale_number(rect[3], True)
        # TODO: save performance by testing if scale is needed
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_image(self, image: str or pygame.image, position: tuple[int, int], scale: tuple[int, int] = None,
                   nearest_neighbor_scaling: bool = False) -> None:
        if isinstance(image, str):
            image = self.editor.get_texture_manager().get_texture(image)
        x = self.scale_number(position[0])
        y = self.scale_number(position[1], True)
        if scale is None:
            width = self.scale_number(image.get_width())
            height = self.scale_number(image.get_height(), True)
        else:
            width = self.scale_number(scale[0])
            height = self.scale_number(scale[1], True)
            # TODO: save performance by testing if scale is needed
        if nearest_neighbor_scaling:
            image = Image.frombytes("RGBA", image.get_size(),
                                    pygame.image.tostring(image, "RGBA")).resize((int(width), int(height)), Image.NEAREST)
            image = pygame.image.fromstring(image.tobytes(), image.size, "RGBA")
        else:
            image = pygame.transform.smoothscale(image, (width, height))
        self.editor.get_screen().blit(image, (x, y))

