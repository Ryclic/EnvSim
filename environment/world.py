import math
import random
import numpy
import pygame
from typing import List
from typing import TYPE_CHECKING
from environment.chunk import Chunk
from environment.generation import Generation

if TYPE_CHECKING:
    from rendering.camera import Camera


class World:
    def __init__(self, world_size_chunks: int):
        self.size_chunks = world_size_chunks
        self.size_tiles = world_size_chunks * Chunk.SIZE
        self.surf = pygame.Surface((self.size_tiles, self.size_tiles)).convert()

        # Terrain Generation
        self.height_map = Generation.get_height_map(
            self.size_tiles,
            self.size_tiles,
            3,
            random.randint(0, 100),
            2.4,
            0.5,
        )
        self.normal_map = Generation.get_normal_map(
            self.height_map, self.size_tiles, self.size_tiles, world_size_chunks / 8
        )
        self.steepness_map = Generation.get_steepness_map(self.normal_map)

        self.light_vector = numpy.array(
            [-math.sqrt(3) / 3, math.sqrt(3) / 3, -math.sqrt(3) / 3]
        )
        self.chunks = self.initialize_chunks(world_size_chunks)

    def tick(self, delta_time: float):
        for y in range(self.size_chunks):
            for x in range(self.size_chunks):
                self.chunks[y][x].tick(delta_time)

    def render(self, camera: "Camera"):  # TODO: Make render visible chunks only.
        """
        Renders all chunks. Kept separate from tick() for it to run on separate clock.
        """
        for y in range(self.size_chunks):
            for x in range(self.size_chunks):
                self.chunks[y][x].render(camera)
        
        camera.render_world(self)

    def initialize_chunks(self, world_size: int) -> "List[List[Chunk]]":
        """
        Returns grid of chunks with dimensions world_size by world_size in chunks.
        """
        return [
            [Chunk(self, x, y) for x in range(world_size)] for y in range(world_size)
        ]
