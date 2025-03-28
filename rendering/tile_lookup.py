import pygame


class TileLookup:
    grass = {  # TODO: Change to dictionaries for different biomes, climates, altitudes, etc.
        "COLOR": pygame.Color(0, 255, 0)
    }
    dirt = {
        "COLOR": pygame.Color(150, 75, 0)
    }
    water = {
        "COLOR": pygame.Color(0, 0, 255)
    }
