
import random

class Hero:
    def __init__(self, name, energy=100, color="blue"):
        self.name = name
        self.energy = energy
        self.color = color
        self.x, self.y = None, None

    def __repr__(self):
        return f"{self.name}({self.x},{self.y},E={self.energy})"

    def move_toward(self, grid, target_x, target_y):
        """Move one step toward a target position (bridge)."""
        if self.energy <= 0:
            return

        dx, dy = 0, 0

        if target_x > self.x:
            dx = 1
        elif target_x < self.x:
            dx = -1

        if target_y > self.y:
            dy = 1
        elif target_y < self.y:
            dy = -1

        # Move hero
        self.energy -= 1
        grid.move_entity(self, dx, dy)

    def move_random(self, grid):
        """Fallback random movement if no target exists."""
        if self.energy <= 0:
            return
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        self.energy -= 1
        grid.move_entity(self, dx, dy)
