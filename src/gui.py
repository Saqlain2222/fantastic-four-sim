import tkinter as tk

CELL_SIZE = 25

class SimulationGUI:
    def __init__(self, grid, heroes, bridges, surfer=None):
        self.grid = grid
        self.heroes = heroes
        self.bridges = bridges
        self.surfer = surfer

        self.root = tk.Tk()
        self.root.title("Fantastic Four Simulation")

        self.canvas = tk.Canvas(
            self.root,
            width=self.grid.size * CELL_SIZE,
            height=self.grid.size * CELL_SIZE
        )
        self.canvas.pack()

    def draw(self):
        self.canvas.delete("all")

        for y in range(self.grid.size):
            for x in range(self.grid.size):
                color = "white"

                # Bridges
                for bridge in self.bridges:
                    if bridge.x == x and bridge.y == y:
                        color = "yellow" if not bridge.repaired else "green"

                # Silver Surfer
                if self.surfer and self.surfer.active:
                    if self.surfer.x == x and self.surfer.y == y:
                        color = self.surfer.color

                # Heroes
                entity = self.grid.cells[y][x]
                if entity is not None and hasattr(entity, "color"):
                    color = entity.color

                self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill=color, outline="black"
                )

        self.root.update_idletasks()
