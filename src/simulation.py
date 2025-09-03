from src.grid import Grid
from src.hero import Hero
from src.bridge import Bridge
from src.gui import SimulationGUI
import time

class Simulation:
    def __init__(self, grid_size=20, turns=100):
        self.grid = Grid(grid_size)
        self.heroes = [
            Hero("Reed", color="navy"),
            Hero("Sue", color="cyan"),
            Hero("Johnny", color="red"),
            Hero("Ben", color="orange"),
        ]
        self.turns = turns

        # Place heroes
        for i, hero in enumerate(self.heroes):
            self.grid.place_entity(hero, i, 0)

        # Place bridges
        self.bridges = [
            Bridge(10, 10),
            Bridge(15, 5),
            Bridge(5, 15),
        ]

        # GUI
        self.gui = SimulationGUI(self.grid, self.heroes, self.bridges)

    def all_bridges_repaired(self):
        return all(b.repaired for b in self.bridges)

    def nearest_damaged_bridge(self, hero):
        """Find the closest damaged bridge for this hero."""
        damaged = [b for b in self.bridges if not b.repaired]
        if not damaged:
            return None
        # Sort by Manhattan distance
        return min(damaged, key=lambda b: abs(b.x - hero.x) + abs(b.y - hero.y))

    def run(self):
        print("Simulation started with Bridges & Smart Heroes.")

        for turn in range(self.turns):
            print(f"\nTurn {turn+1}")

            for hero in self.heroes:
                target = self.nearest_damaged_bridge(hero)

                if target:
                    hero.move_toward(self.grid, target.x, target.y)
                else:
                    hero.move_random(self.grid)  # no bridges left

                # Repair if standing on a bridge
                for bridge in self.bridges:
                    if hero.x == bridge.x and hero.y == bridge.y and not bridge.repaired:
                        bridge.repair()
                        print(f"{hero.name} repaired bridge at ({bridge.x},{bridge.y})!")

                print(hero)

            self.gui.draw()

            # Victory check
            if self.all_bridges_repaired():
                print("\n All bridges repaired! Earth can teleport!")
                break

            time.sleep(0.3)

        print("Simulation finished.")
        self.gui.root.mainloop()
