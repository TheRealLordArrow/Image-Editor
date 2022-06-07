import pygame as pygame

from manager.texture_manager import TextureManager
from scene.scene_manager import SceneManager
from util import window_settings
from util.responsive_drawer import ResponsiveDrawer


class ImageEditor:

    # TODO: add alpha everywhere where color is used

    def __init__(self):
        pygame.init()

        pygame.font.init()

        pygame.display.set_caption("Image Editor")

        self.screen = pygame.display.set_mode(window_settings.DEFAULT_SIZE, pygame.RESIZABLE)

        self.texture_manager = TextureManager()
        self.texture_manager.load_textures()

        self.responsive_drawer = ResponsiveDrawer(self)

        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.debug = False

        self.scene_manager = SceneManager(self)

        self.update()

    def update(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    return
                elif event.type == pygame.WINDOWRESIZED:
                    if event.x < window_settings.MINIMUM_SIZE[0]:
                        event.x = window_settings.MINIMUM_SIZE[0]
                        pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                    if event.y < window_settings.MINIMUM_SIZE[1]:
                        event.y = window_settings.MINIMUM_SIZE[1]
                        pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                    x_scale = event.x / window_settings.DEFAULT_SIZE[0]
                    y_scale = event.y / window_settings.DEFAULT_SIZE[1]
                    self.responsive_drawer.set_current_scale((x_scale, y_scale))

                self.scene_manager.listen(event)

            self.scene_manager.handle()

            pygame.display.update()

            self.clock.tick(self.max_fps)

    def get_screen(self) -> pygame.Surface:
        return self.screen

    def get_texture_manager(self) -> TextureManager:
        return self.texture_manager

    def get_responsive_drawer(self) -> ResponsiveDrawer:
        return self.responsive_drawer

    def get_responsive_mouse_position(self) -> tuple[int, int]:
        mouse_position = pygame.mouse.get_pos()
        scale = self.responsive_drawer.get_current_scale()
        x = 1 / scale[0] * mouse_position[0]
        y = 1 / scale[1] * mouse_position[1]
        return int(x), int(y)

    def get_scene_manager(self) -> SceneManager:
        return self.scene_manager

    def is_debug_enabled(self) -> bool:
        return self.debug

    def toggle_debug(self) -> None:
        if self.debug:
            self.debug = False
        else:
            self.debug = True


if __name__ == "__main__":
    ImageEditor()
