import math
import random
import numpy
import pygame
from typing import List
from typing import TYPE_CHECKING
from environment.chunk import Chunk
from environment.generation import Generation
from environment.animal import Animal

if TYPE_CHECKING:
    from environment.camera import Camera


class World:
    def __init__(self, world_size_chunks: int):
        self.size_chunks = world_size_chunks
        self.size_tiles = world_size_chunks * Chunk.SIZE
        self.surf = pygame.Surface((self.size_tiles, self.size_tiles)).convert()

        # Terrain Generation
        self.seed = random.randint(1, 100)
        self.seed = 32
        print(self.seed)
        self.height_map = Generation.get_height_map(
            self.size_tiles,
            self.size_tiles,
            3,
            self.seed,
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
        #self.chunks[0][0].animals.append(Animal(self.chunks[0][0].tiles[7][7], pygame.Color(255, 0, 0)))

    def tick(self, delta_time: float):
        for y in range(self.size_chunks):
            for x in range(self.size_chunks):
                self.chunks[y][x].tick(delta_time)

    def render(self, camera: "Camera"):
        """
        Renders all chunks. Kept separate from tick() for it to run on separate clock.
        """
        for y in range(self.size_chunks):
            for x in range(self.size_chunks):
                self.chunks[y][x].render(camera)
        
        camera.render_world(self)
    
    def get_tile(self, world_x, world_y):
        chunk_x = world_x // Chunk.SIZE
        chunk_y = world_y // Chunk.SIZE
        tile_x = world_x - chunk_x * Chunk.SIZE
        tile_y = world_y - chunk_y * Chunk.SIZE
        
        return self.chunks[chunk_y][chunk_x].tiles[tile_y][tile_x]

    def initialize_chunks(self, world_size: int) -> "List[List[Chunk]]":
        """
        Returns grid of random Perlin noise generated chunks with dimensions world_size by world_size in chunks.
        """
        return [
            [Chunk(self, x, y) for x in range(world_size)] for y in range(world_size)
        ]
