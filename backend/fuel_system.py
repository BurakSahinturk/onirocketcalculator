"""Fuel Subsystem of Rockets"""
# filename: fuel_system.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from dataclasses import dataclass

from component_bases import BaseFuelTank, OxidizerTank, OxidizerType, ResourceType, Tank
from components import FuelTank, LiquidOxygenTank, OxyliteTank
from component_registry import registry
from exceptions import (
    InvalidAmountError, 
    NoModulesError, 
    CapacityError,
    LimitExceededError,
    WrongModuleTypeError
)
from config import MAX_FUEL_TANKS, MAX_OXI_TANKS

# ------------------------------------------------------------------
# 2. Validators
# ------------------------------------------------------------------
def validate_amount(amount: float) -> float:
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise InvalidAmountError("Fuel must take a valid integer")
    if amount < 0:
        raise InvalidAmountError("Fuel value must be either 0 or positive")
    return amount

# ------------------------------------------------------------------
# 3. Helper / Data Classes
# ------------------------------------------------------------------
@dataclass
class FuelData:
    tank_count: int = 0
    fuel_amount:float = 0
    capacity_per_tank: int = 0

    @property
    def capacity(self) -> int:
        return self.tank_count * self.capacity_per_tank
# ------------------------------------------------------------------
# 4. Fuel System Class
# ------------------------------------------------------------------
class FuelSystem:
    def __init__(self) -> None:
        self._tanks: dict[type[Tank], FuelData] = {
            tank: FuelData(capacity_per_tank=tank.CAPACITY) for tank in registry.list_tanks()
        }

    @property
    def tanks_data(self) -> dict[type[Tank], FuelData]:
        return self._tanks

    @property
    def mass(self) -> float:
        mass = 0
        for tank, tank_recipe in self._tanks.items():
            mass += tank.MASS * tank_recipe.tank_count
            mass += tank_recipe.fuel_amount
        return mass
    
    @property
    def fuel_amount(self) -> float:
        fuel = 0.0
        for tank in self._tanks:
            if tank.RESOURCE_TYPE == ResourceType.FUEL:
                fuel += self._tanks[tank].fuel_amount
        return fuel
    
    @property
    def oxylite_amount(self) -> float:
        oxy = 0.0
        for tank in self._tanks:
            if issubclass(tank, OxidizerTank):
                if tank.OXI_TYPE == OxidizerType.OXYLITE:
                    oxy += self._tanks[tank].fuel_amount
        return oxy
    
    @property
    def lox_amount(self) -> float:
        lox = 0.0
        for tank in self._tanks:
            if issubclass(tank, LiquidOxygenTank):
                if tank.OXI_TYPE == OxidizerType.LOX:
                    lox += self._tanks[tank].fuel_amount
        return lox

    def add_tank(self, tank_type: type[Tank]):
        if issubclass(tank_type, BaseFuelTank):
            max_allowed = MAX_FUEL_TANKS
        elif issubclass(tank_type, OxidizerTank):
            max_allowed = MAX_OXI_TANKS
        else:
            raise WrongModuleTypeError(f"{tank_type} is an unknown tank type")
        if self._tanks[tank_type].tank_count >= max_allowed:
            raise LimitExceededError("No point of adding this many tanks")
        self._tanks[tank_type].tank_count += 1

    def remove_tank(self, tank_type: type[Tank]):
        if not issubclass(tank_type, BaseFuelTank) and not issubclass(tank_type, OxidizerTank):
            raise WrongModuleTypeError(f"{tank_type} is an unknown tank type")
        if self._tanks[tank_type].tank_count <= 0:
            raise NoModulesError("No fuel tanks to remove")
        self._tanks[tank_type].tank_count -= 1
        # Empty excess fuel
        if self._tanks[tank_type].capacity < self._tanks[tank_type].fuel_amount:
            self._tanks[tank_type].fuel_amount = self._tanks[tank_type].capacity

    def add_fuel_tank(self) -> None:
        self.add_tank(FuelTank)
    
    def remove_fuel_tank(self) -> None:
        self.remove_tank(FuelTank)
    
    def add_oxylite_tank(self) -> None:
        self.add_tank(OxyliteTank)

    def remove_oxylite_tank(self) -> None:
        self.remove_tank(OxyliteTank)
    
    def add_lox_tank(self) -> None:
        self.add_tank(LiquidOxygenTank)

    def remove_lox_tank(self) -> None:
        self.remove_tank(LiquidOxygenTank)

    @property
    def fuel_capacity(self) -> int:
        return self._tanks[FuelTank].capacity
    
    @property
    def oxylite_capacity(self) -> int:
        return self._tanks[OxyliteTank].capacity
    
    @property
    def lox_capacity(self) -> int:
        return self._tanks[LiquidOxygenTank].capacity

    def reset_fuel_system(self) -> None:
        for tank in self._tanks:
            self._tanks[tank].fuel_amount = 0
            self._tanks[tank].tank_count = 0

    def set_fuel_by_tank(self, tank_type: type[Tank], amount: float) -> None:
        amount = validate_amount(amount)        
        if amount > self._tanks[tank_type].capacity:
            raise CapacityError("Not enough capacity")
        self._tanks[tank_type].fuel_amount = amount

    def set_fuel(self, amount: float) -> None:
        amount = validate_amount(amount)
        if amount > self._tanks[FuelTank].capacity:
            raise CapacityError("Not enough capacity")
        self._tanks[FuelTank].fuel_amount = amount

    def set_oxylite(self, amount: float) -> None:
        amount = validate_amount(amount)
        if amount > self._tanks[OxyliteTank].capacity:
            raise CapacityError("Not enough capacity")
        self._tanks[OxyliteTank].fuel_amount = amount

    def set_lox(self, amount: float) -> None:
        amount = validate_amount(amount)
        if amount > self._tanks[LiquidOxygenTank].capacity:
            raise CapacityError("Not Enough Capacity")
        self._tanks[LiquidOxygenTank].fuel_amount = amount