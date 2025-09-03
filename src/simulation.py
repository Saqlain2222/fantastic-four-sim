
from src.grid import Grid
from src.hero import Hero
from src.gui import SimulationGUI
import time

class Simulation:
    def __init__(self, grid_size=20, turns=20):
        self.grid = Grid(grid_size)
        self.heroes = [
            Hero("Reed", color="navy"),     # Dark Blue
            Hero("Sue", color="cyan"),      # Light Blue / Cyan
            Hero("Johnny", color="red"),    # Red
            Hero("Ben", color="orange"),    # Orange
        ]
        self.turns = turns

        # Place heroes on first row
        for i, hero in enumerate(self.heroes):
            self.grid.place_entity(hero, i, 0)

        # Setup GUI
        self.gui = SimulationGUI(self.grid, self.heroes)

    def run(self):
        print("Simulation started (GUI mode).")
        for turn in range(self.turns):
            print(f"\nTurn {turn+1}")
            for hero in self.heroes:
                hero.move(self.grid)
                print(hero)

            self.gui.draw()
            time.sleep(0.5)

        print("Simulation finished.")
        self.gui.root.mainloop()
