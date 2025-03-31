import pygame


class TileLookup:
    tiles = {
        "grass": {
            "COLOR": pygame.Color(0, 255, 0)
        },
        "dirt": {
            "COLOR": pygame.Color(150, 75, 0)
        },
        "water": {
            "COLOR": pygame.Color(0, 0, 255)
        }
    }
