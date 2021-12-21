"""
False Worlds: Jacob Meadows' final program for Practicum IT
    Copyright (C) 2019  Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
Started on: 23 November, 2019
"""
import glfw
import numpy
import pyrr
import noise
import os
import random
import time
from threading import Thread
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


# region Constants
HIGHLIGHTED_CUBE = numpy.array([-0.02, -0.02, 1.02, 0.0, 0.0,
                                1.02, -0.02, 1.02, 1.0, 0.0,
                                1.02, 1.02, 1.02, 1.0, 1.0,
                                -0.02, 1.02, 1.02, 0.0, 1.0,

                                -0.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, -0.02, -0.02, 1.0, 0.0,
                                1.02, 1.02, -0.02, 1.0, 1.0,
                                -0.02, 1.02, -0.02, 0.0, 1.0,

                                1.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, 1.02, -0.02, 0.0, 1.0,
                                1.02, 1.02, 1.02, 1.0, 1.0,
                                1.02, -0.02, 1.02, 1.0, 0.0,

                                -0.02, 1.02, -0.02, 1.0, 1.0,
                                -0.02, -0.02, -0.02, 1.0, 0.0,
                                -0.02, -0.02, 1.02, 0.0, 0.0,
                                -0.02, 1.02, 1.02, 0.0, 1.0,

                                -0.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, -0.02, -0.02, 1.0, 0.0,
                                1.02, -0.02, 1.02, 1.0, 1.0,
                                -0.02, -0.02, 1.02, 0.0, 1.0,

                                1.02, 1.02, -0.02, 0.0, 0.0,
                                -0.02, 1.02, -0.02, 1.0, 0.0,
                                -0.02, 1.02, 1.02, 1.0, 1.0,
                                1.02, 1.02, 1.02, 0.0, 1.0], dtype=numpy.float32)
# HIGHLIGHTED_CUBE = numpy.where(HIGHLIGHTED_CUBE[:] < 0, HIGHLIGHTED_CUBE[:] + 0.01, HIGHLIGHTED_CUBE[:] - 0.01)
CUBE_INDICES_EDGES = numpy.array([0, 1, 2, 3,
                                  6, 5, 4, 7,
                                  8, 9, 10, 11,
                                  12, 13, 14, 15,
                                  16, 17, 18, 19,
                                  20, 21, 22, 23], dtype=numpy.uint32)
INDICES = numpy.array([0, 1, 2, 2, 3, 0], dtype=numpy.uint32)
HOTBAR = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 44.0, 0.0, 0.0, 1.0,
                      364.0, 44.0, 0.0, 1.0, 1.0,
                      364.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
ACTIVE_BAR = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 48.0, 0.0, 0.0, 1.0,
                          48.0, 48.0, 0.0, 1.0, 1.0,
                          48.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
HOTBAR_ICON = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                           0.0, 32.0, 0.0, 0.0, 1.0,
                           32.0, 32.0, 0.0, 1.0, 1.0,
                           32.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
