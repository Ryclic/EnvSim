from typing import List
from environment.chunk import Chunk
import pygame as py


class World:
    def __init__(self, world_size: int, canvas: py.Surface):
        self.world_size = world_size
        # For some reason the complier doesn't recognize this variable as a 2d list
        self.chunks: List[List[Chunk]] = self.initialize_chunks()
        self.canvas = canvas

    def tick(self, delta_time: float):
        for y in range(self.world_size):
            for x in range(self.world_size):
                self.chunks[y][x].tick(delta_time)

    def render(self): # TODO: Make render visible chunks only.
        """
        Renders all chunks. Kept separate from tick() for it to run on separate clock.
        """
        for y in range(self.world_size):
            for x in range(self.world_size):
                self.chunks[y][x].render()

    def initialize_chunks(self, world_size: int) -> List[List[Chunk]]:
        """
        Returns grid of chunks with dimensions world_size by world_size in chunks.
        """
        return [
            [Chunk(self, x, y) for x in range(world_size)] for y in range(world_size)
        ]
