from typing import TYPE_CHECKING, List
import pygame
from environment.generation import Generation
from environment.tile import Tile

if TYPE_CHECKING:
    from environment.world import World
    from rendering.camera import Camera


class Chunk:
    SIZE: int = 16

    def __init__(self, world: "World", x: int, y: int):
        self.world = world
        self.x = x
        self.y = y
        self.surf = pygame.Surface((Chunk.SIZE, Chunk.SIZE)).convert()
        # Change to initialize_debug_tiles for debug tilemap
        self.tiles = self.initialize_random_tiles()

    def tick(self, delta_time: float):
        for y in range(Chunk.SIZE):
            for x in range(Chunk.SIZE):
                self.tiles[y][x].tick(delta_time)

    def render(self, camera: "Camera"):
        if not camera.is_chunk_in_camera(self):
            return  # Prevent rendering chunks outside the camera FOV

        self.world.surf.blit(
            self.surf,
            (self.get_world_x(), self.get_world_y()),
        )

    def update_surf(self, x, y, color=None):
        surf_array = pygame.surfarray.pixels3d(self.surf)
        if type(color) == pygame.Color:
            surf_array[x, y] = (color.r, color.g, color.b)
        else:
            surf_array[x, y] = color
        del surf_array  # To prevent surface locking.

    def get_world_x(self) -> int:
        return self.x * self.SIZE

    def get_world_y(self) -> int:
        return self.y * self.SIZE

    def initialize_debug_tiles(self) -> "List[List[Tile]]":
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
                        int(255 * x / Chunk.SIZE),
                        int(255 * y / Chunk.SIZE),
                        int(255 * (self.x + self.y) / (2 * self.world.size_chunks)),
                    ),  # To distinguish each tile for now
                )
                for x in range(Chunk.SIZE)
            ]
            for y in range(Chunk.SIZE)
        ]

    def initialize_random_tiles(self) -> "List[List[Tile]]":
        return Generation.generate_random_chunk(
            self,
            self.world.height_map,
            self.world.normal_map,
            self.world.steepness_map,
            self.world.light_vector,
        )