CROSSHAIR_V = numpy.array([15.0, 0.0, 0.0, 0.0, 0.0,
                           15.0, 32.0, 0.0, 0.0, 1.0,
                           17.0, 32.0, 0.0, 1.0, 1.0,
                           17.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
CROSSHAIR_H = numpy.array([0.0, 15.0, 0.0, 0.0, 0.0,
                           0.0, 17.0, 0.0, 0.0, 1.0,
                           32.0, 17.0, 0.0, 1.0, 1.0,
                           32.0, 15.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
INVENTORY = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 332.0, 0.0, 0.0, 1.0,
                         352.0, 332.0, 0.0, 1.0, 1.0,
                         352.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
SCREEN = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 720.0, 0.0, 0.0, 1.0,
                      1280.0, 720.0, 0.0, 1.0, 1.0,
                      1280.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
BUTTON_OUTLINE = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                              0.0, 40.0, 0.0, 0.0, 1.0,
                              400.0, 40.0, 0.0, 1.0, 1.0,
                              400.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
CHARACTER_DICT = {
    "a": (((8, 48), (5, 5)), ((8, 32), (5, 7))),
    "b": (((16, 48), (5, 7)), ((16, 32), (5, 7))),
    "c": (((24, 48), (5, 5)), ((24, 32), (5, 7))),
    "d": (((32, 48), (5, 7)), ((32, 32), (5, 7))),
    "e": (((40, 48), (5, 5)), ((40, 32), (5, 7))),
    "f": (((48, 48), (4, 7)), ((48, 32), (5, 7))),
    "g": (((56, 48), (5, 6)), ((56, 32), (5, 7))),
    "h": (((64, 48), (5, 7)), ((64, 32), (5, 7))),
    "i": (((72, 48), (1, 7)), ((72, 32), (3, 7))),
    "j": (((80, 48), (5, 8)), ((80, 32), (5, 7))),
    "k": (((88, 48), (4, 7)), ((88, 32), (5, 7))),
    "l": (((96, 48), (2, 7)), ((96, 32), (5, 7))),
    "m": (((104, 48), (5, 5)), ((104, 32), (5, 7))),
    "n": (((112, 48), (5, 5)), ((112, 32), (5, 7))),
    "o": (((120, 48), (5, 5)), ((120, 32), (5, 7))),
    "p": (((0, 56), (5, 6)), ((0, 40), (5, 7))),  # temporary capital size values (5, 7)
    "q": (((8, 56), (5, 6)), ((8, 40), (5, 7))),  # temporary capital size values (5, 7)
    "r": (((16, 56), (5, 5)), ((16, 40), (5, 7))),  # temporary capital size values (5, 7)
    "s": (((24, 56), (5, 5)), ((24, 40), (5, 7))),  # temporary capital size values (5, 7)
    "t": (((32, 56), (3, 7)), ((32, 40), (5, 7))),  # temporary capital size values (5, 7)
    "u": (((40, 56), (5, 5)), ((40, 40), (5, 7))),  # temporary capital size values (5, 7)
    "v": (((48, 56), (5, 5)), ((48, 40), (5, 7))),  # temporary capital size values (5, 7)
    "w": (((56, 56), (5, 5)), ((56, 40), (5, 7))),  # temporary capital size values (5, 7)
    "x": (((64, 56), (5, 5)), ((64, 40), (5, 7))),  # temporary capital size values (5, 7)
    "y": (((72, 56), (5, 6)), ((72, 40), (5, 7))),  # temporary capital size values (5, 7)
    "z": (((80, 56), (5, 5)), ((80, 40), (5, 7))),  # temporary capital size values (5, 7)
}
SPECIAL_CHARACTER_DICT = {
    ".": ((112, 16), (1, 2)),
    ">": ((112, 24), (4, 7)),
    ",": ((96, 16), (1, 3)),
    "<": ((96, 24), (4, 7)),
    "-": ((104, 16), (5, 1)),
    "*": ((80, 16), (4, 3)),
    ":": ((80, 24), (1, 6)),
    "0": ((0, 24), (5, 7)),
    "1": ((8, 24), (5, 7)),
    "2": ((16, 24), (5, 7)),
    "3": ((24, 24), (5, 7)),
    "4": ((32, 24), (5, 7)),
    "5": ((40, 24), (5, 7)),
    "6": ((48, 24), (5, 7)),
    "7": ((56, 24), (5, 7)),
    "8": ((64, 24), (5, 7)),
    "9": ((72, 24), (5, 7))
}
ASCII_PNG = Image.open("textures/_ascii.png")
BLOCK_DICT = {
    0: "air",
    1: "stone",
    2: "grass",
    3: "dirt",
    4: "cobblestone",
    5: "wooden_plank",
    6: "sapling",
    7: "bedrock"
}
BLOCK_IDS = {block_id: block_name for block_name, block_id in BLOCK_DICT.items()}
BLOCK_INFO = {
    "stone": {"hardness": 1.5, "silk_touch": 4, "tool": "pickaxe", "harvestable": "tool"},
    "grass": {"hardness": 0.6, "silk_touch": 3, "tool": "shovel", "harvestable": True},
    "dirt": {"hardness": 0.5, "silk_touch": 0, "tool": "shovel", "harvestable": True},
    "cobblestone": {"hardness": 2, "silk_touch": 0, "tool": "pickaxe", "harvestable": "tool"},
    "wooden_plank": {"hardness": 2, "silk_touch": 0, "tool": "axe", "harvestable": True},
    "sapling": {"hardness": 0, "silk_touch": 0, "tool": None, "harvestable": True},
    "bedrock": {"hardness": numpy.inf, "silk_touch": 0, "tool": None, "harvestable": False}
}
DIFFICULTIES = {0: "Peaceful", 1: "Easy", 2: "Normal", 3: "Hard"}
# endregion


class App:
    def __init__(self, width, height, title):
        # region GLFW Initialization
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.set_window_size_callback(self.window, self.window_resize)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        # endregion

        # region Variables
        self.mouse_visibility = True
        self.in_menu = True
        self.in_inventory = False
        self.in_game = False
        self.paused = False
        self.new_game = False
        self.highlighted = None
        self.breaking_block = None
        self.selected_block = str()
        self.world = dict()
        self.vaos_2d = dict()
        self.vaos_3d = dict()
        self.buttons = dict()
        self.keys = [False] * 1024
        self.mouse_value = [0, 0]
        self.active_bar = 1
        self.fps = int()
        self.width, self.height = width, height
        self.time_p = glfw.get_timer_value()
        self.player = Player(self)
        self.text = Text()
        for vao in self.text.vaos:
            self.vaos_2d[vao] = self.text.vaos[vao]
        self.buttons = Button(self)
        self.load_states = self.get_load_data()
        highlighted_vao = Entity(HIGHLIGHTED_CUBE, CUBE_INDICES_EDGES, "textures/_black.png")
        self.old_player_chunk = tuple()
        block_break = list()
        for stage in range(10):
            block_break.append(Entity.load_texture(f"textures/_destroy_stage_{stage}.png", transpose=True))
        # endregion

        # region OpenGL Initialization
        shader = compileProgram(compileShader(open("vertex.glsl", "r").read(), GL_VERTEX_SHADER),
                                compileShader(open("fragment.glsl", "r").read(), GL_FRAGMENT_SHADER))
        self.projection_loc = glGetUniformLocation(shader, "projection")
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, 1280 / 720, 0.1, 100.0)
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 720, 0, 0.01, 100.0)
        self.view_loc = glGetUniformLocation(shader, "view")
        view_2d = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])
        self.model_loc = glGetUniformLocation(shader, "model")
        model_3d = pyrr.matrix44.create_from_translation([0.0, -1.62, 0.0])
        model_2d = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])

        glClearColor(135 / 255, 206 / 255, 235 / 255, 1.0)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(4)  # todo figure out how large the outlines need to be for highlighted blocks
        glUseProgram(shader)
        # endregion

        self.main_menu()

        sin_translation = numpy.array(pyrr.matrix44.create_from_translation((0, 0, 0)), dtype=numpy.float32)
        self.default_matrix = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])
        self.y_values = numpy.zeros([1024, 1024], dtype=numpy.int32)
        self.rendered_chunks = dict()
        self.chunk_load = dict()
        self.updating = None
        self.nearby_chunks = [(x, z) for x in range(-2, 3) for z in range(-2, 3)]
        self.update = False
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            old_fps = self.fps
            time_n = glfw.get_timer_value()
            time_s = (time_n - self.time_p) / 10000000
            self.time_p = time_n
            self.fps = round(time_s ** -1)
            self.text.remove_text(f"{old_fps}", [1240.0, 20.0, -0.4], 2)
            self.text.add_text(f"{self.fps}", [1240.0, 20.0, -0.4], 2)
            self.mouse_button_check(time_s)
            view = self.player.get_view_matrix()

            if self.update:
                self.update = False
                for block_name in self.transform:
                    for side in self.transform[block_name]:
                        self.transform[block_name][side] = numpy.array([], dtype=numpy.float32)
                for chunk in self.rendered_chunks:
                    if chunk in self.nearby_chunks:
                        for block_name in self.rendered_chunks[chunk]:
                            for side in self.rendered_chunks[chunk][block_name]:
                                new_transform = self.rendered_chunks[chunk][block_name][side]
                                if len(new_transform) > 0:
                                    if self.transform[block_name][side] is not None and \
                                            len(self.transform[block_name][side]) > 0:
                                        self.transform[block_name][side] = \
                                            numpy.append(self.transform[block_name][side], new_transform, 0)
                                    else:
                                        self.transform[block_name][side] = new_transform.copy()
                for cube in self.vaos_3d:
                    for side in self.vaos_3d[cube].sides:
                        if cube in self.transform and self.transform[cube][side] is not None:
                            self.vaos_3d[cube].sides[side].transform_update(self.transform[cube][side].copy())

            rotation_y = pyrr.matrix44.create_from_y_rotation(time_s)
            for vao in self.vaos_3d:
                if "item" in vao and self.vaos_3d[vao].top.transform is not None:
                    remove_list = list()
                    for transform in range(len(self.vaos_3d[vao].top.transform)):
                        pickup_delay = self.vaos_3d[vao].top.item_data[transform, 7]
                        self.vaos_3d[vao].top.item_data[transform, 7] = pickup_delay - time_s if pickup_delay > 0 else 0
                        x, y, z = self.vaos_3d[vao].top.transform[transform, 3, : 3]
                        if self.vaos_3d[vao].top.item_data[transform, 4: 7].any():
                            x, y, z = self.vaos_3d[vao].top.item_data[transform, 4: 7]
                        if self.vaos_3d[vao].top.item_data[transform, 4: 7].any() and \
                                self.vaos_3d[vao].top.item_data[transform, 1] == 0:
                            sin_translation[3, 1] = (numpy.sin(self.vaos_3d[vao].top.item_data[transform, 3]) * time_s) / 4
                            self.vaos_3d[vao].top.item_data[transform, 3] += time_s  # todo might be better somewhere else
                        else:
                            sin_translation[3, 1] = 0
                            self.vaos_3d[vao].top.item_data[transform, 3] = 0
                        if self.check_pos((x, numpy.ceil(y - 1), z)):
                            self.vaos_3d[vao].top.item_data[transform, 4: 7] = 0, 0, 0
                            self.vaos_3d[vao].top.item_data[transform, 1] -= 16 * time_s
                            self.vaos_3d[vao].top.item_data[transform, 1] += 0.4 * self.vaos_3d[vao].top.item_data[transform, 1] * time_s
                            if self.check_pos((x, int(numpy.ceil(y + self.vaos_3d[vao].top.item_data[transform, 1] * time_s - 1)), z)):
                                if self.check_pos((x, int(numpy.ceil(y + 0.25 + self.vaos_3d[vao].top.item_data[transform, 1] * time_s - 1)), z)):
                                    sin_translation[3, 1] += self.vaos_3d[vao].top.item_data[transform, 1] * time_s
                                else:
                                    self.vaos_3d[vao].top.item_data[transform, 1] = 0
                                    self.vaos_3d[vao].top.transform[transform][3, 1] = int(y) + 0.49
                            else:
                                self.vaos_3d[vao].top.item_data[transform, 1] = 0
                                self.vaos_3d[vao].top.transform[transform, 3, 1] = round(y)
                                self.vaos_3d[vao].top.item_data[transform, 4: 7] = x, round(y), z
                        elif self.vaos_3d[vao].top.item_data[transform, 1]:
                            self.vaos_3d[vao].top.item_data[transform, 1] = 0
                            self.vaos_3d[vao].top.transform[transform, 3, 1] = round(y)
                            self.vaos_3d[vao].top.item_data[transform, 4: 7] = x, round(y), z
                        new_transform = numpy.dot(rotation_y, numpy.dot(sin_translation, self.vaos_3d[vao].top.transform[transform]))
                        dx = self.vaos_3d[vao].top.item_data[transform, 0] * time_s
                        dz = self.vaos_3d[vao].top.item_data[transform, 2] * time_s
                        if self.check_pos((x + dx, numpy.ceil(y - 1), z + dz)):
                            new_transform[3, 0] += dx
                            new_transform[3, 2] += dz
                        else:
                            self.vaos_3d[vao].top.item_data[transform, 0] = 0
                            self.vaos_3d[vao].top.item_data[transform, 2] = 0
                        for side in self.vaos_3d[vao].sides:
                            self.vaos_3d[vao].sides[side].transform[transform] = new_transform
                        px, py, pz = self.player.pos
                        if px - 1 < x < px + 1 and py - 1 < y < py + 1 and pz - 1 < z < pz + 1 and \
                                self.vaos_3d[vao].top.item_data[transform, 7] == 0:
                            self.inventory_add("_".join(vao.split("_")[:-1]))
                            remove_list.append(transform)
                    for pos in reversed(sorted(remove_list)):
                        self.vaos_3d[vao].top.item_data = numpy.delete(self.vaos_3d[vao].top.item_data, pos, 0)
                        for side in self.vaos_3d[vao].sides:
                            self.vaos_3d[vao].sides[side].transform = numpy.delete(
                                self.vaos_3d[vao].sides[side].transform, pos, 0
                            )
                    for side in self.vaos_3d[vao].sides:
                        self.vaos_3d[vao].sides[side].transform_update()

            if self.in_game:
                if not self.paused:
                    if self.in_menu:
                        self.in_menu = False
                        self.buttons.clear()
                        self.text.remove_text("Paused", [570.0, 140.0, -0.3], 4)
                    self.do_movement(time_s)
                    view = self.player.get_view_matrix()
                    mx, my = glfw.get_cursor_pos(self.window)
                    ray_nds = pyrr.Vector3([(2.0 * mx) / self.width - 1.0, 1.0 - (2.0 * my) / self.height, 1.0])
                    ray_clip = pyrr.Vector4([*ray_nds.xy, -1.0, 1.0])
                    ray_eye = pyrr.Vector4(numpy.dot(numpy.linalg.inv(self.projection_3d), ray_clip))
                    ray_eye = pyrr.Vector4([*ray_eye.xy, -1.0, 0.0])
                    ray_wor = (numpy.linalg.inv(view) * ray_eye).xyz
                    self.ray_wor = pyrr.vector.normalise(ray_wor)
                    self.s_ray_wor = self.player.pos.copy()
                    self.s_ray_wor[1] += 1.62
                    self.s_ray_wor = [int(self.check_value(axis, 0)) for axis in self.s_ray_wor]
                    self.e_ray_wor = self.player.pos + (self.ray_wor * 4)
                    self.e_ray_wor[1] += 1.62
                    self.e_ray_wor = [int(self.check_value(axis, 0)) for axis in self.e_ray_wor]
                    self.ray_i = 4
                    air = True
                    values = list()
                    for pos in range(3):
                        step = -1 if self.e_ray_wor[pos] < self.s_ray_wor[pos] else 1
                        for value in range(self.s_ray_wor[pos], self.e_ray_wor[pos] + step, step):
                            value -= self.player.pos[pos]
                            if pos == 1:
                                value -= 1.62
                            i = (value / self.ray_wor[pos])
                            if i not in values:  # todo clean up code below
                                values.append(i)
                                ray_cam = self.player.pos + (self.ray_wor * i)
                                ray_cam[1] += 1.62
                                orig_ray_cam = ray_cam.copy()
                                ray_cam[pos] -= 1
                                if ray_cam[pos] < 0:
                                    ray_cam[pos] += 0.5  # arbitrary number between 0 and 1 to fix rounding ex: -2 -> -3
                                try:
                                    ray_cam = numpy.array([int(self.check_value(axis, 0)) for axis in ray_cam])
                                except (OverflowError, ValueError):
                                    pass
                                if 0 < ray_cam[1] < 251:
                                    ix, iy, iz = int(self.check_value(ray_cam[0] % 16, 0)), ray_cam[1], int(self.check_value(ray_cam[2] % 16, 0))
                                    chunk = [int(self.check_value(ray_cam[0] / 16, 0)), int(self.check_value(ray_cam[2] / 16, 0))]
                                    if ray_cam[0] < 0 and ray_cam[0] % 16 == 0:
                                        chunk[0] += 1
                                    if ray_cam[2] < 0 and ray_cam[2] % 16 == 0:
                                        chunk[1] += 1
                                    if tuple(chunk) in self.world and self.world[tuple(chunk)][ix, iy, iz, 0] != 0 and 0 < values[-1] < self.ray_i:
                                        air = False
                                        self.highlighted = numpy.array(pyrr.matrix44.create_from_translation(ray_cam),
                                                                       dtype=numpy.float32)
                                        self.ray_cam = ray_cam.copy()
                                        self.ray_i = values[-1]
                                # Copied portion below may not be necessary; a different fix probably exists
                                ray_cam = orig_ray_cam.copy()
                                if ray_cam[pos] < 0:
                                    ray_cam[pos] += 0.5  # arbitrary number between 0 and 1 to fix rounding ex: -2 -> -3
                                try:
                                    ray_cam = numpy.array([int(self.check_value(axis, 0)) for axis in ray_cam])
                                except (OverflowError, ValueError):
                                    pass
                                if 0 < ray_cam[1] < 251:
                                    ix, iy, iz = int(self.check_value(ray_cam[0] % 16, 0)), ray_cam[1], int(self.check_value(ray_cam[2] % 16, 0))
                                    chunk = [int(self.check_value(ray_cam[0] / 16, 0)), int(self.check_value(ray_cam[2] / 16, 0))]
                                    if ray_cam[0] < 0 and ray_cam[0] % 16 == 0:
                                        chunk[0] += 1
                                    if ray_cam[2] < 0 and ray_cam[2] % 16 == 0:
                                        chunk[1] += 1
                                    if tuple(chunk) in self.world and self.world[tuple(chunk)][ix, iy, iz, 0] != 0 and 0 < values[-1] < self.ray_i:
                                        air = False
                                        self.highlighted = numpy.array(pyrr.matrix44.create_from_translation(ray_cam),
                                                                       dtype=numpy.float32)
                                        self.ray_cam = ray_cam.copy()
                                        self.ray_i = values[-1]
                    if self.highlighted is not None and air:
                        self.highlighted = None
                elif self.paused:
                    if not self.in_menu and not self.in_inventory:
                        self.in_menu = True
                        self.text.add_text("Paused", [570.0, 140.0, -0.3], 4)
                        self.buttons.add_instance("Return to Game", [440.0, 240.0], 3,
                                                  lambda: [
                                                      setattr(self, "paused", False),
                                                      setattr(self, "mouse_visibility", False),
                                                      glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                                                  ])
                        self.buttons.add_instance("Quit", [440.0, 440.0], 3,
                                                  lambda: glfw.set_window_should_close(self.window, True))

            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_3d)
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_3d)
            for block in self.vaos_3d.values():
                for side in block.sides.values():
                    if side.transform is not None:
                        glBindVertexArray(side.vao)
                        glBindTexture(GL_TEXTURE_2D, side.texture)
                        glDrawElementsInstanced(
                            GL_TRIANGLES, len(side.index), GL_UNSIGNED_INT, None, int(len(side.transform))
                        )
                        glBindTexture(GL_TEXTURE_2D, 0)
                        glBindVertexArray(0)

            if self.highlighted is not None:
                if not numpy.array_equal(self.highlighted, highlighted_vao.transform):
                    highlighted_vao.transform_update(self.highlighted)
                glBindVertexArray(highlighted_vao.vao)
                if self.player.breaking:
                    if self.player.break_delay >= 0:
                        glBindTexture(GL_TEXTURE_2D, block_break[
                            int(-(self.player.break_delay - (1 - (1 / 10))) / (1 / 10))
                        ])
                    else:
                        glBindTexture(GL_TEXTURE_2D, block_break[int((0.5 - (0.5 / 10)) / (0.5 / 10))])
                    glDrawElementsInstanced(GL_QUADS, len(highlighted_vao.index), GL_UNSIGNED_INT, None,
                                            int(len(highlighted_vao.transform) / 3))
                    glBindTexture(GL_TEXTURE_2D, 0)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glDrawElementsInstanced(GL_QUADS, len(highlighted_vao.index), GL_UNSIGNED_INT, None,
                                        int(len(highlighted_vao.transform) / 3))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glBindVertexArray(0)

            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_2d)
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view_2d)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_2d)
            for vao in self.vaos_2d:
                active = True
                if ("inventory" in vao and not self.in_inventory) or (vao == "paused" and not self.paused) or \
                        ("button" in vao and not self.in_menu) or ("cross" in vao and not self.in_game) or \
                        ("bar" in vao and not self.in_game and "inventory" not in vao):
                    active = False
                if active:
                    if self.vaos_2d[vao].transform is not None:
                        glBindVertexArray(self.vaos_2d[vao].vao)
                        glBindTexture(GL_TEXTURE_2D, self.vaos_2d[vao].texture)
                        glDrawElementsInstanced(
                            GL_TRIANGLES, len(self.vaos_2d[vao].index), GL_UNSIGNED_INT, None,
                            int(len(self.vaos_2d[vao].transform))
                        )
                        glBindTexture(GL_TEXTURE_2D, 0)
                        glBindVertexArray(0)

            glfw.swap_buffers(self.window)

        glfw.terminate()

    # region Menus
    def main_menu(self):
        self.buttons.clear()
        self.text.clear()
        self.text.add_text("False Worlds", [315.0, 120.0, -0.4], 10)
        self.text.add_text(f"{self.fps}", [1240.0, 20.0, -0.4], 2)
        self.buttons.add_instance("Singleplayer", [440.0, 290.0], 3, self.singleplayer_menu)
        self.buttons.add_instance("Multiplayer", [440.0, 340.0], 3, self.multiplayer_menu, False)
        self.buttons.add_instance("Quit", [440.0, 390.0], 3, lambda: glfw.set_window_should_close(self.window, True))

    def singleplayer_menu(self):
        self.buttons.clear()
        self.buttons.add_instance("New Game", [440.0, 290.0], 3, self.new_game_menu)
        if self.load_states:
            self.buttons.add_instance("Load Game", [440.0, 340.0], 3, self.load_game_menu)
        else:
            self.buttons.add_instance("Load Game", [440.0, 340.0], 3, self.load_game_menu, False)
        self.buttons.add_instance("Back", [440.0, 390.0], 3, self.main_menu)

    def multiplayer_menu(self):
        self.buttons.clear()
        self.buttons.add_instance("Back", [440.0, 390.0], 3, self.main_menu)

    def new_game_menu(self):
        def set_difficulty(level=None):
            difficulty_str = f"Difficulty: {DIFFICULTIES[self.player.difficulty]}"
            self.text.remove_text(difficulty_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(difficulty_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in difficulty_str]) / len(difficulty_str)) / 2), 290.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)
            self.player.difficulty = level if level is not None else \
                self.player.difficulty + 1 if self.player.difficulty < 3 else 0
            difficulty_str = f"Difficulty: {DIFFICULTIES[self.player.difficulty]}"
            self.text.add_text(difficulty_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(difficulty_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in difficulty_str]) / len(difficulty_str)) / 2), 290.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)

        def set_gamemode():
            if self.player.gamemode == "Survival":
                gamemode_str = f"Gamemode: {self.player.gamemode}"
                self.text.remove_text(gamemode_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(gamemode_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in gamemode_str]) / len(gamemode_str)) / 2), 340.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)
                self.player.gamemode = "Hardcore"
                gamemode_str = f"Gamemode: {self.player.gamemode}"
                self.text.add_text(gamemode_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(gamemode_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in gamemode_str]) / len(gamemode_str)) / 2), 340.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)
                set_difficulty(3)
                self.buttons.clear()
                self.buttons.add_instance("Difficulty: Hard", [440.0, 290.0], 3, set_difficulty, False)
                self.buttons.add_instance("Gamemode: Hardcore", [440.0, 340.0], 3, set_gamemode)
                self.buttons.add_instance("Create World", [440.0, 440.0], 3, self.game_init)
            elif self.player.gamemode == "Hardcore":
                gamemode_str = f"Gamemode: {self.player.gamemode}"
                self.text.remove_text(gamemode_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(gamemode_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in gamemode_str]) / len(gamemode_str)) / 2), 340.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)
                self.player.gamemode = "Survival"
                gamemode_str = f"Gamemode: {self.player.gamemode}"
                self.text.add_text(gamemode_str, [440.0 + BUTTON_OUTLINE[10] / 2 - len(gamemode_str) * round(3 * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in gamemode_str]) / len(gamemode_str)) / 2), 340.0 + BUTTON_OUTLINE[11] / 2 - 3 * 4, -0.3], 3)
                self.buttons.clear()
                self.buttons.add_instance(f"Difficulty: {DIFFICULTIES[self.player.difficulty]}", [440.0, 290.0], 3, set_difficulty)
                self.buttons.add_instance("Gamemode: Survival", [440.0, 340.0], 3, set_gamemode)
                self.buttons.add_instance("Create World", [440.0, 440.0], 3, self.game_init)

        self.buttons.clear()
        self.buttons.add_instance("Difficulty: Normal", [440.0, 290.0], 3, set_difficulty)
        self.buttons.add_instance("Gamemode: Survival", [440.0, 340.0], 3, set_gamemode)
        self.buttons.add_instance("Create World", [440.0, 440.0], 3, self.game_init)

    def load_game_menu(self):
        self.buttons.clear()
    # endregion

    def game_init(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.mouse_visibility = False
        self.new_game = True
        self.in_menu = False
        self.in_game = False
        self.paused = False
        self.player.jumping = False
        self.player.crouching = False
        self.highlighted = None
        self.player.air_vel = 0
        self.buttons.clear()

        # region Instructions
        self.text.remove_text("New Game", [565.0, 300.0, -0.3], 3)
        self.text.remove_text("Quit", [610.0, 350.0, -0.3], 3)
        self.text.add_text("Controls:", [200.0, 280.0, -0.4], 4)
        self.text.add_text("* W - Walk forwards", [220.0, 340.0 - 10.0, -0.4], 2)
        self.text.add_text("* A - Walk backwards", [220.0, 360.0 - 10.0, -0.4], 2)
        self.text.add_text("* S - Walk to the left", [220.0, 380.0 - 10.0, -0.4], 2)
        self.text.add_text("* D - Walk to the right", [220.0, 400.0 - 10.0, -0.4], 2)
        self.text.add_text("* Left Mouse Button - Break the highlighted block", [220.0, 420.0 - 10.0, -0.4], 2)
        self.text.add_text("* Right Mouse Button - Place at side of highlighted block", [220.0, 440.0 - 10.0, -0.4], 2)
        self.text.add_text("* Space - Jump", [220.0, 460.0 - 10.0, -0.4], 2)
        self.text.add_text("* Shift - Crouch", [220.0, 480.0 - 10.0, -0.4], 2)
        self.text.add_text("* 1 to 9 - Switch which slot is active in the hotbar or action bar",
                           [220.0, 500.0 - 10.0, -0.4], 2)
        self.text.add_text("* E - Access inventory", [220.0, 520.0 - 10.0, -0.4], 2)
        self.text.add_text("* Esc - Pause game and open menu", [220.0, 540.0 - 10.0, -0.4], 2)
        self.text.add_text("* P - Respawn at starting position", [220.0, 560.0 - 10.0, -0.4], 2)
        self.text.add_text("Loading...", [548.0, 600.0, -0.4], 4)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for vao in self.vaos_2d:
            active = True
            if ("inventory" in vao and not self.in_inventory) or (vao == "paused" and not self.paused) or \
                    ("button" in vao and not self.in_menu) or ("cross" in vao and not self.in_game) or \
                    ("bar" in vao and not self.in_game and "inventory" not in vao):
                active = False
            if active:
                if self.vaos_2d[vao].transform is not None:
                    glBindVertexArray(self.vaos_2d[vao].vao)
                    glBindTexture(GL_TEXTURE_2D, self.vaos_2d[vao].texture)
                    glDrawElementsInstanced(
                        GL_TRIANGLES, len(self.vaos_2d[vao].index), GL_UNSIGNED_INT, None,
                        int(len(self.vaos_2d[vao].transform))
                    )
                    glBindTexture(GL_TEXTURE_2D, 0)
                    glBindVertexArray(0)
        glfw.swap_buffers(self.window)
        # endregion

        self.load_textures()

        # region World Initialization
        # time_b = time.time()
        self.world.clear()
        b = random.randint(0, 1024)
        self.y_values.fill(0)
        for x in range(1024):
            for y in range(1024):
                self.y_values[x, y] = int(noise.pnoise2(
                    x / 100.0, y / 100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=b
                ) * 100 + 60)
        self.rendered_chunks.clear()
        self.chunk_load.clear()
        empty_array = numpy.array([], dtype=numpy.float32)
        self.transform = {"bedrock": {side: empty_array for side in range(1, 7)},
                          "stone": {side: empty_array for side in range(1, 7)},
                          "dirt": {side: empty_array for side in range(1, 7)},
                          "grass": {side: empty_array for side in range(1, 7)}}
        for cube in self.vaos_3d:
            for side in self.vaos_3d[cube].sides:
                if cube in self.transform and self.transform[cube][side] is not None:
                    self.vaos_3d[cube].sides[side].transform_update(self.transform[cube][side].copy())
        if self.updating is None:
            self.updating = Thread(target=self.update_chunks, daemon=True)
            self.updating.start()
        # self.update_chunks()
        # endregion

        self.text.remove_text("Loading...", [548.0, 600.0, -0.4], 4)
        self.text.add_text("Press any key to continue", [380.0, 600.0, -0.4], 4)

    def do_movement(self, time_s):
        net_movement = 4.317 * time_s
        if self.keys[glfw.KEY_W]:
            if (self.player.sprint_delay > 0 and not self.player.holding_walk) or self.keys[glfw.KEY_LEFT_CONTROL]:
                self.player.sprinting = True
            elif self.player.sprint_delay == 0 and not self.player.holding_walk:
                self.player.sprint_delay = 0.25
            self.player.holding_walk = True
            if self.player.flying:
                if self.player.sprinting:
                    self.player.process_keyboard("FRONT", net_movement * 5.0)
                else:
                    self.player.process_keyboard("FRONT", net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("FRONT", net_movement * 0.3)
            else:
                if self.player.sprinting:
                    self.player.process_keyboard("FRONT", net_movement * 1.3)
                else:
                    self.player.process_keyboard("FRONT", net_movement)
        else:
            self.player.holding_walk = False
            self.player.sprinting = False
        if self.keys[glfw.KEY_A]:
            if self.player.flying:
                self.player.process_keyboard("SIDE", -net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("SIDE", -net_movement * 0.3)
            else:
                self.player.process_keyboard("SIDE", -net_movement)
        if self.keys[glfw.KEY_S]:
            if self.player.flying:
                self.player.process_keyboard("FRONT", -net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("FRONT", -net_movement * 0.3)
            else:
                self.player.process_keyboard("FRONT", -net_movement)
        if self.keys[glfw.KEY_D]:
            if self.player.flying:
                self.player.process_keyboard("SIDE", net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("SIDE", net_movement * 0.3)
            else:
                self.player.process_keyboard("SIDE", net_movement)
        if self.keys[glfw.KEY_SPACE]:
            if self.player.fly_delay > 0 and not self.player.holding_jump:
                self.player.flying = not self.player.flying
                self.player.air_vel = 0
            elif self.player.fly_delay == 0 and not self.player.holding_jump:
                self.player.fly_delay = 0.25
            self.player.holding_jump = True
            x, y, z = self.player.pos
            if not self.player.jumping and not self.player.flying and not self.check_pos((x, numpy.ceil(y - 1), z)):
                self.player.air_vel = 8.95142
                self.player.air_vel -= 32 * time_s
                self.player.air_vel += 0.4 * self.player.air_vel * time_s  # This is drag
                self.player.process_keyboard("UP", self.player.air_vel * time_s)
                self.player.jumping = True
            if self.player.flying:
                self.player.process_keyboard("UP", net_movement * 2)
        else:
            self.player.holding_jump = False
        if self.keys[glfw.KEY_LEFT_SHIFT]:
            if not self.player.crouching:
                self.player.pos[1] -= 0.3
                self.player.crouching = True
            if self.player.flying:
                self.player.process_keyboard("UP", -net_movement * 2)
        elif self.player.crouching:
            self.player.pos[1] += 0.3
            self.player.crouching = False
        cx, cy, cz = self.player.pos
        if self.player.crouching:
            cy += 0.3
        if self.check_pos((cx, int(numpy.ceil(cy - 1)), cz)) and not self.player.flying:
            self.player.air_vel -= 32 * time_s
            self.player.air_vel += 0.4 * self.player.air_vel * time_s  # This is drag
            if self.check_pos((cx, int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), cz)):
                if self.check_pos((cx, int(numpy.ceil(cy + 1.8 + self.player.air_vel * time_s - 1)), cz)):
                    self.player.process_keyboard("UP", self.player.air_vel * time_s)
                else:  # todo doesn't feel like minecraft, but might be okay/better
                    if not self.player.crouching:
                        self.player.pos[1] = int(self.player.pos[1]) + 0.2
                    else:
                        self.player.pos[1] = int(self.player.pos[1]) - 0.2
                    self.player.air_vel = 0
            else:
                if not self.player.crouching:
                    self.player.pos[1] = round(self.player.pos[1])
                else:
                    self.player.pos[1] = round(self.player.pos[1]) - 0.3
                self.player.air_vel = 0
                self.player.jumping = False
                self.player.flying = False
        elif not self.check_pos((cx, int(numpy.ceil(cy - 1)), cz)):
            if not self.player.crouching:
                self.player.pos[1] = round(self.player.pos[1])
            else:
                self.player.pos[1] = round(self.player.pos[1]) - 0.3
            self.player.air_vel = 0
            self.player.jumping = False
            self.player.flying = False
        elif not self.check_pos((cx, int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), cz)):
            if not self.player.crouching:
                self.player.pos[1] = int(self.player.pos[1]) + 0.2
            else:
                self.player.pos[1] = int(self.player.pos[1]) - 0.2
        if self.player.sprint_delay > 0:
            self.player.sprint_delay -= time_s
        else:
            self.player.sprint_delay = 0
        if self.player.fly_delay > 0:
            self.player.fly_delay -= time_s
        else:
            self.player.fly_delay = 0
        if self.player.pos[1] < -64 and self.in_game:
            x, z = int(self.player.pos[0]) + 512, int(self.player.pos[2]) + 512
            self.player.pos = pyrr.Vector3([0.3, self.y_values[x, z] + 1, 0.3])
        player_chunk = int(App.check_value(self.player.pos[0] / 16, 0)), int(App.check_value(self.player.pos[2] / 16, 0))
        if player_chunk != self.old_player_chunk:
            Thread(target=self.update_chunks).start()
        self.old_player_chunk = player_chunk[:]
        # self.update_chunks()

    def update_chunks(self):   # todo polish the procedural generation a bit more before moving on
        if self.in_game:
            nearby_chunks = self.nearby_chunks.copy()
            player_chunk = int(App.check_value(self.player.pos[0] / 16, 0)), int(App.check_value(self.player.pos[2] / 16, 0))
            self.nearby_chunks = [(x, z) for x in range(player_chunk[0] - 3, player_chunk[0] + 4)
                                  for z in range(player_chunk[1] - 3, player_chunk[1] + 4)]
            for cx, cz in self.nearby_chunks:
                if (cx, cz) not in self.world:
                    self.chunk_load[(cx, cz)] = (cx - 1, cz), (cx, cz - 1), (cx + 1, cz), (cx, cz + 1), (cx, cz)
                    self.world[(cx, cz)] = numpy.zeros((16, 256, 16, 7), dtype=numpy.float32)
                    self.world[(cx, cz)][:, 0, :, 0] = 7
                    low_y = numpy.min(self.y_values[cx * 16 + 512: cx * 16 + 528, cz * 16 + 512: cz * 16 + 528]) - 5
                    self.world[(cx, cz)][:, 1: low_y, :, 0] = 1
                    for x in range(16):
                        for z in range(16):
                            for y in range(low_y, self.y_values[cx * 16 + x + 512][cz * 16 + z + 512] - 5):
                                self.world[(cx, cz)][x, y, z, 0] = 1
                            for y in range(self.y_values[cx * 16 + x + 512][cz * 16 + z + 512] - 5, self.y_values[cx * 16 + x + 512][cz * 16 + z + 512]):
                                self.world[(cx, cz)][x, y, z, 0] = 3
                            self.world[(cx, cz)][x, self.y_values[cx * 16 + x + 512][cz * 16 + z + 512], z, 0] = 2
            while self.chunk_load:  # todo minecraft seems to do batched rendering (while self.chunk_load:)
                cx, cz = list(self.chunk_load)[0]
                if (cx, cz) in self.world:
                    test_pos = numpy.nonzero((self.world[(cx, cz)][:, :-1, :, 0] != 0) & (self.world[(cx, cz)][:, 1:, :, 0] == 0))
                    self.world[(cx, cz)][test_pos[0], test_pos[1], test_pos[2], 4] = 1
                    test_pos = numpy.nonzero((self.world[(cx, cz)][:, :, :-1, 0] != 0) & (self.world[(cx, cz)][:, :, 1:, 0] == 0))
                    self.world[(cx, cz)][test_pos[0], test_pos[1], test_pos[2], 6] = 1
                    test_pos = numpy.nonzero((self.world[(cx, cz)][:, :, 1:, 0] != 0) & (self.world[(cx, cz)][:, :, :-1, 0] == 0))
                    self.world[(cx, cz)][test_pos[0], test_pos[1], test_pos[2] + 1, 5] = 1
                    test_pos = numpy.nonzero((self.world[(cx, cz)][:-1, :, :, 0] != 0) & (self.world[(cx, cz)][1:, :, :, 0] == 0))
                    self.world[(cx, cz)][test_pos[0], test_pos[1], test_pos[2], 2] = 1
                    test_pos = numpy.nonzero((self.world[(cx, cz)][1:, :, :, 0] != 0) & (self.world[(cx, cz)][:-1, :, :, 0] == 0))
                    self.world[(cx, cz)][test_pos[0] + 1, test_pos[1], test_pos[2], 1] = 1
                    # print(self.y_values[cx * 16 + 512: cx * 16 + 528, cz * 16 + 512: cz * 16 + 528])
                    for x_z in range(4):  # todo redo this part; still slower than it has to be!
                        for axis in range(16):
                            if x_z == 0:
                                x = axis
                                z = 0
                            elif x_z == 1:
                                x = axis
                                z = 15
                            elif x_z == 2:
                                x = 0
                                z = axis
                            else:
                                x = 15
                                z = axis
                            y_start = numpy.min(self.y_values[cx * 16 + x + 511: cx * 16 + x + 514,
                                                cz * 16 + z + 511: cz * 16 + z + 514]) + 1
                            y_end = numpy.max(self.y_values[cx * 16 + x + 511: cx * 16 + x + 514,
                                              cz * 16 + z + 511: cz * 16 + z + 514]) + 1
                            if y_start == y_end:
                                y_end += 1
                            for y in range(y_start, y_end):
                                if self.world[(cx, cz)][x, y, z, 0] == 0:
                                    pos = x, y, z
                                    o_pos_dict = {
                                        1: [pos[0] + 1, *pos[1:]],  # right
                                        2: [pos[0] - 1, *pos[1:]],  # left
                                        3: [pos[0], pos[1] + 1, pos[2]],  # top
                                        4: [pos[0], pos[1] - 1, pos[2]],  # bottom
                                        5: [*pos[0:2], pos[2] + 1],  # front
                                        6: [*pos[0:2], pos[2] - 1]  # back
                                    }
                                    for o_pos in o_pos_dict:
                                        if o_pos_dict[o_pos][0] < 0 or o_pos_dict[o_pos][0] >= 16 or \
                                                o_pos_dict[o_pos][2] < 0 or o_pos_dict[o_pos][2] >= 16:
                                            x_bool = False
                                            z_bool = False
                                            if o_pos_dict[o_pos][0] < 0 or o_pos_dict[o_pos][0] >= 16:
                                                o_pos_dict[o_pos][0] %= 16
                                                x_bool = True
                                            if o_pos_dict[o_pos][2] < 0 or o_pos_dict[o_pos][2] >= 16:
                                                o_pos_dict[o_pos][2] %= 16
                                                z_bool = True
                                            if o_pos_dict[o_pos][0] == 0 and x_bool:
                                                nearby_chunk = [cx + 1]
                                            elif o_pos_dict[o_pos][0] == 15 and x_bool:
                                                nearby_chunk = [cx - 1]
                                            else:
                                                nearby_chunk = [cx]
                                            if o_pos_dict[o_pos][2] == 0 and z_bool:
                                                nearby_chunk.append(cz + 1)
                                            elif o_pos_dict[o_pos][2] == 15 and z_bool:
                                                nearby_chunk.append(cz - 1)
                                            else:
                                                nearby_chunk.append(cz)
                                            nearby_chunk = tuple(nearby_chunk)
                                            if nearby_chunk in self.world and self.world[nearby_chunk][o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][2], 0]:
                                                self.world[nearby_chunk][o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][2], o_pos] = 1
                                        elif self.world[(cx, cz)][o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][2], 0]:
                                            self.world[(cx, cz)][o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][2], o_pos] = 1
                    # self.update = True
                    self.rendered_chunks[(cx, cz)] = dict()
                    for block in [2, 3]:
                        block_name = BLOCK_DICT[block]
                        for side in range(1, 7):
                            new_pos = numpy.array(list(zip(*numpy.nonzero((self.world[(cx, cz)][:, :, :, 0] == block) &
                                                                          (self.world[(cx, cz)][:, :, :, side] == 1)))), dtype=numpy.float32)
                            if len(new_pos) > 0:
                                new_pos[:, 0] += cx * 16
                                new_pos[:, 2] += cz * 16
                                new_transform = numpy.array([self.default_matrix] * len(new_pos), dtype=numpy.float32)
                                new_transform[:, 3, : 3] += new_pos
                                # if self.transform[block_name][side] is not None and \
                                #         len(self.transform[block_name][side]) > 0:
                                #     self.transform[block_name][side] = \
                                #         numpy.append(self.transform[block_name][side], new_transform, 0)
                                # else:
                                #     self.transform[block_name][side] = new_transform.copy()
                                if block_name not in self.rendered_chunks[(cx, cz)]:
                                    empty_array = numpy.array([], dtype=numpy.float32)
                                    self.rendered_chunks[(cx, cz)][block_name] = {side: empty_array for side in range(1, 7)}
                                if len(self.rendered_chunks[(cx, cz)][block_name][side]) > 0:
                                    self.rendered_chunks[(cx, cz)][block_name][side] = \
                                        numpy.append(self.rendered_chunks[(cx, cz)][block_name][side], new_transform, 0)
                                else:
                                    self.rendered_chunks[(cx, cz)][block_name][side] = new_transform.copy()
                for ux, uz in self.chunk_load[(cx, cz)]:
                    if (ux, uz) in self.rendered_chunks:
                        for x_z in range(4):  # todo redo this part; still slower than it has to be!
                            for axis in range(16):
                                x = axis if x_z == 0 or x_z == 1 else 0 if x_z == 2 else 15
                                z = 0 if x_z == 0 else 15 if x_z == 1 else axis
                                y_start = numpy.min(self.y_values[ux * 16 + x + 511: ux * 16 + x + 514,
                                                    uz * 16 + z + 511: uz * 16 + z + 514]) + 1
                                y_end = numpy.max(self.y_values[ux * 16 + x + 511: ux * 16 + x + 514,
                                                  uz * 16 + z + 511: uz * 16 + z + 514]) + 1
                                if y_start == y_end:
                                    y_end += 1
                                for y in range(y_start, y_end):
                                    if self.world[(ux, uz)][x, y, z, 0] == 0:
                                        pos = x, y, z
                                        o_pos_dict = {
                                            1: [pos[0] + 1, *pos[1:]],  # right
                                            2: [pos[0] - 1, *pos[1:]],  # left
                                            3: [pos[0], pos[1] + 1, pos[2]],  # top
                                            4: [pos[0], pos[1] - 1, pos[2]],  # bottom
                                            5: [*pos[0:2], pos[2] + 1],  # front
                                            6: [*pos[0:2], pos[2] - 1]  # back
                                        }
                                        for o_pos in o_pos_dict:
                                            if o_pos_dict[o_pos][0] < 0 or o_pos_dict[o_pos][0] >= 16 or \
                                                    o_pos_dict[o_pos][2] < 0 or o_pos_dict[o_pos][2] >= 16:
                                                x_bool = False
                                                z_bool = False
                                                if o_pos_dict[o_pos][0] < 0 or o_pos_dict[o_pos][0] >= 16:
                                                    o_pos_dict[o_pos][0] %= 16
                                                    x_bool = True
                                                if o_pos_dict[o_pos][2] < 0 or o_pos_dict[o_pos][2] >= 16:
                                                    o_pos_dict[o_pos][2] %= 16
                                                    z_bool = True
                                                if o_pos_dict[o_pos][0] == 0 and x_bool:
                                                    nearby_chunk = [ux + 1]
                                                elif o_pos_dict[o_pos][0] == 15 and x_bool:
                                                    nearby_chunk = [ux - 1]
                                                else:
                                                    nearby_chunk = [ux]
                                                if o_pos_dict[o_pos][2] == 0 and z_bool:
                                                    nearby_chunk.append(uz + 1)
                                                elif o_pos_dict[o_pos][2] == 15 and z_bool:
                                                    nearby_chunk.append(uz - 1)
                                                else:
                                                    nearby_chunk.append(uz)
                                                nearby_chunk = tuple(nearby_chunk)
                                                if nearby_chunk in self.world and self.world[nearby_chunk][
                                                    o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][
                                                        2], 0]:
                                                    self.world[nearby_chunk][
                                                        o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][
                                                            2], o_pos] = 1
                                            elif self.world[(ux, uz)][
                                                o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][2], 0]:
                                                self.world[(ux, uz)][
                                                    o_pos_dict[o_pos][0], o_pos_dict[o_pos][1], o_pos_dict[o_pos][
                                                        2], o_pos] = 1
                        for block in [2, 3]:
                            block_name = BLOCK_DICT[block]
                            for side in range(1, 7):
                                new_pos = numpy.array(list(zip(*numpy.nonzero((self.world[(ux, uz)][:, :, :, 0] == block) &
                                                                              (self.world[(ux, uz)][:, :, :, side] == 1)))),
                                                      dtype=numpy.float32)
                                if len(new_pos) > 0:
                                    new_pos[:, 0] += ux * 16
                                    new_pos[:, 2] += uz * 16
                                    new_transform = numpy.array([self.default_matrix] * len(new_pos), dtype=numpy.float32)
                                    new_transform[:, 3, : 3] += new_pos
                                    # if self.transform[block_name][side] is not None and \
                                    #         len(self.transform[block_name][side]) > 0:
                                    #     self.transform[block_name][side] = \
                                    #         numpy.append(self.transform[block_name][side], new_transform, 0)
                                    # else:
                                    #     self.transform[block_name][side] = new_transform.copy()
                                    if block_name not in self.rendered_chunks[(ux, uz)]:
                                        empty_array = numpy.array([], dtype=numpy.float32)
                                        self.rendered_chunks[(ux, uz)][block_name] = {side: empty_array for side in range(1, 7)}
                                    if len(self.rendered_chunks[(ux, uz)][block_name][side]) > 0:
                                        self.rendered_chunks[(ux, uz)][block_name][side] = \
                                            numpy.append(self.rendered_chunks[(ux, uz)][block_name][side], new_transform, 0)
                                    else:
                                        self.rendered_chunks[(ux, uz)][block_name][side] = new_transform.copy()
                # if chunk not in nearby_chunks and self.rendered_chunks[chunk][1]:
                    #     self.rendered_chunks[chunk][1] = False
                    #     for block_name in self.rendered_chunks[chunk][0]:
                    #         for side in self.rendered_chunks[chunk][0][block_name]:
                    #             if len(self.rendered_chunks[chunk][0][block_name][side]) > 0:
                    #                 for x, y, z in self.rendered_chunks[chunk][0][block_name][side][:, 3, : 3]:
                    #                     self.transform[block_name][side] = numpy.delete(
                    #                         self.transform[block_name][side],
                    #                         numpy.nonzero(
                    #                             (self.transform[block_name][side][:, 3, 0] == x) &
                    #                             (self.transform[block_name][side][:, 3, 1] == y) &
                    #                             (self.transform[block_name][side][:, 3, 2] == z)
                    #                         ), 0
                    #                     )
                    #     break  # todo can probably be removed when I've shorten the time it takes to unload
                # self.update = True
                del self.chunk_load[(cx, cz)]
            if nearby_chunks != self.nearby_chunks:
                self.update = True

    def load_textures(self):
        self.vaos_3d["grass"] = Block(["textures/grass.png"] * 4 + ["textures/dirt.png"] + ["textures/grass_top.png"])
        self.vaos_3d["grass_item"] = Block(
            ["textures/grass.png"] * 4 + ["textures/dirt.png"] + ["textures/grass_top.png"], True
        )
        for block in os.listdir("./textures"):
            if block[0] != "_" and "grass" not in block and "oak_log" not in block:
                self.vaos_3d[block.split(".")[0]] = Block([f"textures/{block}"] * 6)
                self.vaos_3d[f"{block.split('.')[0]}_item"] = Block([f"textures/{block}"] * 6, True)
        self.vaos_2d["crosshair_v"] = Entity(
            CROSSHAIR_V, INDICES, "textures/_white.png", numpy.array([pyrr.matrix44.create_from_translation([624.0, 344.0, -0.6])], dtype=numpy.float32)
        )
        self.vaos_2d["crosshair_h"] = Entity(
            CROSSHAIR_H, INDICES, "textures/_white.png", numpy.array([pyrr.matrix44.create_from_translation([624.0, 344.0, -0.6])], dtype=numpy.float32)
        )
        self.vaos_2d["hotbar"] = Entity(
            HOTBAR, INDICES, "textures/_hotbar.png", numpy.array([pyrr.matrix44.create_from_translation([458.0, 676.0, -0.7])], dtype=numpy.float32)
        )
        self.vaos_2d["active_bar"] = Entity(
            ACTIVE_BAR, INDICES, "textures/_active_bar.png", numpy.array([pyrr.matrix44.create_from_translation([456.0, 674.0, -0.6])], dtype=numpy.float32)
        )
        for i in range(1, 10):
            self.vaos_2d[f"hotbar_{i}"] = Entity(
                HOTBAR_ICON, INDICES, "textures/_tp.png",
                numpy.array([pyrr.matrix44.create_from_translation([424.0 + i * 40, 682.0, -0.6])], dtype=numpy.float32)
            )
            self.vaos_2d[f"inventory_hotbar_slot_{i}"] = Entity(
                HOTBAR_ICON, INDICES, "textures/_tp.png",
                numpy.array([pyrr.matrix44.create_from_translation([444.0 + i * 36, 430.0, -0.3])], dtype=numpy.float32)
            )
        for i in range(1, 28):
            self.vaos_2d[f"inventory_slot_{i}"] = Entity(
                HOTBAR_ICON, INDICES, "textures/_tp.png",
                numpy.array([pyrr.matrix44.create_from_translation([480.0 + ((i - 1) % 9) * 36, 314.0 + int((i - 1) / 9) * 36, -0.3])], dtype=numpy.float32)
            )
        self.selected_block = self.vaos_2d["hotbar_1"].texture_name
        self.vaos_2d["inventory"] = Entity(
            INVENTORY, INDICES, "textures/_crafting_table.png", numpy.array([pyrr.matrix44.create_from_translation([464.0, 146.0, -0.3])], dtype=numpy.float32)
        )
        self.vaos_2d["active_inventory_slot"] = Entity(HOTBAR_ICON, INDICES, "textures/_white_tp.png")
        self.vaos_2d["paused"] = Entity(
            SCREEN, INDICES, "textures/_black_tp.png", numpy.array([pyrr.matrix44.create_from_translation([0.0, 0.0, -0.4])], dtype=numpy.float32)
        )
        self.vaos_2d["mouse_inventory"] = Entity(HOTBAR_ICON, INDICES, "textures/_tp.png")

    def check_pos(self, pos, check_crouch=False):
        x, y, z = pos
        if self.player.crouching:
            y += 0.3
        if 0 < y < 254:
            current_chunk = int(self.check_value(x / 16, 0)), int(self.check_value(z / 16, 0))
            crouch_counter = 0
            for i1, i2 in {(-.3, -.3), (-.3, .3), (.3, -.3), (.3, .3)}:
                ix, iy, iz = int(self.check_value(x % 16 + i1, 0)), y, int(self.check_value(z % 16 + i2, 0))
                x_bool = False
                z_bool = False
                if ix < 0 or ix >= 16:
                    ix %= 16
                    x_bool = True
                if iz < 0 or iz >= 16:
                    iz %= 16
                    z_bool = True
                if ix == 0 and x_bool:
                    nearby_chunk = [current_chunk[0] + 1]
                elif ix == 15 and x_bool:
                    nearby_chunk = [current_chunk[0] - 1]
                else:
                    nearby_chunk = [current_chunk[0]]
                if iz == 0 and z_bool:
                    nearby_chunk.append(current_chunk[1] + 1)
                elif iz == 15 and z_bool:
                    nearby_chunk.append(current_chunk[1] - 1)
                else:
                    nearby_chunk.append(current_chunk[1])
                nearby_chunk = tuple(nearby_chunk)
                if nearby_chunk in self.world:
                    if self.world[nearby_chunk][ix, int(iy), iz, 0] != 0:
                        return False
                    if check_crouch and self.player.crouching and not self.player.flying and not self.player.jumping \
                            and self.world[nearby_chunk][ix, int(iy - 1), iz, 0] == 0:
                        crouch_counter += 1
            if crouch_counter >= 4:
                return False
        return True

    def mouse_button_check(self, time_s):
        if self.highlighted is not None:
            mouse_buttons = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT), \
                            glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT)
            cx, cy, cz = tuple(self.highlighted[3, :3])
            chunk = [int(self.check_value(cx / 16, 0)), int(self.check_value(cz / 16, 0))]
            if cx < 0 and cx % 16 == 0:
                chunk[0] += 1
            if cz < 0 and cz % 16 == 0:
                chunk[1] += 1
            chunk = tuple(chunk)
            break_s = self.check_hardness(BLOCK_DICT[self.world[chunk][int(cx % 16), int(cy), int(cz % 16), 0]])
            if self.player.breaking and \
                    (self.highlighted is None or not numpy.array_equal(self.breaking_block, self.highlighted)):
                self.player.break_delay = 1
                self.breaking_block = self.highlighted
            if mouse_buttons[0]:
                if not self.mouse_visibility and self.highlighted is not None:
                    if not self.player.breaking:
                        self.player.break_delay = 1
                        self.player.breaking = True
                        self.breaking_block = self.highlighted
                    if self.player.break_delay <= 0 and self.player.breaking:
                        self.blocks_remove([(chunk, (cx, cy, cz))], time_s)
                        self.highlighted = None
                        self.breaking_block = None
                        self.player.breaking = False
                else:
                    self.player.breaking = False
            else:
                self.player.breaking = False
            if mouse_buttons[1]:  # todo still broken | UPDATE (10/06/2020): fixed? I changed stuff, but idk if there's bugs
                if not self.mouse_visibility and self.highlighted is not None and self.player.place_delay <= 0:
                    new_block = self.block_face()
                    chunk = [int(self.check_value(new_block[0] / 16, 0)), int(self.check_value(new_block[2] / 16, 0))]
                    if new_block[0] < 0 and new_block[0] % 16 == 0:
                        chunk[0] += 1
                    if new_block[2] < 0 and new_block[2] % 16 == 0:
                        chunk[1] += 1
                    chunk = tuple(chunk)
                    x, y, z = self.player.pos
                    if self.player.crouching:
                        y += 0.3
                    x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
                    player_hitbox = ((int(x), int(y), int(z)),
                                     (int(x), int(y + 1), int(z)),
                                     (int(x), int(y + 1.8), int(z)),
                                     (int(x + 0.3), int(y), int(z + 0.3)),
                                     (int(x + 0.3), int(y), int(z - 0.3)),
                                     (int(x - 0.3), int(y), int(z + 0.3)),
                                     (int(x - 0.3), int(y), int(z - 0.3)),
                                     (int(x + 0.3), int(y + 1), int(z + 0.3)),
                                     (int(x + 0.3), int(y + 1), int(z - 0.3)),
                                     (int(x - 0.3), int(y + 1), int(z + 0.3)),
                                     (int(x - 0.3), int(y + 1), int(z - 0.3)),
                                     (int(x + 0.3), int(y + 1.8), int(z + 0.3)),
                                     (int(x + 0.3), int(y + 1.8), int(z - 0.3)),
                                     (int(x - 0.3), int(y + 1.8), int(z + 0.3)),
                                     (int(x - 0.3), int(y + 1.8), int(z - 0.3)))
                    if new_block not in self.world and new_block not in player_hitbox and \
                            self.selected_block not in [None, "_tp"]:
                        if self.player.gamemode == "Survival":
                            self.inventory_remove(["hotbar", self.active_bar], self.selected_block)
                        self.player.place_delay = 0.25
                        self.blocks_add([(chunk, new_block)])
            else:
                self.player.place_delay = 0
            self.player.place_delay -= time_s if self.player.place_delay > 0 else 0
            self.player.break_delay -= time_s / break_s if self.player.breaking else 0

    def inventory_add(self, item):
        """
        :param item: name of block
        """
        ci = numpy.concatenate((self.player.hotbar, self.player.inventory))
        inventory_items = [BLOCK_DICT[ci[x, 0]] for x in numpy.nonzero((ci[:, 0] != 0) & (ci[:, 1] < 64))[0]]
        for i in range(1, 10):
            if self.player.hotbar[i - 1, 0] == 0 and item not in inventory_items:
                self.player.hotbar[i - 1] = [BLOCK_IDS[item], 1]
                self.vaos_2d[f"hotbar_{i}"].texture_name = item
                self.vaos_2d[f"hotbar_{i}"].texture = Entity.load_texture(f"textures/{item}.png")
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture_name = item
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture = Entity.load_texture(f"textures/{item}.png")
                self.text.add_text("1", [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.add_text("1", [444.0 + i * 36, 430.0, -0.1], 2, True)
                if i == self.active_bar:
                    self.selected_block = self.vaos_2d[f"hotbar_{i}"].texture_name
                return
            elif self.player.hotbar[i - 1, 0] != 0 and \
                    self.player.hotbar[i - 1, 0] == BLOCK_IDS[item] and self.player.hotbar[i - 1, 1] < 64:
                self.text.remove_text(str(int(self.player.hotbar[i - 1, 1])), [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.remove_text(str(int(self.player.hotbar[i - 1, 1])), [444.0 + i * 36, 430.0, -0.1], 2, True)
                self.player.hotbar[i - 1, 1] += 1
                self.text.add_text(str(int(self.player.hotbar[i - 1, 1])), [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.add_text(str(int(self.player.hotbar[i - 1, 1])), [444.0 + i * 36, 430.0, -0.1], 2, True)
                return
        for i in range(1, 28):
            if self.player.inventory[i - 1, 0] == 0 and item not in inventory_items:
                self.player.inventory[i - 1] = [item, 1]
                self.vaos_2d[f"inventory_slot_{i}"].texture_name = item
                self.vaos_2d[f"inventory_slot_{i}"].texture = Entity.load_texture(f"textures/{item}.png")
                self.text.add_text("1", [480.0 + ((i - 1) % 9) * 36, 314.0 + int((i - 1) / 9) * 36, -0.1], 2, True)
                return
            elif self.player.inventory[i - 1, 0] != 0 and \
                    self.player.inventory[i - 1, 0] == BLOCK_IDS[item] and self.player.inventory[i - 1, 1] < 64:
                self.text.remove_text(str(int(self.player.inventory[i - 1, 1])),
                                      [480.0 + ((i - 1) % 9) * 36, 314.0 + int((i - 1) / 9) * 36, -0.1], 2, True)
                self.player.inventory[i - 1, 1] += 1
                self.text.add_text(str(int(self.player.inventory[i - 1][1])),
                                   [480.0 + ((i - 1) % 9) * 36, 314.0 + int((i - 1) / 9) * 36, -0.1], 2, True)
                return

    def inventory_remove(self, pos, item):
        """
        :param pos: hotbar or inventory, and location in whichever
        :param item: name of block
        """
        area, i = pos
        if area == "hotbar":
            if self.player.hotbar[i - 1, 0] == BLOCK_IDS[item] and self.player.hotbar[i - 1, 1] > 1:
                self.text.remove_text(str(int(self.player.hotbar[i - 1][1])), [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.remove_text(str(int(self.player.hotbar[i - 1][1])), [444.0 + i * 36, 430.0, -0.1], 2, True)
                self.player.hotbar[i - 1, 1] -= 1
                self.text.add_text(str(int(self.player.hotbar[i - 1, 1])), [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.add_text(str(int(self.player.hotbar[i - 1, 1])), [444.0 + i * 36, 430.0, -0.1], 2, True)
            elif self.player.hotbar[i - 1][0] == BLOCK_IDS[item] and self.player.hotbar[i - 1, 1] == 1:
                self.text.remove_text(str(int(self.player.hotbar[i - 1, 1])), [424.0 + i * 40, 682.0, -0.5], 2)
                self.text.remove_text(str(int(self.player.hotbar[i - 1, 1])), [444.0 + i * 36, 430.0, -0.1], 2, True)
                self.player.hotbar[i - 1] = [0, 0]
                self.vaos_2d[f"hotbar_{i}"].texture_name = None
                self.vaos_2d[f"hotbar_{i}"].texture = Entity.load_texture(f"textures/_tp.png")
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture_name = None
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture = Entity.load_texture(f"textures/_tp.png")
        elif area == "inventory":
            if self.player.inventory[i - 1, 0] == BLOCK_IDS[item] and self.player.inventory[i - 1, 1] > 1:
                self.text.remove_text(str(int(self.player.inventory[i - 1, 1])), [424.0 + i * 40, 682.0, -0.1], 2)
                self.player.inventory[i - 1][1] -= 1
                self.text.add_text(str(int(self.player.inventory[i - 1, 1])), [424.0 + i * 40, 682.0, -0.1], 2)
            elif self.player.hotbar[i - 1, 0] == BLOCK_IDS[item] and self.player.hotbar[i - 1, 1] == 1:
                self.text.remove_text(str(int(self.player.inventory[i - 1, 1])), [424.0 + i * 40, 682.0, -0.1], 2)
                self.player.inventory[i - 1] = [0, 0]
                self.vaos_2d[f"inventory_slot_{i}"].texture_name = None
                self.vaos_2d[f"inventory_slot_{i}"].texture = Entity.load_texture(f"textures/_tp.png")

    def blocks_add(self, blocks):
        for b_chunk, pos in blocks:
            new_block = pos
            visible_blocks = [1, 1, 1, 1, 1, 1]
            bx, by, bz = new_block
            side_values = {1: (bx + 1, by, bz),
                           3: (bx, by + 1, bz),
                           5: (bx, by, bz + 1),
                           2: (bx - 1, by, bz),
                           4: (bx, by - 1, bz),
                           6: (bx, by, bz - 1)}
            for side in side_values:
                x, y, z = side_values[side]
                chunk = [int(self.check_value(x / 16, 0)), int(self.check_value(z / 16, 0))]
                if x < 0 and x % 16 == 0:
                    chunk[0] += 1
                if z < 0 and z % 16 == 0:
                    chunk[1] += 1
                chunk = tuple(chunk)
                x, y, z = int(x), int(y), int(z)
                if self.world[chunk][x % 16, y, z % 16, 0]:
                    if "ice" not in self.selected_block and "glass" not in self.selected_block:
                        side_block = BLOCK_DICT[self.world[chunk][x % 16, y, z % 16, 0]]
                        self.transform[side_block][side] = numpy.delete(
                            self.transform[side_block][side],
                            numpy.nonzero(
                                (self.transform[side_block][side][:, 3, 0] == x) &
                                (self.transform[side_block][side][:, 3, 1] == y) &
                                (self.transform[side_block][side][:, 3, 2] == z)
                            ), 0
                        )
                        self.rendered_chunks[chunk][side_block][side] = numpy.delete(
                            self.rendered_chunks[chunk][side_block][side],
                            numpy.nonzero(
                                (self.rendered_chunks[chunk][side_block][side][:, 3, 0] == x) &
                                (self.rendered_chunks[chunk][side_block][side][:, 3, 1] == y) &
                                (self.rendered_chunks[chunk][side_block][side][:, 3, 2] == z)
                            ), 0
                        )
                        self.vaos_3d[side_block].sides[side].transform_update(self.transform[side_block][side].copy())
                        if side == 2:
                            visible_blocks[0] = 0
                        elif side == 1:
                            visible_blocks[1] = 0
                        elif side == 4:
                            visible_blocks[2] = 0
                        elif side == 3:
                            visible_blocks[3] = 0
                        elif side == 6:
                            visible_blocks[4] = 0
                        elif side == 5:
                            visible_blocks[5] = 0
            if "ice" not in self.selected_block and "glass" not in self.selected_block and self.highlighted is not None:
                side_value = [int(new_block[axis] - self.highlighted[3, axis]) for axis in range(3)]
                side = 2 if side_value == [1, 0, 0] else 1 if side_value == [-1, 0, 0] \
                    else 4 if side_value == [0, 1, 0] else 3 if side_value == [0, -1, 0] \
                    else 6 if side_value == [0, 0, 1] else 5
                chunk = [int(self.check_value(self.highlighted[3, 0] / 16, 0)),
                         int(self.check_value(self.highlighted[3, 2] / 16, 0))]
                if self.highlighted[3, 0] < 0 and self.highlighted[3, 0] % 16 == 0:
                    chunk[0] += 1
                if self.highlighted[3, 2] < 0 and self.highlighted[3, 2] % 16 == 0:
                    chunk[1] += 1
                chunk = tuple(chunk)
                highlighted_block = BLOCK_DICT[self.world[chunk][int(self.highlighted[3, 0] % 16), int(self.highlighted[3, 1]), int(self.highlighted[3, 2] % 16), 0]]
                self.transform[highlighted_block][side] = numpy.delete(
                    self.transform[highlighted_block][side],
                    numpy.nonzero(
                        (self.transform[highlighted_block][side][:, 3, 0] == self.highlighted[3, 0]) &
                        (self.transform[highlighted_block][side][:, 3, 1] == self.highlighted[3, 1]) &
                        (self.transform[highlighted_block][side][:, 3, 2] == self.highlighted[3, 2])
                    ), 0
                )
                self.rendered_chunks[b_chunk][highlighted_block][side] = numpy.delete(
                    self.rendered_chunks[b_chunk][highlighted_block][side],
                    numpy.nonzero(
                        (self.rendered_chunks[b_chunk][highlighted_block][side][:, 3, 0] == self.highlighted[3, 0]) &
                        (self.rendered_chunks[b_chunk][highlighted_block][side][:, 3, 1] == self.highlighted[3, 1]) &
                        (self.rendered_chunks[b_chunk][highlighted_block][side][:, 3, 2] == self.highlighted[3, 2])
                    ), 0
                )
                self.vaos_3d[highlighted_block].sides[side].transform_update(self.transform[highlighted_block][side].copy())
            self.highlighted = None
            self.world[b_chunk][bx % 16, by, bz % 16] = [BLOCK_IDS[self.selected_block], *visible_blocks]
            for side in numpy.nonzero(self.world[b_chunk][bx % 16, by, bz % 16, 1:])[0] + 1:
                new_transform = numpy.array([pyrr.matrix44.create_from_translation(new_block)], dtype=numpy.float32)
                if len(self.transform[self.selected_block][side]) > 0:
                    self.transform[self.selected_block][side] = numpy.append(
                        self.transform[self.selected_block][side], new_transform, 0
                    )
                else:
                    self.transform[self.selected_block][side] = new_transform.copy()
                if self.selected_block not in self.rendered_chunks[b_chunk]:
                    empty_array = numpy.array([], dtype=numpy.float32)
                    self.rendered_chunks[b_chunk][self.selected_block] = {side: empty_array for side in range(1, 7)}
                if len(self.rendered_chunks[b_chunk][self.selected_block][side]) > 0:
                    self.rendered_chunks[b_chunk][self.selected_block][side] = \
                        numpy.append(self.rendered_chunks[b_chunk][self.selected_block][side], new_transform, 0)
                else:
                    self.rendered_chunks[b_chunk][self.selected_block][side] = new_transform.copy()
                self.vaos_3d[self.selected_block].sides[side].transform_update(self.transform[self.selected_block][side].copy())
            if not self.player.hotbar[self.active_bar - 1, 0]:
                self.selected_block = None

    def blocks_remove(self, blocks, time_s):
        for chunk, pos in blocks:
            cx, cy, cz = pos
            if self.y_values[int(cx) + 512, int(cz) + 512] == cy:
                self.y_values[int(cx) + 512, int(cz) + 512] -= 1
            new_pos = list(pos)
            new_pos[0] += 0.5
            new_pos[1] += (8.95142 / 2) * time_s
            new_pos[2] += 0.5
            block_name = BLOCK_DICT[self.world[chunk][int(cx % 16), int(cy), int(cz % 16), 0]]
            pos_matrix = numpy.dot(pyrr.matrix44.create_from_scale((0.25, 0.25, 0.25)),
                                   pyrr.matrix44.create_from_translation(new_pos))
            item_name = f"{block_name}_item"
            for vao in self.vaos_3d[item_name].sides:
                if self.vaos_3d[item_name].sides[vao].transform is not None:
                    self.vaos_3d[item_name].sides[vao].transform = numpy.append(
                        self.vaos_3d[item_name].sides[vao].transform, numpy.array([pos_matrix], dtype=numpy.float32), 0
                    )
                else:
                    self.vaos_3d[item_name].sides[vao].transform = numpy.array([pos_matrix], dtype=numpy.float32)
                if vao == 4:
                    rx = random.randint(-100, 100) / 100
                    ry = (random.randint(0, 100) / 100) * 8.95142
                    rz = random.randint(-100, 100) / 100
                    if self.vaos_3d[item_name].top.item_data is not None:
                        self.vaos_3d[item_name].top.item_data = numpy.append(
                            self.vaos_3d[item_name].top.item_data,
                            numpy.array([[rx, ry, rz, 1, 0, 0, 0, 0]], dtype=numpy.float32), 0
                        )
                    else:
                        self.vaos_3d[item_name].top.item_data = \
                            numpy.array([[rx, ry, rz, 1, 0, 0, 0, 0]], dtype=numpy.float32)
                self.vaos_3d[item_name].sides[vao].transform_update()
            px, py, pz = pos
            px, py, pz = int(px % 16), int(py), int(pz % 16)
            for side in range(1, 7):
                if len(self.transform[block_name][side]) > 0:
                    self.transform[block_name][side] = numpy.delete(
                        self.transform[block_name][side],
                        numpy.nonzero(
                            (self.transform[block_name][side][:, 3, 0] == pos[0]) &
                            (self.transform[block_name][side][:, 3, 1] == pos[1]) &
                            (self.transform[block_name][side][:, 3, 2] == pos[2])
                        ), 0
                    )
                    self.vaos_3d[block_name].sides[side].transform_update(self.transform[block_name][side].copy())
                if len(self.rendered_chunks[chunk][block_name][side]) > 0:
                    self.rendered_chunks[chunk][block_name][side] = numpy.delete(
                        self.rendered_chunks[chunk][block_name][side],
                        numpy.nonzero(
                            (self.rendered_chunks[chunk][block_name][side][:, 3, 0] == pos[0]) &
                            (self.rendered_chunks[chunk][block_name][side][:, 3, 1] == pos[1]) &
                            (self.rendered_chunks[chunk][block_name][side][:, 3, 2] == pos[2])
                        ), 0
                    )
            self.world[chunk][int(cx % 16), int(cy), int(cz % 16)] = [0] * 7
            side_values = {
                2: (px - 1, py, pz),  # left
                1: (px + 1, py, pz),  # right
                4: (px, py - 1, pz),  # bottom
                3: (px, py + 1, pz),  # top
                6: (px, py, pz - 1),  # back
                5: (px, py, pz + 1)  # front
            }
            for side in side_values:
                x, y, z = side_values[side]
                x_bool = False
                z_bool = False
                if x < 0 or x >= 16:
                    x %= 16
                    x_bool = True
                if z < 0 or z >= 16:
                    z %= 16
                    z_bool = True
                if x == 0 and x_bool:
                    nearby_chunk = [chunk[0] + 1]
                elif x == 15 and x_bool:
                    nearby_chunk = [chunk[0] - 1]
                else:
                    nearby_chunk = [chunk[0]]
                if z == 0 and z_bool:
                    nearby_chunk.append(chunk[1] + 1)
                elif z == 15 and z_bool:
                    nearby_chunk.append(chunk[1] - 1)
                else:
                    nearby_chunk.append(chunk[1])
                nearby_chunk = tuple(nearby_chunk)
                if self.world[nearby_chunk][x, y, z, 0] != 0:
                    block_name = BLOCK_DICT[self.world[nearby_chunk][x, y, z, 0]]
                    self.world[nearby_chunk][x, y, z, side] = 1
                    new_transform = numpy.array([pyrr.matrix44.create_from_translation(
                                [x + nearby_chunk[0] * 16, y, z + nearby_chunk[1] * 16])], dtype=numpy.float32)
                    if block_name in self.transform and len(self.transform[block_name][side]) > 0:
                        self.transform[block_name][side] = numpy.append(
                            self.transform[block_name][side], new_transform, 0
                        )
                    else:
                        self.transform[block_name][side] = new_transform.copy()
                    if block_name not in self.rendered_chunks[nearby_chunk]:
                        empty_array = numpy.array([], dtype=numpy.float32)
                        self.rendered_chunks[nearby_chunk][block_name] = {side: empty_array for side in range(1, 7)}
                    if len(self.rendered_chunks[nearby_chunk][block_name][side]) > 0:
                        self.rendered_chunks[nearby_chunk][block_name][side] = \
                            numpy.append(self.rendered_chunks[nearby_chunk][block_name][side], new_transform, 0)
                    else:
                        self.rendered_chunks[nearby_chunk][block_name][side] = new_transform.copy()
                    self.vaos_3d[block_name].sides[side].transform_update(self.transform[block_name][side].copy())

    def entities_add(self):  # todo implement this and entities_remove. k thnx.
        pass

    def entities_remove(self):
        pass

    def check_hardness(self, block):
        current_tool = BLOCK_INFO[self.player.hotbar[self.active_bar - 1, 0]] \
            if self.player.hotbar[self.active_bar - 1, 0] in BLOCK_INFO else "hand"
        best_tool = BLOCK_INFO[block]["tool"] == current_tool
        harvestable = BLOCK_INFO[block]["harvestable"] is True or (BLOCK_INFO[block]["harvestable"] == "tool" and best_tool)
        if harvestable:
            seconds = BLOCK_INFO[block]["hardness"] * 1.5
        else:
            seconds = BLOCK_INFO[block]["hardness"] * 5
        if best_tool:
            speedMultiplier = 2 if "wood" in current_tool else \
                4 if "stone" in current_tool else \
                6 if "iron" in current_tool else \
                8 if "diamond" in current_tool else \
                9 if "netherite" in current_tool else \
                12 if "gold" in current_tool else 1
            # if toolEfficiency:
            #     speedMultiplier += efficiencyLevel ^ 2 + 1
        else:
            speedMultiplier = 1
        if not harvestable:
            speedMultiplier = 1
        # if hasteEffect:
        #     speedMultiplier *= 1 + (0.2 * hasteLevel)
        # if miningFatigue:
        #     speedMultiplier /= 3 ^ miningFatigueLevel
        seconds /= speedMultiplier
        # if inWater:
        #     seconds *= 5
        if self.player.jumping or self.player.flying:
            seconds *= 5
        return seconds

    def drop_item(self):
        if self.selected_block not in [None, "_tp"]:
            item_name = f"{self.selected_block}_item"
            pos = list(self.player.pos)
            pos[1] += 1.62
            pos_matrix = numpy.dot(pyrr.matrix44.create_from_scale((0.25, 0.25, 0.25)),
                                   pyrr.matrix44.create_from_translation(pos))
            for vao in self.vaos_3d[item_name].sides:
                if self.vaos_3d[item_name].sides[vao].transform is not None:
                    self.vaos_3d[item_name].sides[vao].transform = numpy.append(
                        self.vaos_3d[item_name].sides[vao].transform, numpy.array([pos_matrix], dtype=numpy.float32), 0
                    )
                else:
                    self.vaos_3d[item_name].sides[vao].transform = numpy.array([pos_matrix], dtype=numpy.float32)
                if vao == 4:
                    rx = self.player.front[0] * 2
                    ry = self.player.front[1] * 8.95142
                    rz = self.player.front[2] * 2
                    if self.vaos_3d[item_name].top.item_data is not None:
                        self.vaos_3d[item_name].top.item_data = numpy.append(
                            self.vaos_3d[item_name].top.item_data,
                            numpy.array([[rx, ry, rz, 1, 0, 0, 0, 1]], dtype=numpy.float32), 0
                        )
                    else:
                        self.vaos_3d[item_name].top.item_data = \
                            numpy.array([[rx, ry, rz, 1, 0, 0, 0, 1]], dtype=numpy.float32)
                self.vaos_3d[item_name].sides[vao].transform_update()
            self.inventory_remove(["hotbar", self.active_bar], self.selected_block)
            if not self.player.hotbar[self.active_bar - 1, 0]:
                self.selected_block = None

    def block_face(self):
        x, y, z = self.player.pos + self.ray_wor * (self.ray_i - 0.01)
        y += 1.62
        x, y, z = int(self.check_value(x, 0)), int(self.check_value(y, 0)), int(self.check_value(z, 0))
        hx, hy, hz = self.highlighted[3, :3]
        if (x, y, z) in ((hx + 1, hy, hz), (hx, hy + 1, hz), (hx, hy, hz + 1),
                         (hx - 1, hy, hz), (hx, hy - 1, hz), (hx, hy, hz - 1)):
            return x, y, z
        else:
            return hx, hy, hz

    # region Callback Methods
    def mouse_callback(self, window, dx, dy):
        if not self.mouse_visibility:
            x_offset = dx - self.width / 2
            y_offset = self.height / 2 - dy
            self.player.process_mouse_movement(x_offset, y_offset)
            glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
        elif self.mouse_visibility:
            self.buttons.highlight(dx, dy)
            if self.in_inventory:
                self.vaos_2d["mouse_inventory"].transform_update(numpy.array(
                    [pyrr.matrix44.create_from_translation([dx * (1280 / self.width) - 16, dy * (720 / self.height) - 16, -0.1])], dtype=numpy.float32
                ))
                for vao in self.vaos_2d:
                    if "slot" in vao and "inventory" in vao and "active" not in vao:
                        instance = tuple(self.vaos_2d[vao].transform[0, 3])
                        if (int(instance[0]) / 1280) * self.width < dx < ((int(instance[0]) + 32) / 1280) * \
                                self.width and (int(instance[1]) / 720) * self.height < dy < \
                                ((int(instance[1]) + 32) / 720) * self.height:
                            self.vaos_2d["active_inventory_slot"].transform_update(numpy.array(
                                [pyrr.matrix44.create_from_translation([int(instance[0]), int(instance[1]), -0.2])],
                                dtype=numpy.float32
                            ))
                            break
                        else:
                            self.vaos_2d["active_inventory_slot"].transform_update(numpy.array([], dtype=numpy.float32))

    def scroll_callback(self, window, dx, dy):
        if dy > 0:
            if not self.paused:
                new_hotbar = int((self.vaos_2d["active_bar"].transform[0][3][0] - 416.0) / 40.0 - 1.0)
                if new_hotbar < 1:
                    new_hotbar = 9
                self.active_bar = new_hotbar
                self.selected_block = self.vaos_2d[f"hotbar_{new_hotbar}"].texture_name
                self.vaos_2d["active_bar"].transform = numpy.array(
                    [pyrr.matrix44.create_from_translation([new_hotbar * 40.0 + 416.0, 674.0, -0.5])], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].transform_update()
        elif dy < 0:
            if not self.paused:
                new_hotbar = int((self.vaos_2d["active_bar"].transform[0][3][0] - 416.0) / 40.0 + 1.0)
                if new_hotbar > 9:
                    new_hotbar = 1
                self.active_bar = new_hotbar
                self.selected_block = self.vaos_2d[f"hotbar_{new_hotbar}"].texture_name
                self.vaos_2d["active_bar"].transform = numpy.array(
                    [pyrr.matrix44.create_from_translation([new_hotbar * 40.0 + 416.0, 674.0, -0.5])], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].transform_update()

    def mouse_button_callback(self, window, button, action, mods):
        mouse_pos = glfw.get_cursor_pos(window)
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.mouse_visibility:
                self.buttons.activate(*mouse_pos)
                if self.in_inventory:
                    if not ((464 / 1280) * self.width < mouse_pos[0] < ((464 + 352) / 1280) * self.width and (146 / 720)
                            * self.height < mouse_pos[1] < ((146 + 332) / 720) * self.height):
                        glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                        self.mouse_visibility = False
                        self.paused = False
                        self.in_inventory = False
                    elif len(self.vaos_2d["active_inventory_slot"].transform) > 0:
                        instance = tuple(self.vaos_2d["active_inventory_slot"].transform[0, 3])
                        if f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}" in \
                                self.vaos_2d:
                            area = "inventory"
                            mouse_vao = \
                                f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}"
                            mouse_value = self.player.inventory[int(mouse_vao.split("_")[-1]) - 1]
                        elif f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}" in self.vaos_2d:
                            area = "hotbar"
                            mouse_vao = f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}"
                            mouse_value = self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1]
                        else:
                            area = None
                            mouse_vao = None
                            mouse_value = [0, 0]
                        mouse_value = mouse_value.copy()
                        if mouse_vao is not None:
                            self.vaos_2d["mouse_inventory"].transform_update(numpy.array(
                                [pyrr.matrix44.create_from_translation([int(instance[0]), int(instance[1]), -0.3])], dtype=numpy.float32
                            ))
                            if self.vaos_2d["mouse_inventory"].texture_name == \
                                    self.vaos_2d[mouse_vao].texture_name and \
                                    self.vaos_2d["mouse_inventory"].texture_name != "_tp":
                                if area == "hotbar":
                                    self.text.remove_text(
                                        str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                        [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                    )
                                    self.text.remove_text(
                                        str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                        [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                    )
                                    self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1][1] += self.mouse_value[1]
                                    if self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1] > 64:
                                        mouse_value[1] = self.player.hotbar[int(mouse_vao[-1]) - 1, 1] % 64
                                        self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1] = 64
                                    else:
                                        mouse_value = [0, 0]
                                        self.vaos_2d["mouse_inventory"].texture_name = "_tp"
                                        self.vaos_2d["mouse_inventory"].texture = Entity.load_texture("textures/_tp.png")
                                    self.text.add_text(
                                        str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                        [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                    )
                                    self.text.add_text(
                                        str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                        [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                    )
                                elif area == "inventory":
                                    self.text.remove_text(
                                        str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                         314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                    )
                                    self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1] += self.mouse_value[1]
                                    if self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1] > 64:
                                        mouse_value[1] = \
                                            self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1] % 64
                                        self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1] = 64
                                    else:
                                        mouse_value = [0, 0]
                                        self.vaos_2d["mouse_inventory"].texture_name = "_tp"
                                        self.vaos_2d["mouse_inventory"].texture = Entity.load_texture("textures/_tp.png")
                                    self.text.add_text(
                                        str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                         314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                    )
                            else:
                                self.vaos_2d["mouse_inventory"].texture_name, \
                                    self.vaos_2d[mouse_vao].texture_name = self.vaos_2d[mouse_vao].texture_name, \
                                    self.vaos_2d["mouse_inventory"].texture_name
                                self.vaos_2d["mouse_inventory"].texture, self.vaos_2d[mouse_vao].texture = \
                                    self.vaos_2d[mouse_vao].texture, self.vaos_2d["mouse_inventory"].texture
                                if area == "hotbar":
                                    if self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 0] != 0:
                                        self.text.remove_text(
                                            str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                            [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                        )
                                        self.text.remove_text(
                                            str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                            [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                        )
                                    self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1] = self.mouse_value
                                    if self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 0] != 0:
                                        self.text.add_text(
                                            str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                            [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                        )
                                        self.text.add_text(
                                            str(int(self.player.hotbar[int(mouse_vao[-1]) - 1, 1])),
                                            [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                        )
                                elif area == "inventory":
                                    if self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 0] != 0:
                                        self.text.remove_text(
                                            str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                            [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                             314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                        )
                                    self.player.inventory[int(mouse_vao.split("_")[-1]) - 1] = self.mouse_value
                                    if self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 0] != 0:
                                        self.text.add_text(
                                            str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                            [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                             314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                        )
                            self.mouse_value = mouse_value.copy()
                            if "hotbar" in mouse_vao:
                                self.vaos_2d[f"hotbar_{mouse_vao[-1]}"].texture_name = \
                                    self.vaos_2d[mouse_vao].texture_name
                                self.vaos_2d[f"hotbar_{mouse_vao[-1]}"].texture = \
                                    self.vaos_2d[mouse_vao].texture
                                if int(mouse_vao[-1]) == self.active_bar:
                                    self.selected_block = self.vaos_2d[mouse_vao].texture_name
                    self.vaos_2d["mouse_inventory"].transform_update(numpy.array(
                        [pyrr.matrix44.create_from_translation(
                            [mouse_pos[0] * (1280 / self.width) - 16,
                             mouse_pos[1] * (720 / self.height) - 16, -0.1])], dtype=numpy.float32
                    ))
        elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
            if self.mouse_visibility:
                if self.in_inventory:
                    if len(self.vaos_2d["active_inventory_slot"].transform) > 0:
                        instance = tuple(self.vaos_2d["active_inventory_slot"].transform[0, 3])
                        if f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}" in \
                                self.vaos_2d:
                            area = "inventory"
                            mouse_vao = \
                                f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}"
                            mouse_value = self.player.inventory[int(mouse_vao.split("_")[-1]) - 1]
                        elif f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}" in self.vaos_2d:
                            area = "hotbar"
                            mouse_vao = f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}"
                            mouse_value = self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1]
                        else:
                            area = None
                            mouse_vao = None
                            mouse_value = [0, 0]
                        mouse_value = mouse_value.copy()
                        if mouse_vao is not None:
                            self.vaos_2d["mouse_inventory"].transform_update(numpy.array(
                                [pyrr.matrix44.create_from_translation([
                                    mouse_pos[0] * (1280 / self.width) - 16,
                                    mouse_pos[1] * (720 / self.height) - 16, -0.1])], dtype=numpy.float32
                            ))
                            if self.vaos_2d["mouse_inventory"].texture_name in ["_tp", None] and \
                                    getattr(self.player, area)[int(mouse_vao.split("_")[-1]) - 1, 0] and \
                                    getattr(self.player, area)[int(mouse_vao.split("_")[-1]) - 1, 1] > 1:
                                self.vaos_2d["mouse_inventory"].texture_name = self.vaos_2d[mouse_vao].texture_name
                                self.vaos_2d["mouse_inventory"].texture = self.vaos_2d[mouse_vao].texture
                                if area == "hotbar":
                                    self.text.remove_text(
                                        str(int(self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                    )
                                    self.text.remove_text(
                                        str(int(self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                    )
                                    mouse_value[1] = self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1][1] // 2
                                    self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1][1] -= mouse_value[1]
                                    self.text.add_text(
                                        str(int(self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [424.0 + int(mouse_vao.split("_")[-1]) * 40, 682.0, -0.5], 2
                                    )
                                    self.text.add_text(
                                        str(int(self.player.hotbar[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [444.0 + int(mouse_vao.split("_")[-1]) * 36, 430.0, -0.1], 2, True
                                    )
                                elif area == "inventory":
                                    self.text.remove_text(
                                        str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                         314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                    )
                                    mouse_value[1] = self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1] // 2
                                    self.player.inventory[int(mouse_vao.split("_")[-1]) - 1][1] -= mouse_value[1]
                                    self.text.add_text(
                                        str(int(self.player.inventory[int(mouse_vao.split("_")[-1]) - 1, 1])),
                                        [480.0 + ((int(mouse_vao.split("_")[-1]) - 1) % 9) * 36,
                                         314.0 + int((int(mouse_vao.split("_")[-1]) - 1) / 9) * 36, -0.1], 2, True
                                    )
                                self.mouse_value = mouse_value
                                self.mouse_value = self.mouse_value.copy()

    def key_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            if self.in_game:
                self.paused = not self.paused
                self.mouse_visibility = not self.mouse_visibility
                if self.mouse_visibility:
                    glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                else:
                    glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        elif key == glfw.KEY_E and action == glfw.PRESS:
            if self.in_game:
                self.in_inventory = not self.in_inventory
                self.paused = not self.paused
                self.mouse_visibility = not self.mouse_visibility
                if self.mouse_visibility is True:
                    glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                elif self.mouse_visibility is False:
                    glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
        elif key == glfw.KEY_P and action == glfw.PRESS:
            if self.in_game:
                self.player.pos = pyrr.Vector3([0.3, self.y_values[512, 512] + 1, 0.3])
        elif key == glfw.KEY_Q and action == glfw.PRESS:
            if self.in_game:
                self.drop_item()
        if 0 <= key < 1024:
            if action == glfw.PRESS:
                self.keys[key] = True
            elif action == glfw.RELEASE:
                self.keys[key] = False
        for i in range(1, 10):
            if key == getattr(glfw, f"KEY_{i}"):
                self.selected_block = self.vaos_2d[f"hotbar_{i}"].texture_name
                self.vaos_2d["active_bar"].transform = numpy.array(
                    [pyrr.matrix44.create_from_translation([416.0 + 40.0 * i, 674.0, -0.5])], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].transform_update()
                self.active_bar = i
        if self.new_game:
            self.player.pos = pyrr.Vector3([0.3, self.y_values[512, 512] + 1, 0.3])
            self.text.clear()
            self.text.add_text(f"{self.fps}", [1240.0, 20.0, -0.4], 2)
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            self.mouse_visibility = False
            self.in_game = True
            self.new_game = False

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, width / height, 0.1, 100.0)
        # todo make the 2d projection actually scale
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, width, height, 0, 0.01, 100.0)
        self.width, self.height = width, height
    # endregion

    @staticmethod
    def get_load_data():
        world_data = dict()
        for world in os.listdir(".\\worlds"):
            world_data[world.split(".")[0]] = open(world, "r").read()
        return world_data if len(world_data) > 0 else False

    @staticmethod
    def check_value(value, limit):
        if value < limit:
            value -= 1
        return value


class Camera:
    def __init__(self):
        self.pos = pyrr.Vector3([0.0, 0.0, 0.0])
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.125
        self.yaw = -90.0
        self.pitch = 0.0

    def get_view_matrix(self):
        return self.look_at(self.pos, self.pos + self.front, self.up)

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.yaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 90.0:
                self.pitch = 90.0
            if self.pitch < -90.0:
                self.pitch = -90.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = pyrr.Vector3([0.0, 0.0, 0.0])
        front.x = numpy.cos(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch))
        front.y = numpy.sin(numpy.radians(self.pitch))
        front.z = numpy.sin(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch))

        self.front = pyrr.vector.normalise(front)
        self.right = pyrr.vector.normalise(pyrr.vector3.cross(self.front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.up = pyrr.vector.normalise(pyrr.vector3.cross(self.right, self.front))

    @staticmethod
    def look_at(position, target, world_up):
        z_axis = pyrr.vector.normalise(position - target)
        x_axis = pyrr.vector.normalise(pyrr.vector3.cross(pyrr.vector.normalise(world_up), z_axis))
        y_axis = pyrr.vector3.cross(z_axis, x_axis)

        translation = pyrr.Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = pyrr.Matrix44.identity()
        rotation[0][0] = x_axis[0]
        rotation[1][0] = x_axis[1]
        rotation[2][0] = x_axis[2]
        rotation[0][1] = y_axis[0]
        rotation[1][1] = y_axis[1]
        rotation[2][1] = y_axis[2]
        rotation[0][2] = z_axis[0]
        rotation[1][2] = z_axis[1]
        rotation[2][2] = z_axis[2]

        return rotation * translation


class Player(Camera):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.gamemode = "Survival"
        self.difficulty = 2
        self.jumping = False
        self.crouching = False
        self.holding_walk = False
        self.holding_jump = False
        self.sprinting = False
        self.flying = False
        self.placing = False
        self.breaking = False
        self.sprint_delay = 0
        self.place_delay = 0
        self.break_delay = 0
        self.fly_delay = 0
        self.air_vel = 0
        self.inventory = numpy.zeros((27, 2))
        self.hotbar = numpy.zeros((9, 2))

    def process_keyboard(self, direction, velocity):
        if direction == "FRONT":
            self.pos.x += numpy.cos(numpy.radians(self.yaw)) * velocity
            if not self.app.check_pos(self.pos, True) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1, self.pos[2])) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1.8, self.pos[2])):
                self.pos.x -= numpy.cos(numpy.radians(self.yaw)) * velocity
            self.pos.z += numpy.sin(numpy.radians(self.yaw)) * velocity
            if not self.app.check_pos(self.pos, True) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1, self.pos[2])) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1.8, self.pos[2])):
                self.pos.z -= numpy.sin(numpy.radians(self.yaw)) * velocity
        elif direction == "SIDE":
            self.pos.x += numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            if not self.app.check_pos(self.pos, True) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1, self.pos[2])) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1.8, self.pos[2])):
                self.pos.x -= numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            self.pos.z += numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            if not self.app.check_pos(self.pos, True) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1, self.pos[2])) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1.8, self.pos[2])):
                self.pos.z -= numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
        elif direction == "UP":
            self.pos.y += velocity
            if not self.app.check_pos(self.pos, True) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1, self.pos[2])) \
                    or not self.app.check_pos((self.pos[0], self.pos[1] + 1.8, self.pos[2])):
                self.pos.y -= velocity


