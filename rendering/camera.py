import pygame
from environment.tile import Tile


class Camera:
    INITIAL_PAN_SPEED = 300
    INITIAL_ZOOM_SPEED = 0.5
    SPEED_FACTOR = 2

    def __init__(self, canvas: pygame.Surface):
        self.canvas = canvas
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1

        self.pan_speed = self.INITIAL_PAN_SPEED
        self.zoom_speed = self.INITIAL_ZOOM_SPEED
    
    def tick(self, delta_time: float, controls: dict[str, bool]):
        self.pan_speed = self.INITIAL_PAN_SPEED * self.SPEED_FACTOR**int(controls["speed"])
        self.zoom_speed = self.INITIAL_ZOOM_SPEED * self.SPEED_FACTOR**int(controls["speed"])

        self.camera_x += self.pan_speed * (int(controls["right"]) - int(controls["left"])) * delta_time / self.zoom
        self.camera_y += self.pan_speed * (int(controls["down"]) - int(controls["up"])) * delta_time / self.zoom
        self.zoom += self.zoom_speed * (int(controls["zoom_in"]) - int(controls["zoom_out"])) * delta_time * self.zoom

    def render_tile_debug(self, tile: "Tile"):
        """
        Renders tile as a square relative to camera with color based on coordinates relative to chunk and world.
        """
        pygame.draw.rect(
            self.canvas,
            tile.color,
            pygame.Rect(
                (tile.get_global_x() * tile.TILE_WIDTH - self.camera_x) * self.zoom + self.canvas.get_width() / 2,
                (tile.get_global_y() * tile.TILE_WIDTH - self.camera_y) * self.zoom + self.canvas.get_height() / 2,
                tile.TILE_WIDTH * self.zoom + 1,
                tile.TILE_WIDTH * self.zoom + 1,
            ),
        )
