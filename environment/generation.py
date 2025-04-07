import math
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
    def get_noise(
        height: int,
        width: int,
        octaves: float,
        seed: int,
        lacunarity: float,
        persistance: float,
    ):
        layers = [PerlinNoise(octaves=8, seed=seed) for i in range(octaves)]
        noise = numpy.zeros((height, width))

        for y in range(height):
            for x in range(width):
                amplitude = 1.0
                frequency = 1.0
                noise_value = 0.0

                for i in range(octaves):
                    nx = x / width * frequency
                    ny = y / height * frequency
                    value = layers[i]([nx, ny])
                    noise_value += value * amplitude

                    frequency *= lacunarity
                    amplitude *= persistance

                noise[y][x] = noise_value

        return noise

    def get_normal(
        noise: numpy.ndarray, width: int, height: int, strength: float = 1.0
    ):
        normal_map = numpy.zeros((height, width, 3))

        for y in range(height):
            for x in range(width):
                x2, x1 = x + 1, x - 1
                if x == 0:
                    x1 = x
                elif x == width - 1:
                    x2 = x

                y2, y1 = y + 1, y - 1
                if y == 0:
                    y1 = y
                elif y == height - 1:
                    y2 = y

                dzdx = (noise[y][x2] - noise[y][x1]) * strength
                dzdy = (noise[y2][x] - noise[y1][x]) * strength

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

    def angle_between(v1, v2):
        """
        Returns the angle in radians between vectors 'v1' and 'v2'
        """
        return numpy.arccos(
            numpy.clip(
                numpy.dot(v1 / numpy.linalg.norm(v1), v2 / numpy.linalg.norm(v2)),
                -1.0,
                1.0,
            )
        )

    def generate_random_chunk(
        self: "Chunk", noise: numpy.ndarray, normal: numpy.ndarray, sun: numpy.ndarray
    ):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for x in range(self.CHUNK_SIZE):
            row = []
            for y in range(self.CHUNK_SIZE):
                noise_value = noise[y + self.y * self.CHUNK_SIZE][x + self.x * self.CHUNK_SIZE]

                normal_value = normal[y + self.y * self.CHUNK_SIZE][
                    x + self.x * self.CHUNK_SIZE
                ]
                steepness = Generation.angle_between(
                    normal_value, numpy.array([0, 0, 1])
                )

                color = TileLookup.tiles["water"]["BASE_COLOR"]
                if noise_value < -0.28:
                    color = TileLookup.tiles["water"]["BASE_COLOR"]
                elif noise_value < -0.2:
                    color = TileLookup.tiles["shallow_water"]["BASE_COLOR"]
                elif steepness > 0.1:
                    color = TileLookup.tiles["stone"]["BASE_COLOR"]
                elif noise_value > 0.4:
                    color = TileLookup.tiles["snow"]["BASE_COLOR"]
                elif noise_value > 0.35:
                    color = TileLookup.tiles["stone"]["BASE_COLOR"]
                elif noise_value < -0.15:
                    color = TileLookup.tiles["sand"]["BASE_COLOR"]
                elif steepness > 0.08:
                    color = TileLookup.tiles["dirt"]["BASE_COLOR"]
                else:
                    color = TileLookup.tiles["grass"]["BASE_COLOR"]

                if color != TileLookup.tiles["water"]["BASE_COLOR"] and color != TileLookup.tiles["shallow_water"]["BASE_COLOR"]:
                    color = Generation.brighten_color(
                        color, max(0.2, (-numpy.dot(normal_value, sun) - 0.35) * 4)
                    )

                color = Generation.brighten_color(
                    color, max(0.2, (1 + noise_value * 0.6))
                )

                # Normal Map
                r, g, b = [int(i * 255) for i in ((normal_value + 1) / 2).clip(0, 1)]
                normal_color = pygame.Color(r, g, b)

                row.append(Tile(self, x, y, color))
            tiles.append(row)
        return tiles
