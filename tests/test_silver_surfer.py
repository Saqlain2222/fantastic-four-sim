import pytest
from src.grid import Grid
from src.silver_surfer import SilverSurfer
from src.bridge import Bridge
from src.hero import Hero

def test_silver_surfer_moves_and_sabotages():
    grid = Grid(10)
    surfer = SilverSurfer(0, 0)
    bridge = Bridge(2, 2)
    bridge.repaired = True  # assume it was repaired

    # Move surfer toward the repaired bridge
    surfer.move_toward(grid, bridge.x, bridge.y, heroes=[])
    assert surfer.energy < 100  # energy reduced
    assert (surfer.x, surfer.y) != (0, 0)  # moved

    # Place surfer directly on bridge → sabotage
    surfer.x, surfer.y = bridge.x, bridge.y
    surfer.sabotage([bridge])
    assert bridge.repaired is False

def test_silver_surfer_withdraws():
    surfer = SilverSurfer(0, 0, energy=15)
    assert surfer.should_withdraw() is True
