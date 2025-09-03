# src/simulation.py
class Simulation:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size

    def run(self):
        print(f"Simulation running on a {self.grid_size}x{self.grid_size} grid...")
