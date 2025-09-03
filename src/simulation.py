from src.grid import Grid
from src.hero import Hero
from src.bridge import Bridge
from src.gui import SimulationGUI
from src.silver_surfer import SilverSurfer
from src.galactus import Galactus
from src.franklin import Franklin
import time, random

class Simulation:
    def __init__(self, grid_size=20, turns=150, difficulty="normal"):
        self.grid = Grid(grid_size)
        self.heroes = [
            Hero("Reed", color="navy"),
            Hero("Sue", color="cyan"),
            Hero("Johnny", color="red"),
            Hero("Ben", color="orange"),
        ]
        self.turns = turns
        self.difficulty = difficulty  # <-- new difficulty setting

        # Place heroes
        for i, hero in enumerate(self.heroes):
            self.grid.place_entity(hero, i, 0)

        # Place bridges
        self.bridges = [
            Bridge(10, 10),
            Bridge(15, 5),
            Bridge(5, 15),
        ]

        # Add Franklin Richards (target to protect)
        self.franklin = Franklin(grid_size // 2, grid_size // 2)

        # Add Silver Surfer
        self.surfer = SilverSurfer(0, grid_size - 1)

        # Add Galactus (appears later)
        self.galactus = Galactus(grid_size - 1, 0)

        # GUI
        self.gui = SimulationGUI(
            self.grid, self.heroes, self.bridges,
            self.surfer, self.galactus, self.franklin
        )

    def all_bridges_repaired(self):
        return all(b.repaired for b in self.bridges)

    def nearest_damaged_bridge(self, hero):
        damaged = [b for b in self.bridges if not b.repaired]
        if not damaged:
            return None
        return min(damaged, key=lambda b: abs(b.x - hero.x) + abs(b.y - hero.y))

    def run(self):
        print(f"Simulation started with Galactus, Franklin & Difficulty = {self.difficulty}")

        for turn in range(self.turns):
            print(f"\nTurn {turn+1}")

            # -----------------------------
            # HERO ACTIONS (difficulty-based)
            # -----------------------------
            for hero in self.heroes:
                if hero.energy > 0:
                    if self.difficulty == "easy":
                        # Always repair bridges
                        target = self.nearest_damaged_bridge(hero)
                        if target:
                            hero.move_toward(self.grid, target.x, target.y)
                        else:
                            hero.move_random(self.grid)

                    elif self.difficulty == "normal":
                        # 80% chance smart, 20% chance wander
                        if random.random() < 0.8:
                            target = self.nearest_damaged_bridge(hero)
                            if target:
                                hero.move_toward(self.grid, target.x, target.y)
                        else:
                            hero.move_random(self.grid)

                    elif self.difficulty == "hard":
                        # Dumb heroes wander aimlessly
                        hero.move_random(self.grid)

                    # Repair if standing on a bridge
                    for bridge in self.bridges:
                        if hero.x == bridge.x and hero.y == bridge.y and not bridge.repaired:
                            bridge.repair()
                            print(f"{hero.name} repaired bridge at ({bridge.x},{bridge.y})!")

                    print(hero)

            # -----------------------------
            # SILVER SURFER
            # -----------------------------
            if turn == 10:
                self.surfer.active = True
                print(" Silver Surfer has appeared!")

            if self.surfer.active:
                target_bridge = self.surfer.nearest_repaired_bridge(self.bridges)
                if target_bridge:
                    self.surfer.move_toward(self.grid, target_bridge.x, target_bridge.y, self.heroes)
                self.surfer.sabotage(self.bridges)

                if self.surfer.should_withdraw():
                    print(" Silver Surfer withdrew due to low energy!")
                    self.surfer.active = False

            # -----------------------------
            # GALACTUS
            # -----------------------------
            if turn == 20:
                self.galactus.active = True
                print(" Galactus has arrived!")

            if self.galactus.active:
                if self.difficulty == "easy":
                    # very slow Galactus (every 3 turns)
                    if turn % 3 == 0:
                        self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)

                elif self.difficulty == "normal":
                    # medium speed (every 2 turns)
                    if turn % 2 == 0:
                        self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)

                elif self.difficulty == "hard":
                    # fast Galactus (every turn)
                    self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)

                self.galactus.destroy(self.grid, self.bridges, self.heroes)

                # Check loss condition
                if self.galactus.x == self.franklin.x and self.galactus.y == self.franklin.y:
                    print(" Galactus has reached Franklin Richards! Earth is lost!")
                    break

            # -----------------------------
            # GUI + Victory check
            # -----------------------------
            self.gui.draw()

            if self.all_bridges_repaired():
                print("\n All bridges repaired! Earth can teleport and Galactus is defeated!")
                break

            time.sleep(0.3)

        print("Simulation finished.")
        self.gui.root.mainloop()
