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
    def get_height_map(
        height: int,
        width: int,
        octaves: float,
        seed: int,
        lacunarity: float,
        persistance: float,
    ):
        layers = [PerlinNoise(octaves=4, seed=seed) for i in range(octaves)]
        height_map = numpy.zeros((height, width))

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

                height_map[y][x] = noise_value

        return height_map

    def get_normal_map(
        height_map: numpy.ndarray, width: int, height: int, strength: float = 1.0
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

                dzdx = (height_map[x2, y] - height_map[x1, y]) * strength
                dzdy = (height_map[x, y2] - height_map[x, y1]) * strength

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

    def get_steepness_map(normal_map):
        """
        Returns steepness map from a normal map.
        """
        return numpy.arccos(
            numpy.clip(
                numpy.sum(normal_map * numpy.array([0, 0, 1]).reshape(1, 1, 3), axis=2),
                -1.0,
                1.0,
            )
        )

    def generate_random_chunk(
        self: "Chunk",
        height_map: numpy.ndarray,
        normal_map: numpy.ndarray,
        steepness_map: numpy.ndarray,
        light_vector: numpy.ndarray,
    ):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for y in range(self.SIZE):
            row = []
            for x in range(self.SIZE):
                world_x = x + self.x * self.SIZE
                world_y = y + self.y * self.SIZE
                
                height_value = height_map[world_x, world_y]
                normal_value = normal_map[world_x, world_y]
                steepness_value = steepness_map[world_x, world_y]

                material = ""
                if height_value < -0.28:
                    material = "water"
                elif height_value < -0.2:
                    material = "shallow_water"
                elif steepness_value > 0.1:
                    material = "stone"
                elif height_value > 0.4:
                    material = "snow"
                elif height_value > 0.35:
                    material = "stone"
                elif height_value < -0.15:
                    material = "sand"
                elif steepness_value > 0.08:
                    material = "dirt"
                else:
                    material = "grass"
                color = TileLookup.tiles[material]["BASE_COLOR"]

                # Water doesn't get shadows cause its flat.
                if (
                    color != TileLookup.tiles["water"]["BASE_COLOR"]
                    and color != TileLookup.tiles["shallow_water"]["BASE_COLOR"]
                ):
                    color = Generation.brighten_color(
                        color,
                        max(0.2, (-numpy.dot(normal_value, light_vector) - 0.35) * 4),
                    )

                # Shading based on height.
                color = Generation.brighten_color(
                    color, max(0.2, (1 + height_value * 0.6))
                )

                # Normal map coloring if needed.
                r, g, b = [int(i * 255) for i in ((normal_value + 1) / 2).clip(0, 1)]
                normal_color = pygame.Color(r, g, b)

                row.append(Tile(self, x, y, color, material))
            tiles.append(row)
        return tiles
