import os.path
from pathlib import Path

import pygame.image


class TextureManager:

    def __init__(self):
        self.default_path = os.getcwd() + "/data/texture/"
        self.textures = {}

    def load_texture(self, path: str) -> None:
        if os.path.isfile(path):
            name = Path(path).name.split(".")
            self.textures[name[0]] = pygame.image.load(path).convert_alpha()

    def load_textures(self, path: str = None) -> None:
        if path is None:
            path = self.default_path
        if os.path.isdir(path):
            for file in os.scandir(path):
                if os.path.isdir(path + "\\" + file.name):
                    self.load_textures(path + "\\" + file.name)
                else:
                    self.load_texture(path + "\\" + file.name)

    def get_texture(self, name: str) -> pygame.image:
        return self.textures[name]
