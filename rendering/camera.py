import math
from typing import Tuple, TYPE_CHECKING
import pygame
from environment.tile import Tile

if TYPE_CHECKING:
    from environment.world import World
    from environment.chunk import Chunk


class Camera:
    INITIAL_PAN_SPEED = 300
    INITIAL_ZOOM_SPEED = 0.5
    SPEED_FACTOR = 2
    # Distance outside the camera FOV such that chunks are still rendered
    RENDER_BUFFER = 10

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1

        self.last_cached_zoom = 1
        self.cached_scaled_surf = None
        self.cached_view_rect = None

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
        (OBSOLETE) Renders tile as a square relative to camera with color based on coordinates relative to chunk and world.
        """
        pygame.draw.rect(
            self.screen,
            tile.color,
            pygame.Rect(
                (tile.get_world_x() - self.camera_x) * self.zoom
                + self.screen.get_width() / 2,
                (tile.get_world_y() - self.camera_y) * self.zoom
                + self.screen.get_height() / 2,
                self.zoom + 1,
                self.zoom + 1,
            ),
        )

    def fast_render_world(self, world: "World"):
        """
        A work-in-progress way to render the world selectively.
        """
        viewable_world_rect: pygame.Rect = self.get_world_rect()
        prezoom_surf = pygame.Surface(viewable_world_rect.size)
        overlap_rect = viewable_world_rect.clip(world.surf.get_rect())

        if overlap_rect.width > 0 and overlap_rect.height > 0:
            prezoom_surf.blit(
                world.surf,
                (
                    overlap_rect.x - viewable_world_rect.x,
                    overlap_rect.y - viewable_world_rect.y,
                ),
                area=overlap_rect,
            )

        world_scaled_surf = pygame.transform.scale(prezoom_surf, (prezoom_surf.get_width() * self.zoom, prezoom_surf.get_height() * self.zoom))

        self.screen.blit(
            world_scaled_surf,
            (
                (viewable_world_rect.center[0] - self.camera_x) * self.zoom,
                (viewable_world_rect.center[1] - self.camera_y) * self.zoom,
            ),
        )

    def render_world(self, world: "World"):
        """
        Optimized way to render the world using caching and selective rendering.
        """
        viewable_world_rect: pygame.Rect = self.get_world_rect()
        
        # Caching, recaculation if zoom change, no cache, or camera pan
        if (self.zoom != self.last_cached_zoom or self.cached_scaled_surf is None or 
            self.cached_view_rect != viewable_world_rect):
            
            visible_surf = pygame.Surface(viewable_world_rect.size)
            overlap_rect = viewable_world_rect.clip(world.surf.get_rect())
            
            if overlap_rect.width > 0 and overlap_rect.height > 0:
                # Only blit the visible portion
                visible_surf.blit(
                    world.surf,
                    (
                        overlap_rect.x - viewable_world_rect.x,
                        overlap_rect.y - viewable_world_rect.y,
                    ),
                    area=overlap_rect,
                )
                
                # Scale visible portion
                self.cached_scaled_surf = pygame.transform.scale(
                    visible_surf,
                    (
                        int(visible_surf.get_width() * self.zoom),
                        int(visible_surf.get_height() * self.zoom)
                    )
                )
                self.last_cached_zoom = self.zoom
                self.cached_view_rect = viewable_world_rect
        
        screen_center_x = self.screen.get_width() / 2
        screen_center_y = self.screen.get_height() / 2
        
        # Calc correct position to blit
        blit_x = screen_center_x - (self.camera_x - viewable_world_rect.x) * self.zoom
        blit_y = screen_center_y - (self.camera_y - viewable_world_rect.y) * self.zoom
        
        self.screen.blit(
            self.cached_scaled_surf,
            (blit_x, blit_y)
        )

    def get_world_rect(self) -> pygame.rect:
        """
        Gets the rect of the screen in world coorindates.
        """
        world_x = (-self.screen.get_width() / 2) / self.zoom + self.camera_x
        world_y = (-self.screen.get_height() / 2) / self.zoom + self.camera_y

        return pygame.Rect(
            math.floor(world_x),
            math.floor(world_y),
            math.ceil(self.screen.get_width() / self.zoom + world_x) - math.floor(world_x),
            math.ceil(self.screen.get_height() / self.zoom + world_y) - math.floor(world_y),
        )

    def get_world_tuple(self) -> Tuple[float]:
        """
        Gets a tuple of the screen in world coorindates.
        """
        world_x = (-self.screen.get_width() / 2) / self.zoom + self.camera_x
        world_y = (-self.screen.get_height() / 2) / self.zoom + self.camera_y

        return (
            world_x,
            world_y,
            self.screen.get_width() / self.zoom,
            self.screen.get_height() / self.zoom,
        )

    def is_chunk_in_camera(self, chunk: "Chunk") -> bool:
        screen_world_dimensions = self.get_world_rect()

        return (
            screen_world_dimensions.x - self.RENDER_BUFFER
            < chunk.get_world_x() + chunk.SIZE
            and chunk.get_world_x()
            < screen_world_dimensions.x
            + self.screen.get_width() / self.zoom
            + self.RENDER_BUFFER
            and screen_world_dimensions.y - self.RENDER_BUFFER
            < chunk.get_world_y() + chunk.SIZE
            and chunk.get_world_y()
            < screen_world_dimensions.y
            + self.screen.get_height() / self.zoom
            + self.RENDER_BUFFER
        )
