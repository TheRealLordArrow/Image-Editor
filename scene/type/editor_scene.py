import math

import pygame

from gui.button import Button
from gui.painting_area import PaintingArea
from scene.scene import Scene
from util import action_utils, editing_settings
from util.responsive_drawer import ResponsiveDrawer


class EditorScene(Scene):

    def __init__(self, editor):
        super().__init__(editor)
        self.add_button = Button(editor, (55, 8), (36, 36), "add", self.print, "addFilled")
        self.save_button = Button(editor, (105, 8), (36, 36), "save", self.print, "saveFilled")
        self.folder_button = Button(editor, (155, 8), (36, 36), "folder", self.print, "folderFilled")
        self.resize_button = Button(editor, (255, 8), (36, 36), "resize", self.print, "resizeFilled")
        self.left_arrow_button = Button(editor, (355, 8), (36, 36), "leftArrow", self.on_undo, "leftArrowFilled")
        self.right_arrow_button = Button(editor, (405, 8), (36, 36), "rightArrow", self.on_redo, "rightArrowFilled")
        self.debug_button = Button(editor, (1559, 8), (36, 36), "debug", self.on_debug, "debugFilled")

        self.hand_button = Button(editor, (8, 75), (36, 36), "hand", self.print, "handFilled")
        self.bucket_button = Button(editor, (8, 125), (36, 36), "bucket", self.print, "bucketFilled")
        self.pencil_button = Button(editor, (8, 175), (36, 36), "pencil", self.print, "pencilFilled")
        self.pipette_button = Button(editor, (8, 225), (36, 36), "pipette", self.print, "pipetteFilled")
        self.rubber_button = Button(editor, (8, 275), (36, 36), "rubber", self.print, "rubberFilled")
        self.add_image_button = Button(editor, (8, 325), (36, 36), "addImage", self.print, "addImageFilled")
        self.text_button = Button(editor, (8, 375), (36, 36), "text", self.print, "textFilled")
        self.shapes_button = Button(editor, (8, 425), (36, 36), "shapes", self.print, "shapesFilled")
        self.color_selector_button = Button(editor, (8, 525), (36, 36), "colorSelector", self.print,
                                            "colorSelectorFilled")

        self.painting_area = PaintingArea(editor, (90, 90), (1180, 710))
        self.painting_area.set_editing_image("Schnelligkeitstrank")
        self.painting_area.set_zoom(5, False)

        self.action_log = []
        self.undo_log = []



    def listen(self, event: pygame.event.Event):
        if not self.painting_area.is_mouse_over():
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and self.painting_area.get_zoom() < editing_settings.MAX_ZOOM:
                self.painting_area.set_zoom(self.painting_area.get_zoom() + 0.5)
                self.painting_area.render()
            elif event.button == 5 and self.painting_area.get_zoom() > editing_settings.MIN_ZOOM:
                self.painting_area.set_zoom(self.painting_area.get_zoom() - 0.5)
                self.painting_area.render()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                offset = self.painting_area.get_offset()
                self.painting_area.set_offset((offset[0] + editing_settings.PIXEL_CHANGE_PER_MOVE, offset[1]))
                self.painting_area.render()
            elif event.key == pygame.K_d:
                offset = self.painting_area.get_offset()
                self.painting_area.set_offset((offset[0] - editing_settings.PIXEL_CHANGE_PER_MOVE, offset[1]))
                self.painting_area.render()
            elif event.key == pygame.K_w:
                offset = self.painting_area.get_offset()
                self.painting_area.set_offset((offset[0], offset[1] + editing_settings.PIXEL_CHANGE_PER_MOVE))
                self.painting_area.render()
            elif event.key == pygame.K_s:
                offset = self.painting_area.get_offset()
                self.painting_area.set_offset((offset[0], offset[1] - editing_settings.PIXEL_CHANGE_PER_MOVE))
                self.painting_area.render()

    def handle(self) -> None:
        self.save_button.handle()
        self.add_button.handle()
        self.folder_button.handle()
        self.resize_button.handle()
        self.left_arrow_button.handle()
        self.right_arrow_button.handle()
        self.debug_button.handle()

        self.hand_button.handle()
        self.bucket_button.handle()
        self.pencil_button.handle()
        self.pipette_button.handle()
        self.rubber_button.handle()
        self.add_image_button.handle()
        self.text_button.handle()
        self.shapes_button.handle()
        self.color_selector_button.handle()

        self.painting_area.handle()

        if self.painting_area.is_mouse_over():
            if pygame.mouse.get_pressed()[0]:
                position = self.editor.get_responsive_mouse_position()
                area_position = self.painting_area.get_position()
                position = position[0] - area_position[0], position[1] - area_position[1]
                offset = self.painting_area.get_offset()
                x = math.floor(position[0] / (1 + self.painting_area.get_zoom())) - offset[0]
                y = math.floor(position[1] / (1 + self.painting_area.get_zoom())) - offset[1]

                color = self.painting_area.get_pixel_at((x, y))

                if color is None or color == (255, 0, 0):
                    return

                self.painting_area.set_pixel_at((255, 0, 0), (x, y))

                self.action_log.append(action_utils.from_set(color, (255, 0, 0), (x, y)))
                if len(self.action_log) >= editing_settings.MAX_ACTION_LOG_SIZE + 1:
                    self.action_log.remove(self.action_log[0])

    def render(self, responsive_drawer: ResponsiveDrawer) -> None:
        responsive_drawer.draw_rect((200, 200, 200), (0, 0, 1600, 900))

        responsive_drawer.draw_rect((100, 100, 100), (0, 0, 1600, 50))
        responsive_drawer.draw_rect((0, 0, 0), (50, 50, 1550, 10))

        responsive_drawer.draw_rect((100, 100, 100), (0, 0, 50, 900))
        responsive_drawer.draw_rect((0, 0, 0), (50, 50, 10, 850))

        responsive_drawer.draw_rect((0, 0, 0), (80, 80, 1200, 730))

        self.save_button.render()
        self.add_button.render()
        self.folder_button.render()
        self.resize_button.render()
        self.left_arrow_button.render()
        self.right_arrow_button.render()
        self.debug_button.render()

        self.hand_button.render()
        self.bucket_button.render()
        self.pencil_button.render()
        self.pipette_button.render()
        self.rubber_button.render()
        self.add_image_button.render()
        self.text_button.render()
        self.shapes_button.render()
        self.color_selector_button.render()

        self.painting_area.render()

    def on_undo(self) -> None:
        if len(self.action_log) == 0:
            return

        last_action = self.action_log[-1]

        if last_action is list:
            for action in last_action:
                self.undo_action(action)
        else:
            self.undo_action(last_action)

        self.painting_area.set_zoom(self.painting_area.get_zoom(), False)
        self.painting_area.render()

        self.action_log.remove(last_action)

        self.undo_log.append(last_action)
        if len(self.undo_log) >= editing_settings.MAX_UNDO_LOG_SIZE + 1:
            self.undo_log.remove(self.undo_log[0])

    def undo_action(self, action: dict) -> None:
        if action["action_id"] == action_utils.SET:
            self.painting_area.set_pixel_at(action["old_color"], action["position"])

    def on_redo(self) -> None:
        if len(self.undo_log) == 0:
            return

        last_undo = self.undo_log[-1]

        if last_undo is list:
            for action in last_undo:
                self.redo_action(action)
        else:
            self.redo_action(last_undo)

        self.painting_area.set_zoom(self.painting_area.get_zoom(), False)
        self.painting_area.render()

        self.undo_log.remove(last_undo)

        self.action_log.append(last_undo)
        if len(self.action_log) >= editing_settings.MAX_ACTION_LOG_SIZE + 1:
            self.action_log.remove(self.action_log[0])

    def redo_action(self, action: dict) -> None:
        if action["action_id"] == action_utils.SET:
            self.painting_area.set_pixel_at(action["new_color"], action["position"])

    def on_debug(self) -> None:
        self.editor.toggle_debug()
        self.render(self.editor.get_responsive_drawer())

    def print(self):
        pass
