"""Test Module for Rocket Calculations"""
# filename: tests\test_rocket_configurator.py

import pytest
from rocket import Rocket
from component_bases import *
from components import *
from rocket_configurator import configure_rocket_for_range


# ============================================================
# CONSTANTS / HELPERS
# ============================================================

def assert_fuel(rocket: Rocket, fuel: int, distance: int, oxidizer_type: OxidizerType|None = None):
    rocket = configure_rocket_for_range(rocket, distance, oxidizer_type)
    assert distance <= rocket.calculate_range()
    assert rocket.fuel_amount == fuel

def rocket_factory(
    engine: type[Engine],
    booster: bool = False,
    research: int = 0,
    cargo: int = 0,
):
    rocket = Rocket()
    rocket.engine_system.set_engine(engine)

    if booster:
        rocket.engine_system.add_thruster(Thruster)

    for _ in range(research):
        rocket.modules.add_module(ResearchModule)

    for _ in range(cargo):
        rocket.modules.add_module(CargoBay)

    return rocket


# ============================================================
# STEAM ENGINE
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (695, 10000),
])
def test_steam_basic(fuel, dist):
    rocket = rocket_factory(SteamEngine, research=5)
    assert_fuel(rocket, fuel, dist)


@pytest.mark.parametrize("fuel,dist", [
    (163, 10000),
    (809, 20000),
])
def test_steam_booster(fuel, dist):
    rocket = rocket_factory(SteamEngine, booster=True, research=5)
    assert_fuel(rocket, fuel, dist)


def test_steam_cargo():
    rocket = rocket_factory(SteamEngine, booster=True, cargo=1)
    assert_fuel(rocket, 528, 10000)


# ============================================================
# PETROLEUM + SOLID OXIDIZER
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (306, 10000),
    (569, 20000),
    (832, 30000),
    (1098, 40000),
    (1394, 50000),
    (1723, 60000),
    (2124, 70000),
    (2592, 80000),
])
def test_petrol_solid_research(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        research=5
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.OXYLITE)


@pytest.mark.parametrize("fuel,dist", [
    (16, 10000),
    (279, 20000),
    (543, 30000),
    (820, 40000),
    (1155, 50000),
    (1514, 60000),
    (1987, 70000),
    (2656, 80000),
])
def test_petrol_solid_booster(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        booster=True, research=5
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.OXYLITE)


# ============================================================
# PETROLEUM + LIQUID OXIDIZER
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (227, 10000),
    (422, 20000),
    (618, 30000),
    (813, 40000),
    (1010, 50000),
    (1211, 60000),
    (1430, 70000),
    (1659, 80000),
    (1916, 90000),
    (2177, 100000),
    (2462, 110000),
    (2879, 120000),
    (3329, 130000),
])
def test_petrol_liquid_research(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        research=5
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.LOX)


@pytest.mark.parametrize("fuel,dist", [
    (12, 10000),
    (208, 20000),
    (403, 30000),
    (598, 40000),
    (802, 50000),
    (1034, 60000),
    (1268, 70000),
    (1515, 80000),
    (1780, 90000),
    (2105, 100000),
    (2451, 110000),
])
def test_petrol_liquid_booster(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        booster=True, research=5
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.LOX)


# ============================================================
# HYDROGEN (RESEARCH)
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (206, 10000),
    (378, 20000),
    (550, 30000),
    (723, 40000),
    (895, 50000),
    (1075, 60000),
    (1266, 70000),
    (1463, 80000),
    (1667, 90000),
])
def test_hydrogen_solid_research(fuel, dist):
    rocket = rocket_factory(
        HydrogenEngine, research=5
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.OXYLITE)


@pytest.mark.parametrize("fuel,dist", [
    (153, 10000),
    (282, 20000),
    (411, 30000),
    (539, 40000),
    (668, 50000),
    (796, 60000),
    (926, 70000),
    (1058, 80000),
    (1195, 90000),
    (1335, 100000),
])
def test_hydrogen_liquid_research(fuel, dist):
    rocket = rocket_factory(HydrogenEngine, research=5)
    assert_fuel(rocket, fuel, dist, OxidizerType.LOX)


# ============================================================
# CARGO VARIANTS
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (332, 10000),
    (595, 20000),
    (882, 30000),
])
def test_petrol_solid_cargo(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        cargo=1
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.OXYLITE)


@pytest.mark.parametrize("fuel,dist", [
    (247, 10000),
    (442, 20000),
    (637, 30000),
    (846, 40000),
])
def test_petrol_liquid_cargo(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine,
        cargo=1
    )
    assert_fuel(rocket, fuel, dist, OxidizerType.LOX)