import pygame as py
from environment.tile import Tile


class Rendering:
    def __init__(self, canvas: py.Surface):
        self.canvas = canvas
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1

    def render_tile(self, tile: Tile):
        """
        Renders tile as a square relative to camera.
        """
        py.draw.rect(
            self.canvas,
            tile.color,
            py.Rect(
                (tile.x - self.camera_x) * self.zoom,
                (tile.y - self.camera_y) * self.zoom,
                Tile.TILE_WIDTH * self.zoom,
                Tile.TILE_WIDTH * self.zoom,
            ),
        )
