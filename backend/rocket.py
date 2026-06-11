"""Rocket Class Definition"""
# filename: rocket.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from component_bases import Engine, OxidizerType, OxidizerEfficiency
from engine_system import EngineSystem
from fuel_system import FuelSystem
from modules_system import ModuleSystem
from config import weight_penalty_formula
# ------------------------------------------------------------------
# 2. Main Rocket Class
# ------------------------------------------------------------------
class Rocket:
    def __init__(self) -> None:
        self._engine = EngineSystem()
        self._fuel = FuelSystem()
        self._modules = ModuleSystem()

    # --------------------------------------------------------------
    # 2.1 Exposing Subsystems
    # --------------------------------------------------------------
    @property
    def fuel_system(self) -> FuelSystem:
        return self._fuel
    
    @property
    def engine(self) -> type[Engine] | None:
        return self._engine.engine
    
    @property
    def engine_system(self) -> EngineSystem:
        return self._engine

    @property
    def modules(self) -> ModuleSystem:
        return self._modules


    # --------------------------------------------------------------
    # 2.2 Fuel Methods
    # --------------------------------------------------------------
    @property
    def fuel_capacity(self) -> int:
        if self._engine.uses_internal_fuel:
            return self._engine.capacity
        return self._fuel.fuel_capacity
    
    @property
    def oxylite_capacity(self) -> int:
        return self._fuel.oxylite_capacity
    
    @property
    def lox_capacity(self) -> int:
        return self._fuel.lox_capacity
    
    @property
    def oxidizer_capacity(self) -> int:
        return self.oxylite_capacity + self.lox_capacity

    def set_fuel(self, amount: float) -> None:
        if self._engine.uses_internal_fuel:
            self._engine.set_fuel(amount)
        else:
            self._fuel.set_fuel(amount)

    def set_oxylite(self, amount: float) -> None:
        self._fuel.set_oxylite(amount)
    
    def set_lox(self, amount: float) -> None:
        self._fuel.set_lox(amount)
    
    @property
    def fuel_amount(self) -> float:
        if self._engine.uses_internal_fuel:
            return self._engine.fuel
        else:
            return self._fuel.fuel_amount

    # --------------------------------------------------------------
    # 2.3 Data required for range calculation
    # --------------------------------------------------------------
    @property
    def total_mass(self) -> float:
        return self._engine.mass + self._fuel.mass + self._modules.mass
    
    @property
    def base_distance(self) -> float:
        """Calculated based on engine efficiency, amound of fuel, amound of oxidizer and oxidizer type efficiency."""
        # No Engine -> No Thrust
        if self.engine is None:
            return 0
        
        # Steam Engine -> Steam Engine Handles its own fuel
        # Formula: fuel * engine efficiency
        if self._engine.uses_internal_fuel:
            return self._engine.fuel * self.engine.EFFICIENCY
        
        # Other Engines -> Fuel and Oxidizer is required, taken from Fuel System
        # Formula: fuel * engine efficiency * oxidizer efficiency, an amount of oxidizer equal to amount of fuel must be present
        remaining_fuel = self.fuel_system.fuel_amount
        oxylite_amount = self._fuel.oxylite_amount
        lox_amount = self._fuel.lox_amount
        distance = 0
        eng_eff = self.engine.EFFICIENCY
        
        # Uses LOX first - high efficiency
        lox_burnt_fuel = min(remaining_fuel, lox_amount)
        distance += lox_burnt_fuel * OxidizerEfficiency[OxidizerType.LOX] * eng_eff
        remaining_fuel -= lox_burnt_fuel

        # Uses Solid Oxylite next - low efficiency
        sox_burnt_fuel = min(remaining_fuel, oxylite_amount)
        distance += sox_burnt_fuel * OxidizerEfficiency[OxidizerType.OXYLITE] * eng_eff
        remaining_fuel -= sox_burnt_fuel

        return distance    

    @property
    def weight_penalty(self) -> float:
        """Weight penalty is based on total mass. Formula is from ONI forum"""
        mass = self.total_mass
        return weight_penalty_formula(mass) 
    
    def calculate_range(self) -> float:
        """Formula: Propulsion + Extra Thrust - Weight Penalty
        Propulsion, named base_distance, is derived from engine type, fuel amount, oxidizer type and amount.
        Extra Thrust comes from Thrusters, stored in engine subsystem.
        Weight Penalty is calculated based on mass.
        """
        if self.engine is None:
            return 0
        base_distance = self.base_distance
        weight_penalty = self.weight_penalty
        extra_thrust = self._engine.extra_thrust
        return max(0, (base_distance - weight_penalty + extra_thrust))