import random

class Animal:
    """
    Generic base class for animal, used for implementation of other animals.
    """
    def __init__(self, tile, color: int):
        self.tile = tile
        self.color = color
        self.path = []
        self.unwalkable = {"water", "shallow_water", "snow", "stone"}

        self.state = "wander"
        self.update()
    
    def update(self):
        self.tile.chunk.update_surf(self.tile.x, self.tile.y, self.color)

    def move(self, dx, dy):
        old_chunk = self.tile.chunk
        world_x = max(0, min(self.tile.get_world_x() + dx, self.tile.chunk.world.size_tiles - 1))
        world_y = max(0, min(self.tile.get_world_y() + dy, self.tile.chunk.world.size_tiles - 1))
        
        new_tile = self.tile.chunk.world.get_tile(world_x, world_y)
        if new_tile.material in self.unwalkable:
            return

        self.tile.chunk.update_surf(self.tile.x, self.tile.y, self.tile.color)
        self.tile = new_tile
        if old_chunk != self.tile.chunk:
            old_chunk.animals.remove(self)
            self.tile.chunk.animals.append(self)
        self.update()

    def wander(self, chance=0.05):
        if random.random() < chance:
            self.move(random.randint(-1, 1), random.randint(-1, 1))
    
    def tick(self, delta_time):
        if self.state == "idle":
            return
        elif self.state == "wander":
            self.wander(0.2)

