from environment.chunk import Chunk
import pygame as py


class Tile:
    TILE_WIDTH = 1

    def __init__(self, chunk: Chunk, x: int, y: int, starting_color: py.Color):
        self.chunk = chunk
        self.x = x
        self.y = y
        self.color = starting_color

    def get_global_x(self):
        return self.x + self.chunk.x * Chunk.CHUNK_SIZE

    def get_global_y(self):
        return self.y + self.chunk.y * Chunk.CHUNK_SIZE

    def tick(self, delta_time: float):  # TODO
        pass

    def render(self):  # TODO
        pass
