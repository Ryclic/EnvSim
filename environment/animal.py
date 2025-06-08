import random
import pygame
import heapq
from concurrent.futures import ThreadPoolExecutor


class PathNode:
    def __init__(self, tile, g_cost=0, h_cost=0, parent=None):
        self.tile = tile
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def get_distance(self, other):
        return self.get_distance_to_coordinate(
            other.tile.get_world_x(), other.tile.get_world_y()
        )

    def get_distance_to_coordinate(self, x, y):
        dx = abs(x - self.tile.get_world_x())
        dy = abs(y - self.tile.get_world_y())

        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)

    def __lt__(self, other):
        return self.f_cost < other.f_cost or (
            self.f_cost == other.f_cost and self.h_cost < other.h_cost
        )


class Animal:
    """
    Generic base class for animal, used for implementation of other animals.
    """

    count = 0
    pathfinding_executor = ThreadPoolExecutor(max_workers=2)

    def __init__(
        self,
        tile,
        color=pygame.Color(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        ),
        prey={},
        unwalkable={"water", "shallow_water", "snow", "stone"},
        age=random.randint(20, 80)
    ):
        self.tile = tile
        self.color = color
        self.path = []
        self.path_future = None
        self.unwalkable = unwalkable
        self.prey = prey
        self.target = None
        self.removed = False
        self.max_hunger = 100
        self.hunger = self.max_hunger * 0.8
        self.age = age

        self.movement_state = "none"  # "wander", "follow", "none"
        self.goal_state = "none"  # "reproduce", "hunt", "none"
        self.update()

        Animal.count += 1

    def get_distance(self, other):
        dx = abs(other.tile.get_world_x() - self.tile.get_world_x())
        dy = abs(other.tile.get_world_y() - self.tile.get_world_y())

        return max(dx, dy)

    def update(self):
        self.tile.chunk.update_surf(self.tile.x, self.tile.y, self.color)

    def get_path_to(self, world_x, world_y):
        node_lookup = {}
        node_lookup[self.tile] = PathNode(self.tile)

        open_nodes = [node_lookup[self.tile]]
        heapq.heapify(open_nodes)
        closed_tiles = set()

        while len(open_nodes):
            current_node = heapq.heappop(open_nodes)
            del node_lookup[current_node.tile]
            closed_tiles.add(current_node.tile)

            if (
                current_node.tile.get_world_x() == world_x
                and current_node.tile.get_world_y() == world_y
            ):
                path = []
                node = current_node
                while node != None:
                    path.append(node.tile)
                    node = node.parent
                path.pop()
                # for tile in path:
                #    tile.chunk.update_surf(tile.x, tile.y, pygame.Color(255, 255, 0))
                return path

            for neighbor_tile in current_node.tile.get_neighbors():
                if (
                    neighbor_tile.material in self.unwalkable
                    or neighbor_tile in closed_tiles
                ):
                    continue

                new_g_cost = (
                    current_node.g_cost
                    + current_node.get_distance_to_coordinate(
                        neighbor_tile.get_world_x(), neighbor_tile.get_world_y()
                    )
                )
                add_flag = False
                if (
                    neighbor_tile not in node_lookup
                    or new_g_cost < node_lookup[neighbor_tile].g_cost
                ):
                    if neighbor_tile not in node_lookup:
                        add_flag = True
                        node_lookup[neighbor_tile] = PathNode(neighbor_tile)
                        node_lookup[neighbor_tile].h_cost = node_lookup[
                            neighbor_tile
                        ].get_distance_to_coordinate(world_x, world_y)

                    node_lookup[neighbor_tile].g_cost = new_g_cost
                    node_lookup[neighbor_tile].update_f_cost()
                    node_lookup[neighbor_tile].parent = current_node

                    if add_flag:
                        heapq.heappush(open_nodes, node_lookup[neighbor_tile])
        return []

    def move(self, dx, dy):
        old_chunk = self.tile.chunk
        world_x = max(
            0, min(self.tile.get_world_x() + dx, self.tile.chunk.world.size_tiles - 1)
        )
        world_y = max(
            0, min(self.tile.get_world_y() + dy, self.tile.chunk.world.size_tiles - 1)
        )

        new_tile = self.tile.chunk.world.get_tile(world_x, world_y)
        if new_tile.material in self.unwalkable:
            return

        self.tile.chunk.update_surf(self.tile.x, self.tile.y, self.tile.color)
        self.tile = new_tile
        if old_chunk != self.tile.chunk:
            old_chunk.animals.remove(self)
            self.tile.chunk.animals.append(self)
        self.update()

    def remove(self):
        self.tile.chunk.animals.remove(self)
        self.tile.chunk.update_surf(self.tile.x, self.tile.y, self.tile.color)
        self.removed = True
        Animal.count -= 1
        del self

    def move_to(self, x, y):
        self.move(x - self.tile.get_world_x(), y - self.tile.get_world_y())

    def move_to_tile(self, tile):
        self.move_to(tile.get_world_x(), tile.get_world_y())

    def wander(self, chance=0.05):
        if random.random() < chance:
            self.move(random.randint(-1, 1), random.randint(-1, 1))

    def follow(self, chance=0.01):
        if random.random() < chance and len(self.path) > 0:
            self.move_to_tile(self.path.pop())

    def search(self, targets):
        if len(targets) <= 0:
            return None

        nearest = None
        shortest_distance = -1
        neighbor_chunks = self.tile.chunk.get_neighbors()
        for neighbor_chunk in neighbor_chunks:
            for animal in neighbor_chunk.animals:
                if not isinstance(animal, tuple(targets)):
                    continue
                distance = self.get_distance(animal)
                if shortest_distance == -1 or distance < shortest_distance:
                    shortest_distance = distance
                    nearest = animal

        if shortest_distance < 14:
            return nearest

    def update_hunger(self, chance=0.02):
        if self.hunger <= 0:
            self.remove()
            print("Starved")
            return

        if random.random() < chance:
            self.hunger -= 1
    
    def update_lifetime(self, chance=0.01):
        if self.age >= 100:
            self.remove()
            print("Aged")
            return

        if random.random() < chance:
            self.age > 0

    def tick(self, delta_time):
        self.update_hunger()
        self.update_lifetime()

        if self.tile.material in self.unwalkable:
            self.remove()
            return

        if self.target != None and self.target.removed:
            self.target = None

        if self.target is None:
            self.path = []
            self.movement_state = "wander"

        if self.path_future and self.path_future.done():
            self.path = self.path_future.result()
            self.path_future = None

        if self.target != None and self.get_distance(self.target) <= 1:
            if self.goal_state == "hunt":
                self.target.remove()
                self.target = None
                self.hunger += 70
                self.hunger = min(self.hunger, self.max_hunger)
                self.movement_state = "wander"
                self.goal_state = "none"
                print("Hunted")
            elif self.goal_state == "reproduce":
                self.target = None
                self.hunger -= 30
                self.tile.chunk.animals.append(type(self)(self.tile, age=0))
                self.goal_state = "none"
                self.movement_state = "wander"
                print("Reproduced")

        elif len(self.path) > 0:
            self.movement_state = "follow"
        else:
            if self.target is None:
                if self.goal_state == "hunt":
                    self.target = self.search(self.prey)
                elif self.goal_state == "reproduce":
                    self.target = self.search((type(self),)) # Comma because it needs to be tuple
            if self.target != None and self.path_future is None:
                self.path_future = Animal.pathfinding_executor.submit(
                    self.get_path_to,
                    self.target.tile.get_world_x(),
                    self.target.tile.get_world_y(),
                )
            else:
                self.movement_state = "wander"

        if self.movement_state == "none":
            return
        elif self.movement_state == "wander":
            self.wander(0.05)
        elif self.movement_state == "follow":
            self.follow(0.07)


class Fox(Animal):
    count = 0

    def __init__(self, tile, age=random.randint(20, 80)):
        super().__init__(tile, color=pygame.Color(196, 110, 43), prey={Rabbit}, age=age)
        Fox.count += 1

    def remove(self):
        super().remove()
        Fox.count -= 1

    def tick(self, delta_time):
        super().tick(delta_time)
        if self.hunger < 60:
            self.goal_state = "hunt"
        elif  20 < self.age < 60 and self.hunger > 90:
            self.goal_state = "reproduce"
        else:
            self.goal_state = "none"

class Rabbit(Animal):
    count = 0

    def __init__(self, tile, age=random.randint(20, 80)):
        super().__init__(tile, color=pygame.Color(204, 186, 163), age=age)
        Rabbit.count += 1

    def remove(self):
        super().remove()
        Rabbit.count -= 1

    def tick(self, delta_time):
        super().tick(delta_time)
        if self.tile.material == "grass" and random.random() < 0.06 - 0.0008 * Rabbit.count:
            self.hunger += 1
            self.hunger = min(self.hunger, self.max_hunger)

        if self.hunger > 85 and 20 < self.age < 60:
            self.goal_state = "reproduce"
        else:
            self.goal_state = "none"
