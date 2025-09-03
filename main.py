from src.simulation import Simulation

def main():
    # Choose difficulty: "easy", "normal", "hard"
    sim = Simulation(grid_size=20, turns=150, difficulty="hard")
    sim.run()

if __name__ == "__main__":
    main()
