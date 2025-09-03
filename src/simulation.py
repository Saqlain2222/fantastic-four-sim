from src.grid import Grid
from src.hero import Hero
import time

class Simulation:
    def __init__(self, grid_size=20, turns=5):
        self.grid = Grid(grid_size)
        self.heroes = [
            Hero("Reed"),
            Hero("Sue"),
            Hero("Johnny"),
            Hero("Ben"),
        ]
        self.turns = turns

        # Place heroes on first row
        for i, hero in enumerate(self.heroes):
            self.grid.place_entity(hero, i, 0)

    def run(self):
        print("Simulation started.")

        for turn in range(self.turns):
            print(f"\nTurn {turn+1}")
            for hero in self.heroes:
                hero.move(self.grid)
                print(hero)
            time.sleep(1)  # pause for readability
