from typing import TYPE_CHECKING, List
import pygame
from environment.generation import Generation
from environment.tile import Tile
from environment.animal import Animal, Fox, Rabbit
import random

if TYPE_CHECKING:
    from environment.world import World
    from environment.camera import Camera


class Chunk:
    SIZE: int = 16

    def __init__(self, world: "World", x: int, y: int):
        self.world = world
        self.x = x
        self.y = y
        self.surf = pygame.Surface((Chunk.SIZE, Chunk.SIZE)).convert()
        # Change to initialize_debug_tiles for debug tilemap
        self.tiles = self.initialize_random_tiles()
        self.animals = []

        for x in (2, 12):
            self.animals.append(
                Fox(
                    self.tiles[x][x],
                )
                if random.random() < 0.2 else
                Rabbit(
                    self.tiles[x][x],
                )
            )

    def tick(self, delta_time: float):
        for y in range(Chunk.SIZE):
            for x in range(Chunk.SIZE):
                self.tiles[y][x].tick(delta_time)

        for animal in self.animals:
            animal.tick(delta_time)

    def render(self, camera: "Camera"):
        if not camera.is_chunk_in_camera(self):
            return  # Prevent rendering chunks outside the camera FOV

        self.world.surf.blit(
            self.surf,
            (self.get_world_x(), self.get_world_y()),
        )

    def update_surf(self, x, y, color=None):
        surf_array = pygame.surfarray.pixels3d(self.surf)
        if type(color) == pygame.Color:
            surf_array[x, y] = (color.r, color.g, color.b)
        else:
            surf_array[x, y] = color
        del surf_array  # To prevent surface locking.

    def get_world_x(self) -> int:
        return self.x * self.SIZE

    def get_world_y(self) -> int:
        return self.y * self.SIZE

    def get_neighbors(self):
        chunk_x, chunk_y = self.x, self.y
        neighbors = set()
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (
                    (dx != 0 or dy != 0)
                    and 0 <= chunk_x + dx < self.world.size_chunks
                    and 0 <= chunk_y + dy < self.world.size_chunks
                ):
                    neighbors.add(self.world.chunks[chunk_y + dy][chunk_x + dx])
        return neighbors

    def initialize_debug_tiles(self) -> "List[List[Tile]]":
        """
        Initializes grid of tiles.
        """
        return [
            [
                Tile(
                    self,
                    x,
                    y,
                    pygame.Color(
                        int(255 * x / Chunk.SIZE),
                        int(255 * y / Chunk.SIZE),
                        int(255 * (self.x + self.y) / (2 * self.world.size_chunks)),
                    ),  # To distinguish each tile for now
                )
                for x in range(Chunk.SIZE)
            ]
            for y in range(Chunk.SIZE)
        ]

    def initialize_random_tiles(self) -> "List[List[Tile]]":
        return Generation.generate_random_chunk(
            self,
            self.world.height_map,
            self.world.normal_map,
            self.world.steepness_map,
            self.world.light_vector,
        )
