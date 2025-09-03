
class Galactus:
    def __init__(self, x, y, energy=999, color="purple"):
        self.x = x
        self.y = y
        self.energy = energy  # he moves slowly, so energy is huge
        self.color = color
        self.active = False

    def __repr__(self):
        return f"Galactus({self.x},{self.y},Active={self.active})"

    def move_toward(self, grid, target_x, target_y):
        """Moves slowly (every 2 turns) toward Franklin Richards."""
        if not self.active:
            return

        dx, dy = 0, 0
        if target_x > self.x: dx = 1
        elif target_x < self.x: dx = -1
        if target_y > self.y: dy = 1
        elif target_y < self.y: dy = -1

        grid.move_entity(self, dx, dy)

    def destroy(self, grid, bridges, heroes):
        """Destroys anything in his path: bridges or heroes."""
        # Destroy bridges
        for bridge in bridges:
            if self.x == bridge.x and self.y == bridge.y:
                bridge.repaired = False
                print(f"💥 Galactus destroyed bridge at ({bridge.x},{bridge.y})!")

        # Destroy heroes
        for hero in heroes:
            if hero.x == self.x and hero.y == self.y:
                hero.energy = 0
                print(f"💀 Galactus crushed {hero.name}!")
