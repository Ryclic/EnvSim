import math
import random
import numpy
from typing import List
from typing import TYPE_CHECKING
from environment.chunk import Chunk
from environment.generation import Generation

if TYPE_CHECKING:
    from rendering.camera import Camera


class World:
    def __init__(self, world_size: int):
        self.world_size = world_size
        self.world_noise = Generation.get_noise(
            world_size * Chunk.CHUNK_SIZE,
            world_size * Chunk.CHUNK_SIZE,
            3,
            random.randint(0, 100),
            2.4,
            0.5,
        )
        self.world_normal = Generation.get_normal(
            self.world_noise,
            self.world_size * Chunk.CHUNK_SIZE,
            self.world_size * Chunk.CHUNK_SIZE,
            1
        )
        self.sun_vector = numpy.array(
            [-math.sqrt(3) / 3, math.sqrt(3) / 3, -math.sqrt(3) / 3]
        )
        # For some reason the complier doesn't recognize this variable as a 2d list
        self.chunks: List[List[Chunk]] = self.initialize_chunks(world_size)

    def tick(self, delta_time: float):
        for y in range(self.world_size):
            for x in range(self.world_size):
                self.chunks[y][x].tick(delta_time)

    def render(self, camera: "Camera"):  # TODO: Make render visible chunks only.
        """
        Renders all chunks. Kept separate from tick() for it to run on separate clock.
        """
        for y in range(self.world_size):
            for x in range(self.world_size):
                self.chunks[y][x].render(camera)

    def initialize_chunks(self, world_size: int) -> "List[List[Chunk]]":
        """
        Returns grid of chunks with dimensions world_size by world_size in chunks.
        """
        return [
            [Chunk(self, x, y) for x in range(world_size)] for y in range(world_size)
        ]
