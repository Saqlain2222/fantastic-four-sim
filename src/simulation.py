from src.grid import Grid
from src.hero import Hero
from src.bridge import Bridge
from src.gui import SimulationGUI
from src.silver_surfer import SilverSurfer
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

        # Add Silver Surfer
        self.surfer = SilverSurfer(0, grid_size - 1)

        # GUI
        self.gui = SimulationGUI(self.grid, self.heroes, self.bridges, self.surfer)

    def all_bridges_repaired(self):
        return all(b.repaired for b in self.bridges)

    def nearest_damaged_bridge(self, hero):
        damaged = [b for b in self.bridges if not b.repaired]
        if not damaged:
            return None
        return min(damaged, key=lambda b: abs(b.x - hero.x) + abs(b.y - hero.y))

    def run(self):
        print("Simulation started with Smart Silver Surfer.")

        for turn in range(self.turns):
            print(f"\nTurn {turn+1}")

            # Heroes repair bridges
            for hero in self.heroes:
                target = self.nearest_damaged_bridge(hero)
                if target:
                    hero.move_toward(self.grid, target.x, target.y)
                else:
                    hero.move_random(self.grid)

                for bridge in self.bridges:
                    if hero.x == bridge.x and hero.y == bridge.y and not bridge.repaired:
                        bridge.repair()
                        print(f"{hero.name} repaired bridge at ({bridge.x},{bridge.y})!")

                print(hero)

            # Silver Surfer appears after turn 10
            if turn == 10:
                self.surfer.active = True
                print("⚡ Silver Surfer has appeared!")

            # Surfer AI: move toward repaired bridges + sabotage
            if self.surfer.active:
                target_bridge = self.surfer.nearest_repaired_bridge(self.bridges)
                if target_bridge:
                    self.surfer.move_toward(self.grid, target_bridge.x, target_bridge.y, self.heroes)
                else:
                    self.surfer.move_toward(self.grid, self.x, self.y, self.heroes)  # roam if no repaired bridge

                self.surfer.sabotage(self.bridges)

                if self.surfer.should_withdraw():
                    print("⚡ Silver Surfer withdrew due to low energy!")
                    self.surfer.active = False

            # Draw updated grid
            self.gui.draw()

            # Victory condition
            if self.all_bridges_repaired():
                print("\n All bridges repaired! Earth can teleport!")
                break

            time.sleep(0.3)

        print("Simulation finished.")
        self.gui.root.mainloop()
