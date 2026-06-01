"""Test Module for Rocket Calculations"""
# filename: tests\test_rockets.py

import pytest
from components import *
from exceptions import InvalidAmountError, LimitExceededError, NoModulesError
from fuel_system import MAX_OXI_TANKS, MAX_FUEL_TANKS
from rocket import Rocket
from component_bases import *

# ============================================================
# CONSTANTS / HELPERS
# ============================================================

def assert_range(rocket: Rocket, expected: int):
    actual = rocket.calculate_range()
    assert expected <= actual
    rocket.set_fuel(rocket.fuel_amount - 1)
    if rocket.fuel_system.oxylite_amount > 0:
        rocket.set_oxylite(rocket.fuel_system.oxylite_amount - 1)
    if rocket.fuel_system.lox_amount > 0:
        rocket.set_lox(rocket.fuel_system.lox_amount - 1)
    assert rocket.calculate_range() < expected

def rocket_factory(
    engine: type[Engine],
    fuel_tanks: int,
    fuel: int,
    oxidizer_type: OxidizerType | None = None,
    oxidizer_tanks: int = 0,
    booster: bool = False,
    research: int = 0,
    cargo: int = 0,
):
    rocket = Rocket()
    rocket.engine_system.set_engine(engine)

    for _ in range(fuel_tanks):
        rocket.fuel_system.add_fuel_tank()

    rocket.set_fuel(fuel)

    if oxidizer_type:
        if oxidizer_type == OxidizerType.OXYLITE:
            for _ in range(oxidizer_tanks):
                rocket.fuel_system.add_oxylite_tank()
            rocket.set_oxylite(fuel)

        elif oxidizer_type == OxidizerType.LOX:
            for _ in range(oxidizer_tanks):
                rocket.fuel_system.add_lox_tank()
            rocket.set_lox(fuel)

    if booster:
        rocket.engine_system.add_thruster()

    for _ in range(research):
        rocket.modules.add_module(ResearchModule)

    for _ in range(cargo):
        rocket.modules.add_module(CargoBay)

    return rocket


# ============================================================
# BASIC TESTS
# ============================================================

def test_rocket_exists():
    rocket = Rocket()
    assert rocket.total_mass == 200


def test_empty_rocket_range():
    rocket = Rocket()
    assert rocket.calculate_range() == 0


# ============================================================
# STEAM ENGINE
# ============================================================

@pytest.mark.parametrize("fuel,dist", [
    (695, 10000),
])
def test_steam_basic(fuel, dist):
    rocket = rocket_factory(SteamEngine, 0, fuel, research=5)
    assert_range(rocket, dist)


@pytest.mark.parametrize("fuel,dist", [
    (163, 10000),
    (809, 20000),
])
def test_steam_booster(fuel, dist):
    rocket = rocket_factory(SteamEngine, 0, fuel, booster=True, research=5)
    assert_range(rocket, dist)


def test_steam_cargo():
    rocket = rocket_factory(SteamEngine, 0, 528, booster=True, cargo=1)
    assert_range(rocket, 10000)


# ============================================================
# PETROLEUM + SOLID OXIDIZER
# ============================================================

@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 306, 10000),
    (1, 569, 20000),
    (1, 832, 30000),
    (2, 1098, 40000),
    (2, 1394, 50000),
    (2, 1723, 60000),
    (3, 2124, 70000),
    (3, 2592, 80000),
])
def test_petrol_solid_research(tanks, fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine, tanks, fuel,
        OxidizerType.OXYLITE, 1, research=5
    )
    assert_range(rocket, dist)


@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 16, 10000),
    (1, 279, 20000),
    (1, 543, 30000),
    (1, 820, 40000),
    (2, 1155, 50000),
    (2, 1514, 60000),
    (3, 1987, 70000),
    (3, 2656, 80000),
])
def test_petrol_solid_booster(tanks, fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine, tanks, fuel,
        OxidizerType.OXYLITE, 1, booster=True, research=5
    )
    assert_range(rocket, dist)


# ============================================================
# PETROLEUM + LIQUID OXIDIZER
# ============================================================

@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 227, 10000),
    (1, 422, 20000),
    (1, 618, 30000),
    (1, 813, 40000),
    (2, 1010, 50000),
    (2, 1211, 60000),
    (2, 1430, 70000),
    (2, 1659, 80000),
    (3, 1916, 90000),
    (3, 2177, 100000),
    (3, 2462, 110000),
    (4, 2879, 120000),
    (4, 3329, 130000),
])
def test_petrol_liquid_research(tanks, fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine, tanks, fuel,
        OxidizerType.LOX,
        2 if tanks == 4 else 1,
        research=5
    )
    assert_range(rocket, dist)


@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 12, 10000),
    (1, 208, 20000),
    (1, 403, 30000),
    (1, 598, 40000),
    (1, 802, 50000),
    (2, 1034, 60000),
    (2, 1268, 70000),
    (2, 1515, 80000),
    (2, 1780, 90000),
    (3, 2105, 100000),
    (3, 2451, 110000),
])
def test_petrol_liquid_booster(tanks, fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine, tanks, fuel,
        OxidizerType.LOX, 1,
        booster=True, research=5
    )
    assert_range(rocket, dist)


# ============================================================
# HYDROGEN (RESEARCH)
# ============================================================

