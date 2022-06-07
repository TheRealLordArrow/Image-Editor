import copy

import pygame.event

from scene.scene import Scene
from scene.type.editor_scene import EditorScene
from util.responsive_drawer import ResponsiveDrawer


class SceneManager:

    def __init__(self, editor):
        self.editor = editor
        self.current_scene = EditorScene(editor)
        self.registered_scenes = {}
        self.register_scenes(
            [
                EditorScene(editor),

            ]
        )
        self.render(self.editor.get_responsive_drawer())

    def get_current_scene(self) -> Scene:
        return self.current_scene

    def register_scene(self, scene: Scene) -> None:
        self.registered_scenes[scene.get_name()] = scene

    def register_scenes(self, scenes: list[Scene]) -> None:
        for scene in scenes:
            self.register_scene(scene)

    def change_scene(self, name: str) -> None:
        for scene in self.registered_scenes:
            if scene.get_name() == name:
                self.current_scene = (copy.copy(scene))
                self.render(self.editor.get_responsive_drawer())
                return
        raise RuntimeError(f"no registered scene named {name} found")

    def listen(self, event: pygame.event.Event) -> None:
        self.current_scene.listen(event)

    def handle(self) -> None:
        self.current_scene.handle()

    def render(self, responsive_drawer: ResponsiveDrawer) -> None:
        self.current_scene.render(responsive_drawer)
