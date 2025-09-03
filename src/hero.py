
import random

class Hero:
    def __init__(self, name, energy=100, color="blue"):
        self.name = name
        self.energy = energy
        self.color = color
        self.x, self.y = None, None

    def __repr__(self):
        return f"{self.name}({self.x},{self.y},E={self.energy})"

    def move(self, grid):
        if self.energy > 0:
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
            self.energy -= 1
            grid.move_entity(self, dx, dy)
