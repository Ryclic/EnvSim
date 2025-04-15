class Animal:
    """
    Generic base class for animal, used for implementation of other animals.
    """
    def __init__(self, x: int = None, y: int = None):
        self.x = x
        self.y = y
        if self.x or self.y == None:
            self.place_random_tile(self)
        pass

    def place_random_tile(self):
        pass

    def get_world_x(self) -> int:
        return self.x
    
    def get_world_y(self) -> int:
        return self.y