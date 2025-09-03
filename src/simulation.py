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
        self.difficulty = difficulty

        # Stats tracking
        self.turns_survived = 0
        self.bridges_repaired_count = 0
        self.bridges_sabotaged_count = 0
        self.bridges_destroyed_count = 0
        self.heroes_collapsed_count = 0
        self.heroes_destroyed_count = 0

        # Place heroes
        for i, hero in enumerate(self.heroes):
            self.grid.place_entity(hero, i, 0)

        # Place bridges randomly
        self.bridges = []
        for _ in range(3):
            bx, by = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            self.bridges.append(Bridge(bx, by))
        print(" Bridges placed at:", [(b.x, b.y) for b in self.bridges])

        # Place Franklin Richards randomly
        self.franklin = Franklin(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        print(f" Franklin placed at: ({self.franklin.x},{self.franklin.y})")

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
            self.turns_survived = turn + 1

            # -----------------------------
            # HERO ACTIONS (difficulty-based)
            # -----------------------------
            for hero in self.heroes:
                if not getattr(hero, "active", True):  # skip inactive heroes
                    continue

                if hero.energy <= 0:
                    hero.active = False
                    self.heroes_collapsed_count += 1
                    print(f" {hero.name} has collapsed from exhaustion!")
                    continue

                if self.difficulty == "easy":
                    target = self.nearest_damaged_bridge(hero)
                    if target:
                        hero.move_toward(self.grid, target.x, target.y)
                    else:
                        hero.move_random(self.grid)

                elif self.difficulty == "normal":
                    if random.random() < 0.8:
                        target = self.nearest_damaged_bridge(hero)
                        if target:
                            hero.move_toward(self.grid, target.x, target.y)
                    else:
                        hero.move_random(self.grid)

                elif self.difficulty == "hard":
                    hero.move_random(self.grid)

                # Repair if standing on a bridge
                for bridge in self.bridges:
                    if hero.x == bridge.x and hero.y == bridge.y and not bridge.repaired:
                        bridge.repair()
                        self.bridges_repaired_count += 1
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
                sabotaged = self.surfer.sabotage(self.bridges)
                if sabotaged:
                    self.bridges_sabotaged_count += 1

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
                    if turn % 3 == 0:
                        self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)
                elif self.difficulty == "normal":
                    if turn % 2 == 0:
                        self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)
                elif self.difficulty == "hard":
                    self.galactus.move_toward(self.grid, self.franklin.x, self.franklin.y)

                # Destruction log with counts
                b_destroyed, h_destroyed = self.galactus.destroy(self.grid, self.bridges, self.heroes)
                self.bridges_destroyed_count += b_destroyed
                self.heroes_destroyed_count += h_destroyed

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

        # -----------------------------
        # GAME SUMMARY
        # -----------------------------
        print("\n===== GAME SUMMARY =====")
        print(f"Turns survived: {self.turns_survived}")
        print(f"Bridges repaired: {self.bridges_repaired_count}")
        print(f"Bridges sabotaged (Silver Surfer): {self.bridges_sabotaged_count}")
        print(f"Bridges destroyed (Galactus): {self.bridges_destroyed_count}")
        print(f"Heroes collapsed (exhaustion): {self.heroes_collapsed_count}")
        print(f"Heroes destroyed (Galactus): {self.heroes_destroyed_count}")
        alive_heroes = [h.name for h in self.heroes if getattr(h, "active", True)]
        print(f"Heroes alive: {alive_heroes if alive_heroes else 'None'}")
        if self.all_bridges_repaired():
            print("Final outcome: Victory ")
        else:
            print("Final outcome: Defeat ")
        print("========================\n")

        print("Simulation finished.")
        self.gui.root.mainloop()
