import pygame


class TileLookup:
    tiles = {
        "grass": {
            "BASE_COLOR": pygame.Color(83, 115, 56)
        },
        "stone": {
            "BASE_COLOR": pygame.Color(69, 64, 59)
        },
        "water": {
            "BASE_COLOR": pygame.Color(18, 70, 112)
        },
        "shallow_water": {
            "BASE_COLOR": pygame.Color(36, 105, 128)
        },
        "sand": {
            "BASE_COLOR": pygame.Color(219, 203, 156)
        },
        "dirt": {
            "BASE_COLOR": pygame.Color(97, 75, 49)
        },
        "snow": {
            "BASE_COLOR": pygame.Color(232, 229, 225)
        }
    }
