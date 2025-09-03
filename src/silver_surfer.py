import random

class SilverSurfer:
    def __init__(self, x, y, energy=100, color="grey"):
        self.x = x
        self.y = y
        self.energy = energy
        self.color = color
        self.active = False

    def __repr__(self):
        return f"SilverSurfer({self.x},{self.y},E={self.energy},Active={self.active})"

    def nearest_repaired_bridge(self, bridges):
        """Find the closest repaired bridge to sabotage."""
        repaired = [b for b in bridges if b.repaired]
        if not repaired:
            return None
        return min(repaired, key=lambda b: abs(b.x - self.x) + abs(b.y - self.y))

    def move_toward(self, grid, target_x, target_y, heroes):
        """Move one step toward a repaired bridge, avoiding heroes."""
        if self.energy <= 0:
            return

        dx, dy = 0, 0
        if target_x > self.x: dx = 1
        elif target_x < self.x: dx = -1
        if target_y > self.y: dy = 1
        elif target_y < self.y: dy = -1

        # Check if the new cell has a hero → avoid combat
        new_x, new_y = grid.wrap_position(self.x + dx, self.y + dy)
        if any(hero.x == new_x and hero.y == new_y for hero in heroes):
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])  # fallback random move

        self.energy -= 1
        grid.move_entity(self, dx, dy)

    def sabotage(self, bridges):
        """
        Turn a repaired bridge back into damaged.
        Returns True if sabotage happened, otherwise False.
        """
        for bridge in bridges:
            if self.x == bridge.x and self.y == bridge.y and bridge.repaired:
                bridge.repaired = False
                print(f"⚡ Silver Surfer sabotaged bridge at ({bridge.x},{bridge.y})!")
                return True
        return False

    def should_withdraw(self):
        """Withdraw when energy < 20%."""
        return self.energy < 20
