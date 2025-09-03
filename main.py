from src.simulation import Simulation

def main():
    sim = Simulation(grid_size=20, turns=30)
    sim.run()

if __name__ == "__main__":
    main()
