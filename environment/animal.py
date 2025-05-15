import random
import heapq

class PathNode():
    def __init__(self, tile, g_cost=0, h_cost=0, parent=None):
        self.tile = tile
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent
    
    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost
    
    def get_distance(self, other):
        return get_distance_to_coordinate(self, self.tile.get_world_x(), self.tile.get_world_y()):
    
    def get_distance_to_coordinate(self, x, y):
        dx = x - self.tile.get_world_x()
        dy = y - self.tile.get_world.y()

        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)

    def __lt__(self, other):
        return self.f_cost < other.f_cost or (self.f_cost == other.f_cost and self.h_cost < other.h_cost)

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

    def get_path_to(self, world_x, world_y):
        node_lookup = {}
        node_lookup[self.tile] = PathNode(self.tile)

        open_nodes = [node_lookup[self.tile]]
        heapq.heapify(open_tiles)
        closed_tiles = set()

        while len(open_nodes):
            current_node = heapq.heappop(open_nodes)
            del node_lookup[current_node.tile] 
            closed_tiles.add(current_node.tile)

            if current_node.tile.get_world_x() == world_x and current_node.tile.get_world_y() == world_y:
                return

            for neighbor_tile in current_node.tile.get_neighbors():
                if neighbor_tile.material in self.unwalkable or neighbor_tile in closed_tiles:
                    continue
                
                new_g_cost = current_node.g_cost + current_node.get_distance_to_coordinate(neighbor_tile.get_world_x(), neighbor_tile.get_world_y())
                if neighbor_tile not in node_lookup or new_g_cost  < node_lookup[neighbor_tile].g_cost:
                    if (neighbor_tile not in node_lookup):
                        node_lookup[neighbor_tile] = PathNode(neighbor_tile)
                    
                    node_lookup[neighbor_tile].g_cost = new_g_cost
                    node_lookup[neighbor_tile].h_cost = node_lookup[neighbor_tile].get_distance_to_coordinate(world_x, world_y)
                    node_lookup[neighbor_tile].update_f_cost()
                    node_lookup[neighbor_tile].parent = current_node

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

