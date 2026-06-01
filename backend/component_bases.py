"""Rocket Component Bases and Rules"""
# filename: component_bases.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from enum import Enum
from abc import ABC

# ------------------------------------------------------------------
# 2. Building Block Enums
# ------------------------------------------------------------------
class ModuleRole(Enum):
    COMMAND = "Command Capsule"
    ENGINE = "Engine"
    THRUSTER = "Solid Fuel Thruster"
    TANK = "Fuel or Oxidizer Tank"
    FUEL_TANK = "Fuel Tank"
    OXI_TANK = "Oxidizer Tank"
    EXTRA = "Extra Module"

class EngineType(Enum):
    STEAM = "Steam"
    PETROL = "Petrol"
    HYDROGEN = "Liquid Hydrogen"
    BIODIESEL = "Biodiesel"

class EngineEfficiency(Enum):
    STEAM = 20
    PETROL = 40
    HYDROGEN = 60
    BIODIESEL = 40
    THRUSTER = 30

class OxidizerType(Enum):
    OXYLITE = "OXYLITE" # "Solid Oxylite"
    LOX = "LOX" # "Liquid Oxygen"

OxidizerEfficiency: dict[OxidizerType, float] = {
    OxidizerType.OXYLITE: 1.0,
    OxidizerType.LOX: 1.33,
}

class ResourceType(Enum):
    FUEL = "Fuel" 
    OXIDIZER = "Oxidizer"

class CargoType(Enum):
    BIO = "Biological"
    SOLID = "Solid"
    LIQUID = "Liquid"
    GAS = "Gas"

# ------------------------------------------------------------------
# 3. Base Components: Parent Classes.
#   Usable rocket components reside in components.py
# ------------------------------------------------------------------
# Base Component
class Component(ABC):
    KEY: str
    ONLYONE: bool = False
    MASS: int
    ROLE: ModuleRole
    DISPLAY_NAME: str = "Component"
    def __str__(self) -> str:
        return self.DISPLAY_NAME
    
# Base Command
class BaseCommand(Component, ABC):
    ROLE: ModuleRole = ModuleRole.COMMAND

# Base Engine
class Engine(Component, ABC):
    ENGINE_TYPE: EngineType
    EFFICIENCY: float
    ROLE: ModuleRole = ModuleRole.ENGINE
    USE_INTERNAL_FUEL: bool
    DISPLAY_NAME: str = "Engine"

class InternalFuelEngine(Engine, ABC):
    CAPACITY: int = 900
    USE_INTERNAL_FUEL: bool = True

class ExternalFuelEngine(Engine, ABC):
    USE_INTERNAL_FUEL: bool = False

# Base Fuel Tank
class Tank(Component, ABC):
    RESOURCE_TYPE: ResourceType
    MASS: int = 100
    CAPACITY: int
    ROLE: ModuleRole = ModuleRole.FUEL_TANK

class BaseFuelTank(Tank, ABC):
    RESOURCE_TYPE: ResourceType = ResourceType.FUEL
    MASS: int = 100
    CAPACITY: int

#Base Oxidizer Tank
class OxidizerTank(Tank, ABC):
    OXI_TYPE: OxidizerType
    RESOURCE_TYPE: ResourceType = ResourceType.OXIDIZER
    MASS: int = 100
    CAPACITY: int = 2700 # Max Fuel
    ROLE: ModuleRole = ModuleRole.OXI_TANK
    DISPLAY_NAME: str = "Oxidizer Tank"

class ExtraModule(Component, ABC):
    ROLE: ModuleRole = ModuleRole.EXTRA

class CargoModule(ExtraModule, ABC):
    CARGO_TYPE: CargoType
    DISPLAY_NAME: str = "Cargo Module"

class BaseThruster(Component, ABC):
    EFFICIENCY: float
    ROLE: ModuleRole = ModuleRole.THRUSTER
    CAPACITY: int = 0