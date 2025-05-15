import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment.chunk import Chunk
    from environment.camera import Camera


class Tile:
    def __init__(self, chunk: "Chunk", x: int, y: int, starting_color: pygame.Color, material):
        self.chunk = chunk
        self.x = x
        self.y = y
        self.color = starting_color
        self.material = material
        self.update()

    def get_world_x(self) -> int:
        return self.x + self.chunk.x * self.chunk.SIZE

    def get_world_y(self) -> int:
        return self.y + self.chunk.y * self.chunk.SIZE

    def tick(self, delta_time: float):  # TODO
        pass

    def render(self, camera: "Camera"):
        camera.render_tile_debug(self)
    
    def get_neighbors(self):
        world_x, world_y = self.get_world_x(), self.get_world_y()
        neighbors = set()
        for dy in range(-1, 1):
            for dx in range(-1, 1):
                if dx != 0 or dy != 0:
                    neighbors.add(self.chunk.world.get_tile(world_x + dx, world_y + dy))
        return neighbors
    
    def update(self):
        self.chunk.update_surf(self.x, self.y, self.color)