@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 206, 10000),
    (1, 378, 20000),
    (1, 550, 30000),
    (1, 723, 40000),
    (1, 895, 50000),
    (2, 1075, 60000),
    (2, 1266, 70000),
    (2, 1463, 80000),
    (2, 1667, 90000),
])
def test_hydrogen_solid_research(tanks, fuel, dist):
    rocket = rocket_factory(
        HydrogenEngine, tanks, fuel,
        OxidizerType.OXYLITE, 1, research=5
    )
    assert_range(rocket, dist)


@pytest.mark.parametrize("tanks,fuel,dist", [
    (1, 153, 10000),
    (1, 282, 20000),
    (1, 411, 30000),
    (1, 539, 40000),
    (1, 668, 50000),
    (1, 796, 60000),
    (2, 926, 70000),
    (2, 1058, 80000),
    (2, 1195, 90000),
    (2, 1335, 100000),
])
def test_hydrogen_liquid_research(tanks, fuel, dist):
    rocket = rocket_factory(
        HydrogenEngine, tanks, fuel,
        OxidizerType.LOX, 1, research=5
    )
    assert_range(rocket, dist)


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
        PetroleumEngine, 1, fuel,
        OxidizerType.OXYLITE, 1, cargo=1
    )
    assert_range(rocket, dist)


@pytest.mark.parametrize("fuel,dist", [
    (247, 10000),
    (442, 20000),
    (637, 30000),
    (846, 40000),
])
def test_petrol_liquid_cargo(fuel, dist):
    rocket = rocket_factory(
        PetroleumEngine, 1, fuel,
        OxidizerType.LOX, 1, cargo=1
    )
    assert_range(rocket, dist)


# ============================================================
# EDGE / FAILURE TESTS (IMPORTANT)
# ============================================================

def test_missing_oxidizer_results_in_zero_range():
    rocket = rocket_factory(
        PetroleumEngine, 1, 500,
        oxidizer_type=None, research=5
    )
    assert rocket.calculate_range() == 0


def test_zero_fuel():
    rocket = rocket_factory(
        PetroleumEngine, 1, 0,
        OxidizerType.OXYLITE, 1, research=5
    )
    assert rocket.calculate_range() == 0


def test_underfuel_boundary():
    rocket = rocket_factory(
        SteamEngine, 0, 694, research=5
    )
    assert rocket.calculate_range() < 10000

def test_adding_too_many_fuel_tanks():
    rocket = rocket_factory(SteamEngine, 0,0)
    with pytest.raises(LimitExceededError):
        for _ in range(MAX_FUEL_TANKS + 1):
            rocket.fuel_system.add_fuel_tank()

def test_adding_too_many_oxylite_tanks():
    rocket = rocket_factory(PetroleumEngine, 0,0)
    with pytest.raises(LimitExceededError):
        for _ in range(MAX_OXI_TANKS + 1):
            rocket.fuel_system.add_oxylite_tank()

def test_adding_too_many_lox_tanks():
    rocket = rocket_factory(PetroleumEngine, 0,0)
    with pytest.raises(LimitExceededError):
        for _ in range(MAX_OXI_TANKS + 1):
            rocket.fuel_system.add_lox_tank()

def test_removing_fuel_tanks_from_rocket_with_none():
    rocket = rocket_factory(SteamEngine, 0,0)
    rocket2 = rocket_factory(PetroleumEngine, 0,0)
    with pytest.raises(NoModulesError):
        rocket.fuel_system.remove_fuel_tank()
    with pytest.raises(NoModulesError):
        rocket2.fuel_system.remove_fuel_tank()
    
def test_removing_oxylite_tanks_from_rocket_with_none():
    rocket = rocket_factory(SteamEngine, 0,0)
    rocket2 = rocket_factory(PetroleumEngine, 0,0)
    with pytest.raises(NoModulesError):
        rocket.fuel_system.remove_oxylite_tank()
    with pytest.raises(NoModulesError):
        rocket2.fuel_system.remove_oxylite_tank()

def test_removing_lox_tanks_from_rocket_with_none():
    rocket = rocket_factory(SteamEngine, 0,0)
    rocket2 = rocket_factory(PetroleumEngine, 0,0)
    with pytest.raises(NoModulesError):
        rocket.fuel_system.remove_lox_tank()
    with pytest.raises(NoModulesError):
        rocket2.fuel_system.remove_lox_tank()

# ============================================================
# INVALID VALUES
# ============================================================


def test_string_for_amount_rejected():
    rocket = Rocket()
    rocket.fuel_system.add_fuel_tank()
    rocket.fuel_system.add_lox_tank()
    rocket.fuel_system.add_oxylite_tank()
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox("b") # type: ignore
    rocket.engine_system.set_engine(SteamEngine)
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox("b") # type: ignore
    rocket.engine_system.set_engine(PetroleumEngine)
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite("b") # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox("b") # type: ignore
    

def test_negative_for_amount_rejected():
    rocket = Rocket()
    rocket.fuel_system.add_fuel_tank()
    rocket.fuel_system.add_lox_tank()
    rocket.fuel_system.add_oxylite_tank()
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel(-10) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite(-11) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox(-12) # type: ignore
    rocket.engine_system.set_engine(SteamEngine)
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel(-20) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite(-21) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox(-22) # type: ignore
    rocket.engine_system.set_engine(PetroleumEngine)
    with pytest.raises(InvalidAmountError):
        rocket.set_fuel(-31) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_oxylite(-32) # type: ignore
    with pytest.raises(InvalidAmountError):
        rocket.set_lox(-33) # type: ignore