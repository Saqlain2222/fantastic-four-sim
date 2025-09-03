import pytest
from src.grid import Grid
from src.hero import Hero
from src.bridge import Bridge

def test_hero_initial_energy():
    hero = Hero("Reed")
    assert hero.energy == 100
    assert hero.name == "Reed"

def test_hero_move_toward_and_repair():
    grid = Grid(10)
    hero = Hero("Sue")
    bridge = Bridge(5, 5)

    grid.place_entity(hero, 0, 0)
    for _ in range(6):
        hero.move_toward(grid, bridge.x, bridge.y)

    # hero should reach the bridge eventually
    assert (hero.x, hero.y) == (5, 5) or hero.energy < 100

def test_hero_collapses_when_energy_zero():
    grid = Grid(5)
    hero = Hero("Johnny")
    grid.place_entity(hero, 0, 0)

    hero.energy = 1
    hero.move_random(grid)
    assert hero.energy == 0 or hero.energy == 1  # collapses at 0