class Entity:
    def __init__(self, vertex, index, texture, transform=None, transpose=False):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertex_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 5, ctypes.c_void_p(0))

        self.index_ebo = glGenBuffers(1)
        self.index = index
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertex.itemsize * 5, ctypes.c_void_p(12))
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.transform_vbo = glGenBuffers(1)
        self.transform = transform
        glBindBuffer(GL_ARRAY_BUFFER, self.transform_vbo)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glVertexAttribDivisor(3, 1)
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glVertexAttribDivisor(4, 1)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        if self.transform is not None:
            self.transform_update(self.transform)

        if isinstance(texture, str):
            self.texture_name = texture.split("/")[-1].split(".")[0]
        self.texture = self.load_texture(texture, transpose)

        glBindVertexArray(0)

        self.item_data = None

    def transform_update(self, transform=None):
        if transform is not None:
            self.transform = transform
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.transform_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.transform.nbytes, self.transform.flatten(), GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @staticmethod
    def load_texture(texture_file, transpose=False):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        if isinstance(texture_file, str):
            image = Image.open(texture_file)
            if transpose:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            width, height = image.width, image.height
            img_data = numpy.array(list(image.getdata()), numpy.uint8)
        else:
            cx, cy = texture_file[1]
            image = texture_file[0]
            orig_data = numpy.array(list(image.getdata()), numpy.uint8).reshape((image.height, image.width * 4))
            img_data = numpy.empty((8, texture_file[2][0] * 4), dtype=numpy.uint8)
            for x in range(cx * 4, (cx + texture_file[2][0]) * 4):
                for y in range(cy, cy + 8):
                    img_data[y - cy, x - (cx * 4)] = orig_data[y, x]
            width, height = texture_file[2][0], 8
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture


