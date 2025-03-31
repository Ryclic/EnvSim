import pygame


class TileLookup:
    tiles = {
        "grass": {
            "COLOR": pygame.Color(0, 255, 0)
        },
        "stone": {
            "COLOR": pygame.Color(128, 128, 128)
        },
        "water": {
            "COLOR": pygame.Color(0, 0, 255)
        }
    }
