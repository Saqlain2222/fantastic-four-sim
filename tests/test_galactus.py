import pytest
from src.grid import Grid
from src.galactus import Galactus
from src.hero import Hero
from src.bridge import Bridge

def test_galactus_destroys_bridge():
    grid = Grid(10)
    galactus = Galactus(5, 5)
    galactus.active = True
    bridge = Bridge(5, 5)
    bridge.repaired = True

    galactus.destroy(grid, [bridge], [])
    assert bridge.repaired is False

def test_galactus_destroys_hero():
    grid = Grid(10)
    galactus = Galactus(3, 3)
    galactus.active = True
    hero = Hero("Ben")
    grid.place_entity(hero, 3, 3)

    galactus.destroy(grid, [], [hero])
    assert hero.energy == 0

def test_galactus_moves_toward():
    grid = Grid(10)
    galactus = Galactus(0, 0)
    galactus.active = True

    galactus.move_toward(grid, 5, 5)
    assert (galactus.x, galactus.y) != (0, 0)  # moved closer