class Block:
    front_v = numpy.array([
        0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 0.0, 1.0, 1.0, 0.0,
        1.0, 1.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 0.0, 1.0
    ], dtype=numpy.float32)
    back_v = numpy.array([
        1.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
        0.0, 1.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 0.0, 0.0, 1.0
    ], dtype=numpy.float32)
    right_v = numpy.array([
        1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 1.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 0.0, 1.0,
        1.0, 0.0, 1.0, 0.0, 0.0
    ], dtype=numpy.float32)
    left_v = numpy.array([
        0.0, 1.0, 0.0, 0.0, 1.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 1.0, 0.0,
        0.0, 1.0, 1.0, 1.0, 1.0,
    ], dtype=numpy.float32)
    bottom_v = numpy.array([
        0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 0.0, 1.0,
    ], dtype=numpy.float32)
    top_v = numpy.array([
        1.0, 1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 1.0, 0.0,
        0.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 0.0, 1.0
    ], dtype=numpy.float32)

    item_front_v = numpy.array([
        -0.5, 0.0, 0.5, 0.0, 0.0,
        0.5, 0.0, 0.5, 1.0, 0.0,
        0.5, 1.0, 0.5, 1.0, 1.0,
        -0.5, 1.0, 0.5, 0.0, 1.0
    ], dtype=numpy.float32)
    item_back_v = numpy.array([
        0.5, 0.0, -0.5, 0.0, 0.0,
        -0.5, 0.0, -0.5, 1.0, 0.0,
        -0.5, 1.0, -0.5, 1.0, 1.0,
        0.5, 1.0, -0.5, 0.0, 1.0
    ], dtype=numpy.float32)
    item_right_v = numpy.array([
        0.5, 0.0, 0.5, 0.0, 0.0,
        0.5, 0.0, -0.5, 1.0, 0.0,
        0.5, 1.0, -0.5, 1.0, 1.0,
        0.5, 1.0, 0.5, 0.0, 1.0
    ], dtype=numpy.float32)
    item_left_v = numpy.array([
        -0.5, 0.0, -0.5, 0.0, 0.0,
        -0.5, 0.0, 0.5, 1.0, 0.0,
        -0.5, 1.0, 0.5, 1.0, 1.0,
        -0.5, 1.0, -0.5, 0.0, 1.0
    ], dtype=numpy.float32)
    item_bottom_v = numpy.array([
        -0.5, 0.0, -0.5, 0.0, 0.0,
        0.5, 0.0, -0.5, 1.0, 0.0,
        0.5, 0.0, 0.5, 1.0, 1.0,
        -0.5, 0.0, 0.5, 0.0, 1.0,
    ], dtype=numpy.float32)
    item_top_v = numpy.array([
        0.5, 1.0, -0.5, 0.0, 0.0,
        -0.5, 1.0, -0.5, 1.0, 0.0,
        -0.5, 1.0, 0.5, 1.0, 1.0,
        0.5, 1.0, 0.5, 0.0, 1.0
    ], dtype=numpy.float32)

    def __init__(self, textures, item=False):
        self.item = item
        self.front = Entity(Block.front_v if not self.item else Block.item_front_v, INDICES, textures[0], transpose=True)
        self.back = Entity(Block.back_v if not self.item else Block.item_back_v, INDICES, textures[1], transpose=True)
        self.right = Entity(Block.right_v if not self.item else Block.item_right_v, INDICES, textures[2], transpose=True)
        self.left = Entity(Block.left_v if not self.item else Block.item_left_v, INDICES, textures[3], transpose=True)
        self.bottom = Entity(Block.bottom_v if not self.item else Block.item_bottom_v, INDICES, textures[4], transpose=True)
        self.top = Entity(Block.top_v if not self.item else Block.item_top_v, INDICES, textures[5], transpose=True)
        self.sides = {6: self.front, 5: self.back, 2: self.right, 1: self.left, 4: self.top, 3: self.bottom}


