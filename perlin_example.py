# NOTE: This is ChatGPT generated, use as a template for now
# TODO: Figure out how to integrate Perlin noise with individually generated chunks, currently this does Perlin noise on the entire tilemap. We want individual chunks.

import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Perlin Noise Tilemap")

# Define tile size
TILE_SIZE = 32

# Tile types
TILE_GRASS = 0
TILE_WATER = 1
TILE_MOUNTAIN = 2

# Tile colors (instead of images)
GRASS_COLOR = (34, 139, 34)   # Green (Grass)
WATER_COLOR = (0, 0, 255)     # Blue (Water)
MOUNTAIN_COLOR = (139, 137, 137)  # Grey (Mountain)

# Tile colors mapping
TILE_COLORS = {
    TILE_GRASS: GRASS_COLOR,
    TILE_WATER: WATER_COLOR,
    TILE_MOUNTAIN: MOUNTAIN_COLOR
}

# Map dimensions
MAP_WIDTH = 50
MAP_HEIGHT = 50

# Perlin noise settings
scale = 0.1  # Larger scale = more zoomed out terrain
octaves = 6  # Number of "octaves" of noise
persistence = 0.5  # Amplitude decay for each octave
lacunarity = 2.0  # Frequency growth for each octave
seed = random.randint(0, 100)

# Generate a tilemap using Perlin noise
def generate_perlin_tilemap(width, height):
    tilemap = []
    for y in range(height):
        row = []
        for x in range(width):
            # Generate Perlin noise value for the current tile
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
        tilemap.append(row)
    return tilemap

# Initial tilemap generation
tilemap = generate_perlin_tilemap(MAP_WIDTH, MAP_HEIGHT)

# Function to draw the tilemap
def draw_tilemap():
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            pygame.draw.rect(screen, TILE_COLORS[tile], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game loop
running = True
last_time = pygame.time.get_ticks()  # Store the last time the tilemap was generated
regenerate_interval = 3000  # 3 seconds in milliseconds

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if 3 seconds have passed since the last tilemap generation
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= regenerate_interval:
        # Regenerate the Perlin tilemap
        seed = random.randint(0, 100)
        tilemap = generate_perlin_tilemap(MAP_WIDTH, MAP_HEIGHT)
        last_time = current_time  # Update the time of the last regeneration
    # Fill the screen with black
    screen.fill((0, 0, 0))  
    draw_tilemap()  # Draw the current tilemap on the screen

    pygame.display.flip()  # Update the display

pygame.quit()

