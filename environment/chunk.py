from typing import List
from environment.tile import Tile
from environment.world import World
import pygame as py


class Chunk:
    CHUNK_SIZE = 16

    def __init__(self, world: World, x: int, y: int):
        self.world = world
        self.x = x
        self.y = y
        self.tiles = self.initialize_tiles()

    def tick(self, delta_time: float):
        for y in range(Chunk.CHUNK_SIZE):
            for x in range(Chunk.CHUNK_SIZE):
                self.tiles[y][x].tick(delta_time)

    def render(self):
        for y in range(Chunk.CHUNK_SIZE):
            for x in range(Chunk.CHUNK_SIZE):
                self.tiles[y][x].render()

    def initialize_tiles(self) -> List[List[Tile]]:
        """
        Initializes grid of tiles.
        """
        return [
            [
                Tile(
                    self,
                    x,
                    y,
                    py.Color(
                        255 * x / Chunk.CHUNK_SIZE,
                        255 * y / Chunk.CHUNK_SIZE,
                        255 * (self.x + self.y) / (2 * self.world.world_size),
                    ),  # To distinguish each tile for now
                )
                for x in range(Chunk.CHUNK_SIZE)
            ]
            for y in range(Chunk.CHUNK_SIZE)
        ]
