import numpy
import colorsys
import pygame
from typing import TYPE_CHECKING, List
from perlin_noise import PerlinNoise
from environment.tile_lookup import TileLookup
from environment.tile import Tile

if TYPE_CHECKING:
    from environment.chunk import Chunk


class Generation:
    def get_noise(octaves: float, seed: int):
        return PerlinNoise(octaves=octaves, seed=seed)

    def get_normal(noise: PerlinNoise, height: int, width: int, strength: float = 1.0):
        normal_map = numpy.zeros((height, width, 3))

        for y in range(0, height):
            for x in range(0, width):
                x2, x1 = x + 1, x - 1
                if x == 0:
                    x1 = x
                elif x == width:
                    x2 = x

                y2, y1 = y + 1, y - 1
                if y == 0:
                    y1 = y
                elif y == height:
                    y2 = y

                dzdx = (
                    noise([x2 / width, y / height])
                    - noise([x1 / width, y / height])
                ) * strength

                dzdy = dzdy = (
                    noise([x / width, y2 / height])
                    - noise([x / width, y1 / height])
                ) * strength

                v1 = numpy.array([1, 0, dzdx])
                v2 = numpy.array([0, 1, dzdy])

                cross_product = numpy.cross(v1, v2)

                normal_map[y][x] = cross_product / numpy.linalg.norm(cross_product)

        return normal_map

    def brighten_color(color: pygame.Color, brightness_factor):
        r, g, b = color.r / 255, color.g / 255, color.b / 255
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        v = max(0, min(1, v * brightness_factor))
        # s = max(0, min(1, s / brightness_factor))

        new_r, new_g, new_b = (int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))
        return pygame.Color(new_r, new_g, new_b)

    def generate_random_chunk(
        self: "Chunk", noise: PerlinNoise, normal: numpy.ndarray, sun: numpy.ndarray
    ):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for x in range(self.CHUNK_SIZE):
            row = []
            for y in range(self.CHUNK_SIZE):
                noise_value = noise(
                    [
                        (x + self.x * self.CHUNK_SIZE)
                        / (self.CHUNK_SIZE * self.world.world_size),
                        (y + self.y * self.CHUNK_SIZE)
                        / (self.CHUNK_SIZE * self.world.world_size),
                    ]
                )

                normal_value = normal[y + self.y * self.CHUNK_SIZE][
                    x + self.x * self.CHUNK_SIZE
                ]

                color = TileLookup.tiles["water"]["BASE_COLOR"]
                if noise_value < -0.2:
                    color = TileLookup.tiles["water"]["BASE_COLOR"]
                elif noise_value < -0.15:
                    color = TileLookup.tiles["sand"]["BASE_COLOR"]
                elif noise_value < 0.3:
                    color = TileLookup.tiles["grass"]["BASE_COLOR"]
                else:
                    color = TileLookup.tiles["stone"]["BASE_COLOR"]

                if color != TileLookup.tiles["water"]["BASE_COLOR"]:
                    color = Generation.brighten_color(
                        color, max(0.2, (-numpy.dot(normal_value, sun) - 0.35) * 4)
                    )

                color = Generation.brighten_color(
                    color, max(0.2, (1 + noise_value * 0.6))
                )

                row.append(Tile(self, x, y, color))
            tiles.append(row)
        return tiles
