"""Test Module for Rocket Modules"""
# filename: tests\test_components.py

from components import *

#Base Classes / Scaffolding Tests:
def test_command_capsule():
    command = CommandCapsule()
    assert command.MASS == 200
    assert command.ROLE.value == "Command Capsule"

def test_biodiesel_engine():
    engine = BiodieselEngine()
    assert engine.MASS == 200
    assert engine.ROLE.value == "Engine"
    assert engine.ENGINE_TYPE.value == "Biodiesel"

def test_petrol_engine():
    engine = PetroleumEngine()
    assert engine.MASS == 200
    assert engine.ROLE.value == "Engine"
    assert engine.ENGINE_TYPE.value == "Petrol"

def test_hydrogen_engine():
    engine = HydrogenEngine()
    assert engine.MASS == 500
    assert engine.ROLE.value == "Engine"
    assert engine.ENGINE_TYPE.value == "Liquid Hydrogen"

def test_steam_engine():
    engine = SteamEngine()
    assert engine.MASS == 2000
    assert engine.ROLE.value == "Engine"
    assert engine.ENGINE_TYPE.value == "Steam"
    assert engine.CAPACITY == 900

def test_fuel_tank():
    tank = FuelTank()
    assert tank.MASS == 100
    assert tank.ROLE.value == "Fuel Tank"
    assert tank.CAPACITY == 900

def test_oxylite_tank():
    tank = OxyliteTank()
    assert tank.MASS == 100
    assert tank.ROLE.value == "Oxidizer Tank"
    assert tank.CAPACITY == 2700
    assert tank.RESOURCE_TYPE.value == "Oxidizer"
    assert tank.OXI_TYPE == OxidizerType.OXYLITE

def test_liq_oxy_tank():
    tank = LiquidOxygenTank()
    assert tank.MASS == 100
    assert tank.ROLE.value == "Oxidizer Tank"
    assert tank.CAPACITY == 2700
    assert tank.RESOURCE_TYPE.value == "Oxidizer"
    assert tank.OXI_TYPE == OxidizerType.LOX

def test_research_mod():
    module = ResearchModule()
    assert module.MASS == 200
    assert module.ROLE.value == "Extra Module"

def test_cargo_bay():
    cargo = CargoBay()
    assert cargo.MASS == 2000
    assert cargo.ROLE.value == "Extra Module"
    assert cargo.CARGO_TYPE.value == "Solid"

def test_liquid_cargo_tank():
    tank = LiquidCargoTank()
    assert tank.MASS == 1000
    assert tank.ROLE.value == "Extra Module"
    assert tank.CARGO_TYPE.value == "Liquid"

def test_gas_cargo_canister():
    canister = GasCargoCanister()
    assert canister.MASS == 1000
    assert canister.ROLE.value == "Extra Module"
    assert canister.CARGO_TYPE.value == "Gas"

def test_biological_cargo_bay():
    cargo = BiologicalCargoBay()
    assert cargo.MASS == 1000
    assert cargo.ROLE.value == "Extra Module"
    assert cargo.CARGO_TYPE.value == "Biological"

def test_sightseeing_module():
    module = Sightseeing()
    assert module.MASS == 200
    assert module.ROLE.value == "Extra Module"

def test_thruster():
    module = Thruster()
    assert module.MASS == 1000
    assert module.ROLE.value == "Solid Fuel Thruster"
