import pygame


class TileLookup:
    tiles = {
        "grass": {
            "BASE_COLOR": pygame.Color(34, 143, 70)
        },
        "stone": {
            "BASE_COLOR": pygame.Color(144, 163, 150)
        },
        "water": {
            "BASE_COLOR": pygame.Color(70, 150, 219)
        },
        "sand": {
            "BASE_COLOR": pygame.Color(219, 203, 156)
        }
    }
