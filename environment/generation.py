import random
import noise
from environment.tile_lookup import TileLookup
from environment.chunk import Chunk

class Generation:

    def generate_random_chunk(self):
        """
        Initializes Perlin generated grid of tiles.
        """
        tiles = []
        for x in range(Chunk.CHUNK_SIZE):
            row = []
            for y in range(Chunk.CHUNK_SIZE):
                noise_value = noise.pnoise2(x * scale,
                                            y * scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=seed)
                # Map noise values to tile types
                if noise_value < -0.1:
                    row.append(TILE_WATER)  # Water
                elif noise_value < 0.2:
                    row.append(TILE_GRASS)  # Grass
                else:
                    row.append(TILE_MOUNTAIN)  # Mountain
            tiles.append(row)
