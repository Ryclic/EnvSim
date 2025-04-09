import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment.chunk import Chunk
    from rendering.camera import Camera


class Tile:
    def __init__(self, chunk: "Chunk", x: int, y: int, starting_color: pygame.Color):
        self.chunk = chunk
        self.x = x
        self.y = y
        self.color = starting_color
        self.update()

    def get_world_x(self) -> int:
        return self.x + self.chunk.x * self.chunk.SIZE

    def get_world_y(self) -> int:
        return self.y + self.chunk.y * self.chunk.SIZE

    def tick(self, delta_time: float):  # TODO
        pass

    def render(self, camera: "Camera"):
        camera.render_tile_debug(self)
    
    def update(self):
        self.chunk.update_surf(self.x, self.y, self.color)
