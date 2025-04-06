import random
from typing import TYPE_CHECKING, List
from perlin_noise import PerlinNoise
from environment.tile_lookup import TileLookup
from environment.tile import Tile

if TYPE_CHECKING:
    from environment.chunk import Chunk


class Generation:
    SCALE = 0.1
    OCTAVES = 6
    PERSISTENCE = 0.5
    LACUNARITY = 2.0
    SEED = random.randint(0, 100)
    NOISE = PerlinNoise(octaves=OCTAVES, seed=SEED)

    def generate_random_chunk(self: "Chunk"):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for x in range(self.CHUNK_SIZE):
            row = []
            for y in range(self.CHUNK_SIZE):
                noise_value = Generation.NOISE(
                    [
                        (x + self.x * self.CHUNK_SIZE)
                        / (self.CHUNK_SIZE * self.world.world_size),
                        (y + self.y * self.CHUNK_SIZE)
                        / (self.CHUNK_SIZE * self.world.world_size),
                    ]
                )
                if noise_value < -0.1:
                    row.append(Tile(self, x, y, TileLookup.tiles["water"]["BASE_COLOR"]))
                elif noise_value < -0.05:
                    row.append(Tile(self, x, y, TileLookup.tiles["sand"]["BASE_COLOR"]))
                elif noise_value < 0.3:
                    row.append(Tile(self, x, y, TileLookup.tiles["grass"]["BASE_COLOR"]))
                else:
                    row.append(Tile(self, x, y, TileLookup.tiles["stone"]["BASE_COLOR"]))
            tiles.append(row)
        return tiles
