"""End user Rocket Modules"""
# filename: components.py


# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from component_bases import BaseCommand, BaseFuelTank, BaseThruster, CargoModule, CargoType, Component, EngineEfficiency, EngineType, ExternalFuelEngine, InternalFuelEngine, ModuleRole, OxidizerTank, OxidizerType, ExtraModule
from component_registry import registry

# ------------------------------------------------------------------
# 2. Command Capsule
# ------------------------------------------------------------------
@registry.command
class CommandCapsule(BaseCommand):
    KEY: str = "command"
    ONLYONE: bool = True
    MASS: int = 200
    DISPLAY_NAME: str = "Command Capsule"


# ------------------------------------------------------------------
# 3. Engines
# ------------------------------------------------------------------
@registry.engine
class BiodieselEngine(ExternalFuelEngine):
    KEY: str = "bio_engine"
    ONLYONE: bool = True
    ENGINE_TYPE: EngineType = EngineType.BIODIESEL
    MASS: int = 200
    EFFICIENCY: float = EngineEfficiency.BIODIESEL.value
    DISPLAY_NAME: str = "Biodiesel Engine"

@registry.engine
class HydrogenEngine(ExternalFuelEngine):
    KEY: str = "h2_engine"
    ONLYONE: bool = True
    ENGINE_TYPE: EngineType = EngineType.HYDROGEN
    MASS: int = 500
    EFFICIENCY: float = EngineEfficiency.HYDROGEN.value
    DISPLAY_NAME: str = "Hydrogen Engine"
    
@registry.engine
class PetroleumEngine(ExternalFuelEngine):
    KEY: str = "petrol_engine"
    ONLYONE: bool = True
    ENGINE_TYPE: EngineType = EngineType.PETROL
    MASS: int = 200
    EFFICIENCY: float = EngineEfficiency.PETROL.value
    DISPLAY_NAME: str = "Petroleum Engine"

@registry.engine
class SteamEngine(InternalFuelEngine):
    KEY: str = "steam_engine"
    ONLYONE: bool = True
    CAPACITY: int = 900
    ENGINE_TYPE: EngineType = EngineType.STEAM
    MASS: int = 2000
    EFFICIENCY: float = EngineEfficiency.STEAM.value
    USE_INTERNAL_FUEL = True
    DISPLAY_NAME: str = "Steam Engine"

# ------------------------------------------------------------------
# 4. Fuel Tanks
# ------------------------------------------------------------------
@registry.fuel_tank
class FuelTank(BaseFuelTank):
    KEY: str = "fuel_tank"
    CAPACITY: int = 900
    MASS: int = 100
    DISPLAY_NAME: str = "Fuel Tank"

# Oxidizer Tanks
@registry.oxidizer_tank
class LiquidOxygenTank(OxidizerTank):
    KEY: str = "lox_tank"
    OXI_TYPE: OxidizerType = OxidizerType.LOX
    DISPLAY_NAME: str = "Liquid Oxygen Tank"

@registry.oxidizer_tank
class OxyliteTank(OxidizerTank):
    KEY: str = "oxylite_tank"
    OXI_TYPE: OxidizerType = OxidizerType.OXYLITE
    DISPLAY_NAME: str = "Oxylite Tank"


# ------------------------------------------------------------------
# 5. Additional Modules
# ------------------------------------------------------------------
@registry.extra_module
class BiologicalCargoBay(CargoModule):
    KEY: str = "bio_cargo"
    MASS: int = 1000
    CARGO_TYPE: CargoType = CargoType.BIO
    DISPLAY_NAME: str = "Biological Cargo Bay"


@registry.extra_module
class LiquidCargoTank(CargoModule):
    KEY: str = "liquid_cargo"
    CARGO_TYPE: CargoType = CargoType.LIQUID
    MASS: int = 1000
    DISPLAY_NAME: str = "Liquid Cargo Tank"

@registry.extra_module
class CargoBay(CargoModule): #It's called so in the game, but this is the solid cargo tank
    KEY: str = "solid_cargo"
    CARGO_TYPE: CargoType = CargoType.SOLID
    MASS: int = 2000
    DISPLAY_NAME: str = "Cargo Bay (Solid)"

@registry.extra_module
class GasCargoCanister(CargoModule):
    KEY: str = "gas_cargo"
    CARGO_TYPE: CargoType = CargoType.GAS
    MASS: int = 1000
    DISPLAY_NAME: str = "Gas Cargo Bay"

@registry.extra_module
class ResearchModule(ExtraModule):
    KEY: str = "research"
    MASS: int = 200
    DISPLAY_NAME: str = "Research Module"

@registry.extra_module
class Sightseeing(ExtraModule):
    KEY: str = "sightseeing"
    MASS: int = 200
    DISPLAY_NAME: str = "Sightseeing Module"


# ------------------------------------------------------------------
# 6. Thruster -assumed full-
# ------------------------------------------------------------------
@registry.thruster
class Thruster(BaseThruster):
    KEY: str = "thruster"
    MASS: int = 1000 #dry_mass: 200 + oxylite: 400 + iron: 400
    EFFICIENCY: float = EngineEfficiency.THRUSTER.value
    DISPLAY_NAME: str = "Solid Fuel Thruster"
    CAPACITY: int = 400