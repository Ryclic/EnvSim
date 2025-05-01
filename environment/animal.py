class Animal:
    """
    Generic base class for animal, used for implementation of other animals.
    """
    def __init__(self, x: int, y: int, color: int):
        self.x = x
        self.y = y
        self.color = color

    def place_random_tile(self):
        pass

    def get_world_x(self) -> int:
        return self.x
    
    def get_world_y(self) -> int:
        return self.y