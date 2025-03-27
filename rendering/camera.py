from typing import Tuple
import pygame
from environment.chunk import Chunk
from environment.tile import Tile


class Camera:
    INITIAL_PAN_SPEED = 300
    INITIAL_ZOOM_SPEED = 0.5
    SPEED_FACTOR = 2
    RENDER_BUFFER = 10 # Distance outside the camera FOV such that chunks are still rendered

    def __init__(self, canvas: pygame.Surface):
        self.canvas = canvas
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1

        self.pan_speed = self.INITIAL_PAN_SPEED
        self.zoom_speed = self.INITIAL_ZOOM_SPEED

    def tick(self, delta_time: float, controls: dict[str, bool]):
        self.pan_speed = self.INITIAL_PAN_SPEED * self.SPEED_FACTOR ** int(
            controls["speed"]
        )
        self.zoom_speed = self.INITIAL_ZOOM_SPEED * self.SPEED_FACTOR ** int(
            controls["speed"]
        )

        self.camera_x += (
            self.pan_speed
            * (int(controls["right"]) - int(controls["left"]))
            * delta_time
            / self.zoom
        )
        self.camera_y += (
            self.pan_speed
            * (int(controls["down"]) - int(controls["up"]))
            * delta_time
            / self.zoom
        )
        self.zoom += (
            self.zoom_speed
            * (int(controls["zoom_in"]) - int(controls["zoom_out"]))
            * delta_time
            * self.zoom
        )

    def render_tile_debug(self, tile: "Tile"):
        """
        Renders tile as a square relative to camera with color based on coordinates relative to chunk and world.
        """
        pygame.draw.rect(
            self.canvas,
            tile.color,
            pygame.Rect(
                (tile.get_world_x() - self.camera_x) * self.zoom
                + self.canvas.get_width() / 2,
                (tile.get_world_y() - self.camera_y) * self.zoom
                + self.canvas.get_height() / 2,
                tile.TILE_WIDTH * self.zoom + 1,
                tile.TILE_WIDTH * self.zoom + 1,
            ),
        )

    def get_camera_world_position(self) -> Tuple[int]:
        """
        Gets the top-left point of the screen in world coorindates.
        """
        world_x: int = round((-self.canvas.get_width() / 2) / self.zoom + self.camera_x)
        world_y: int = round(
            (-self.canvas.get_height() / 2) / self.zoom + self.camera_y
        )
        return (world_x, world_y)

    def is_chunk_in_camera(self, chunk: Chunk) -> bool:
        screen_world_dimensions = self.get_camera_world_position()

        return (
            screen_world_dimensions[0] - self.RENDER_BUFFER < chunk.get_world_x() + Chunk.CHUNK_SIZE * Tile.TILE_WIDTH
            and chunk.get_world_x()
            < screen_world_dimensions[0]
            + self.canvas.get_width() / self.zoom
            + self.RENDER_BUFFER
            and screen_world_dimensions[1] - self.RENDER_BUFFER < chunk.get_world_y() + Chunk.CHUNK_SIZE * Tile.TILE_WIDTH
            and chunk.get_world_y()
            < screen_world_dimensions[1]
            + self.canvas.get_height() / self.zoom
            + self.RENDER_BUFFER
        )