class Text:
    def __init__(self):
        self.vaos = dict()
        character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 1.0, 5.0, 8.0, 0.0, 1.0, 1.0,
                                 5.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
        self.vaos[" "] = Entity(character, INDICES, (ASCII_PNG, (0, 16), (8, 8)))
        self.vaos[" _inventory"] = Entity(character, INDICES, (ASCII_PNG, (0, 16), (8, 8)))
        for char in CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0], 8.0, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0], 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
            self.vaos[f"{char}"] = Entity(character, INDICES, (ASCII_PNG, *CHARACTER_DICT[char][0]))
            self.vaos[f"{char}_inventory"] = Entity(character, INDICES, (ASCII_PNG, *CHARACTER_DICT[char][0]))
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0], 8.0, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0], 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
            self.vaos[f"{char.upper()}"] = Entity(character, INDICES, (ASCII_PNG, *CHARACTER_DICT[char][1]))
            self.vaos[f"{char.upper()}_inventory"] = Entity(character, INDICES, (ASCII_PNG, *CHARACTER_DICT[char][1]))
        for char in SPECIAL_CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0], 8.0, 0.0, 1.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0], 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
            self.vaos[f"{char}"] = Entity(character, INDICES, (ASCII_PNG, *SPECIAL_CHARACTER_DICT[char]))
            self.vaos[f"{char}_inventory"] = Entity(character, INDICES, (ASCII_PNG, *SPECIAL_CHARACTER_DICT[char]))

    def add_text(self, text, pos, size, in_inventory=False, justify="left"):
        pos_list = list()
        for character in text:
            pos_list.append(pos.copy())
            if character in CHARACTER_DICT:
                pos[0] += size * (CHARACTER_DICT[character][0][1][0] + 1)
            elif character.lower() in CHARACTER_DICT:
                pos[0] += size * (CHARACTER_DICT[character.lower()][1][1][0] + 1)
            elif character in SPECIAL_CHARACTER_DICT:
                pos[0] += size * (SPECIAL_CHARACTER_DICT[character][1][0] + 1)
            else:
                pos[0] += size * 5
        for i, character in enumerate(text):
            if character is not None:
                if justify == "center":
                    pos_list[i] = [
                        pos_list[i][0] - len(text) * round(size * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in text]) / len(text)) / 2), pos_list[i][1] + BUTTON_OUTLINE[11] / 2 - size * 4, pos_list[i][2]
                    ]
                if in_inventory:
                    if self.vaos[f"{character}_inventory"].transform is not None:
                        self.vaos[f"{character}_inventory"].transform = numpy.append(
                            self.vaos[f"{character}_inventory"].transform, numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([size] * 3), pyrr.matrix44.create_from_translation(pos_list[i]))], dtype=numpy.float32), 0
                        )
                    else:
                        self.vaos[f"{character}_inventory"].transform = numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([size] * 3), pyrr.matrix44.create_from_translation(pos_list[i]))], dtype=numpy.float32)
                    self.vaos[f"{character}_inventory"].transform_update()
                else:
                    if self.vaos[f"{character}"].transform is not None:
                        self.vaos[f"{character}"].transform = numpy.append(
                            self.vaos[f"{character}"].transform, numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([size] * 3), pyrr.matrix44.create_from_translation(pos_list[i]))], dtype=numpy.float32), 0
                        )
                    else:
                        self.vaos[f"{character}"].transform = numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([size] * 3), pyrr.matrix44.create_from_translation(pos_list[i]))], dtype=numpy.float32)
                    self.vaos[f"{character}"].transform_update()

    def remove_text(self, text, pos, size, in_inventory=False, justify="left"):
        pos_list = list()
        for character in text:
            pos_list.append(pos.copy())
            if character in CHARACTER_DICT:
                pos[0] += size * (CHARACTER_DICT[character][0][1][0] + 1)
            elif character.lower() in CHARACTER_DICT:
                pos[0] += size * (CHARACTER_DICT[character.lower()][1][1][0] + 1)
            elif character in SPECIAL_CHARACTER_DICT:
                pos[0] += size * (SPECIAL_CHARACTER_DICT[character][1][0] + 1)
            else:
                pos[0] += size * 5
        for i, character in enumerate(text):
            if character is not None:
                if justify == "center":
                    pos_list[i] = [
                        pos_list[i][0] - len(text) * round(size * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in text]) / len(text)) / 2), pos_list[i][1] + BUTTON_OUTLINE[11] / 2 - size * 4, pos_list[i][2]
                    ]
                if in_inventory:
                    self.vaos[f"{character}_inventory"].transform = numpy.delete(
                        self.vaos[f"{character}_inventory"].transform,
                        numpy.nonzero((self.vaos[f"{character}_inventory"].transform[:, 3, 0] == pos_list[i][0]) &
                                    (self.vaos[f"{character}_inventory"].transform[:, 3, 1] == pos_list[i][1]) &
                                    (self.vaos[f"{character}_inventory"].transform[:, 3, 2] == pos_list[i][2])),
                        0
                    )
                    self.vaos[f"{character}_inventory"].transform_update()
                else:
                    self.vaos[f"{character}"].transform = numpy.delete(
                        self.vaos[f"{character}"].transform,
                        numpy.nonzero((self.vaos[f"{character}"].transform[:, 3, 0] == pos_list[i][0]) &
                                    (self.vaos[f"{character}"].transform[:, 3, 1] == pos_list[i][1]) &
                                    (self.vaos[f"{character}"].transform[:, 3, 2] == pos_list[i][2])),
                        0
                    )
                    self.vaos[f"{character}"].transform_update()

    def clear(self):
        for vao in self.vaos.values():
            vao.transform = None


