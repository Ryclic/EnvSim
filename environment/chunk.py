from typing import List, Tuple
from typing import TYPE_CHECKING
import pygame
from environment.tile import Tile

if TYPE_CHECKING:
    from environment.world import World
    from rendering.camera import Camera


class Chunk:
    CHUNK_SIZE: int = 8

    def __init__(self, world: "World", x: int, y: int):
        self.world = world
        self.x = x
        self.y = y
        self.tiles = self.initialize_tiles()

    def tick(self, delta_time: float):
        for y in range(Chunk.CHUNK_SIZE):
            for x in range(Chunk.CHUNK_SIZE):
                self.tiles[y][x].tick(delta_time)

    def render(self, camera: "Camera"):
        if not camera.is_chunk_in_camera(self):
            return # Prevent rendering chunks outside the camera FOV

        for y in range(Chunk.CHUNK_SIZE):
            for x in range(Chunk.CHUNK_SIZE):
                self.tiles[y][x].render(camera)

    def get_world_x(self) -> int:
        return self.x * self.CHUNK_SIZE * Tile.TILE_WIDTH

    def get_world_y(self) -> int:
        return self.y * self.CHUNK_SIZE * Tile.TILE_WIDTH

    def initialize_tiles(self) -> "List[List[Tile]]":
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
                        int(255 * x / Chunk.CHUNK_SIZE),
                        int(255 * y / Chunk.CHUNK_SIZE),
                        int(255 * (self.x + self.y) / (2 * self.world.world_size)),
                    ),  # To distinguish each tile for now
                )
                for x in range(Chunk.CHUNK_SIZE)
            ]
            for y in range(Chunk.CHUNK_SIZE)
        ]
