import pytest
from src.grid import Grid
from src.hero import Hero

def test_wrap_position():
    grid = Grid(20)
    assert grid.wrap_position(-1, -1) == (19, 19)
    assert grid.wrap_position(20, 20) == (0, 0)

def test_place_and_move_entity():
    grid = Grid(10)
    hero = Hero("Reed")
    grid.place_entity(hero, 5, 5)

    assert hero.x == 5 and hero.y == 5
    assert (5, 5) in grid.entities

    grid.move_entity(hero, 1, 0)
    assert (6, 5) in grid.entities
    assert hero.x == 6
