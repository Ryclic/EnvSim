from typing import TYPE_CHECKING
import random
import noise
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

    def generate_random_chunk(self):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for x in range(self.CHUNK_SIZE):
            row = []
            for y in range(self.CHUNK_SIZE):
                noise_value = noise.pnoise2((x + self.get_world_x()) * Generation.SCALE,
                                            (y + self.get_world_y()) * Generation.SCALE,
                                            octaves=Generation.OCTAVES,
                                            persistence=Generation.PERSISTENCE,
                                            lacunarity=Generation.LACUNARITY,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=Generation.SEED)
                # Map noise values to tile types
                if noise_value < -0.1:
                    row.append(Tile(self, x, y, TileLookup.tiles["water"]["COLOR"]))
                elif noise_value < 0.2:
                    row.append(Tile(self, x, y, TileLookup.tiles["grass"]["COLOR"]))
                else:
                    row.append(Tile(self, x, y, TileLookup.tiles["stone"]["COLOR"]))
            tiles.append(row)
        return tiles