class Button:
    def __init__(self, app):
        self.app = app
        self.pos_list = list()
        self.app.vaos_2d["normal_button_outline"] = \
            Entity(BUTTON_OUTLINE, INDICES, "textures/_normal_button_outline.png")
        self.app.vaos_2d["highlighted_button_outline"] = \
            Entity(BUTTON_OUTLINE, INDICES, "textures/_highlighted_button_outline.png")
        self.app.vaos_2d["disabled_button_foreground"] = \
            Entity(BUTTON_OUTLINE, INDICES, "textures/_black_tp.png")

        # self.texture = Entity.load_texture(self.texture)
        # self.highlight_texture = Entity.load_texture(self.highlight_texture)

    def add_instance(self, text, pos, size, active_lambda, state=True):
        self.pos_list.append([pos, False, text, size, active_lambda, state])
        self.app.text.add_text(text, [
            pos[0] + BUTTON_OUTLINE[10] / 2 - len(text) * round(size * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in text]) / len(text)) / 2), pos[1] + BUTTON_OUTLINE[11] / 2 - size * 4, -0.3
        ], size)
        if self.app.vaos_2d["normal_button_outline"].transform is not None and \
                len(self.app.vaos_2d["normal_button_outline"].transform) > 0:
            self.app.vaos_2d["normal_button_outline"].transform_update(
                numpy.append(
                    self.app.vaos_2d["normal_button_outline"].transform,
                    numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32), 0
                )
            )
        else:
            self.app.vaos_2d["normal_button_outline"].transform_update(
                numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32)
            )
        if not state:
            if self.app.vaos_2d["disabled_button_foreground"].transform is not None and \
                    len(self.app.vaos_2d["disabled_button_foreground"].transform) > 0:
                self.app.vaos_2d["disabled_button_foreground"].transform_update(
                    numpy.append(
                        self.app.vaos_2d["disabled_button_foreground"].transform,
                        numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.2])], dtype=numpy.float32), 0
                    )
                )
            else:
                self.app.vaos_2d["disabled_button_foreground"].transform_update(
                    numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.2])], dtype=numpy.float32)
                )

    def activate(self, dx, dy):
        for pos, outline, text, size, active_lambda, state in self.pos_list:
            if pos[0] / 1280 * self.app.width < dx < (pos[0] + BUTTON_OUTLINE[10]) / 1280 * self.app.width and \
                    pos[1] / 720 * self.app.height < dy < (pos[1] + BUTTON_OUTLINE[11]) / 720 * self.app.height and state:
                active_lambda()
                return True
        return False

    def highlight(self, dx, dy):
        for index, data in enumerate(self.pos_list):
            pos, highlighted, text, size, active_lambda, state = data
            if pos[0] / 1280 * self.app.width < dx < (pos[0] + BUTTON_OUTLINE[10]) / 1280 * self.app.width and \
                    pos[1] / 720 * self.app.height < dy < (pos[1] + BUTTON_OUTLINE[11]) / 720 * self.app.height and state:
                if not highlighted:
                    self.app.vaos_2d["normal_button_outline"].transform_update(
                        numpy.delete(
                            self.app.vaos_2d["normal_button_outline"].transform,
                            numpy.nonzero((self.app.vaos_2d["normal_button_outline"].transform[:, 3, 0] == pos[0]) &
                                        (self.app.vaos_2d["normal_button_outline"].transform[:, 3, 1] == pos[1])),
                            0
                        )
                    )
                    if self.app.vaos_2d["highlighted_button_outline"].transform is not None and \
                            len(self.app.vaos_2d["highlighted_button_outline"].transform) > 0:
                        self.app.vaos_2d["highlighted_button_outline"].transform_update(
                            numpy.append(
                                self.app.vaos_2d["highlighted_button_outline"].transform,
                                numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32),
                                0
                            )
                        )
                    else:
                        self.app.vaos_2d["highlighted_button_outline"].transform_update(
                            numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32)
                        )
                    self.pos_list[index][1] = True
            elif highlighted:
                self.app.vaos_2d["highlighted_button_outline"].transform_update(
                    numpy.delete(
                        self.app.vaos_2d["highlighted_button_outline"].transform,
                        numpy.nonzero((self.app.vaos_2d["highlighted_button_outline"].transform[:, 3, 0] == pos[0]) &
                                      (self.app.vaos_2d["highlighted_button_outline"].transform[:, 3, 1] == pos[1])),
                        0
                    )
                )
                if self.app.vaos_2d["normal_button_outline"].transform is not None:
                    self.app.vaos_2d["normal_button_outline"].transform_update(
                        numpy.append(
                            self.app.vaos_2d["normal_button_outline"].transform,
                            numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32), 0
                        )
                    )
                else:
                    self.app.vaos_2d["normal_button_outline"].transform_update(
                        numpy.array([pyrr.matrix44.create_from_translation([*pos, -0.4])], dtype=numpy.float32)
                    )
                self.pos_list[index][1] = False

    def clear(self):
        for index, data in enumerate(self.pos_list):
            pos, highlighted, text, size, active_lambda, state = data
            self.app.text.remove_text(text, [
                pos[0] + BUTTON_OUTLINE[10] / 2 - len(text) * round(size * (sum([CHARACTER_DICT[letter][0][1][0] + 1 if letter in CHARACTER_DICT else CHARACTER_DICT[letter.lower()][1][1][0] + 1 if letter.lower() in CHARACTER_DICT else SPECIAL_CHARACTER_DICT[letter][1][0] + 1 if letter in SPECIAL_CHARACTER_DICT else 5 for letter in text]) / len(text)) / 2), pos[1] + BUTTON_OUTLINE[11] / 2 - size * 4, -0.3
            ], size)
        self.pos_list.clear()
        self.app.vaos_2d["normal_button_outline"].transform_update(numpy.array([], dtype=numpy.float32))
        self.app.vaos_2d["highlighted_button_outline"].transform_update(numpy.array([], dtype=numpy.float32))
        self.app.vaos_2d["disabled_button_foreground"].transform_update(numpy.array([], dtype=numpy.float32))


if __name__ == '__main__':
    App(1280, 720, "False Worlds")
