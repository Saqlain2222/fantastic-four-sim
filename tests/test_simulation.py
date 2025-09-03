import pytest
from src.simulation import Simulation

def test_simulation_setup():
    sim = Simulation(grid_size=10, turns=5, difficulty="easy")
    assert len(sim.heroes) == 4
    assert len(sim.bridges) == 3
    assert sim.franklin is not None
    assert sim.surfer is not None
    assert sim.galactus is not None

def test_all_bridges_repaired_false_initially():
    sim = Simulation(grid_size=10, turns=5, difficulty="easy")
    assert sim.all_bridges_repaired() is False
