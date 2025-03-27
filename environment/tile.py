import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment.chunk import Chunk
    from rendering.camera import Camera


class Tile:
    TILE_WIDTH = 10

    def __init__(self, chunk: "Chunk", x: int, y: int, starting_color: pygame.Color):
        self.chunk = chunk
        self.x = x
        self.y = y
        self.color = starting_color

    def get_world_x(self) -> int:
        return (self.x + self.chunk.x * self.chunk.CHUNK_SIZE) * self.TILE_WIDTH

    def get_world_y(self) -> int:
        return (self.y + self.chunk.y * self.chunk.CHUNK_SIZE) * self.TILE_WIDTH

    def tick(self, delta_time: float):  # TODO
        pass

    def render(self, camera: "Camera"):
        camera.render_tile_debug(self)
