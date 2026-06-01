"""Engine Subsystem of Rockets"""
# filename: engine_system.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from component_bases import BaseThruster, Engine, InternalFuelEngine
from component_registry import registry
from components import Thruster
from exceptions import InvalidAmountError, LimitExceededError, NoModulesError, CapacityError, WrongEngineTypeError, NotAnEngineError
from config import MAX_THRUSTERS

# ------------------------------------------------------------------
# 2. Thruster System to be edited/implemented later
# ------------------------------------------------------------------
FULL_THRUSTER_FUEL = Thruster.CAPACITY #400

# ------------------------------------------------------------------
# 3. Engine System Class
# ------------------------------------------------------------------

class EngineSystem:
    def __init__(self) -> None:
        self._engine: type[Engine] | None = None
        self._thruster: dict[type[BaseThruster], int] = {thruster: 0 for thruster in registry.list_thrusters()}
        self._fuel: float = 0

    @property
    def engine(self) -> type[Engine] | None:
        return self._engine

    def set_engine(self, engine: type[Engine] | None) -> None:
        if engine is None:
            self._engine = None
            self._fuel = 0
            return
        if not isinstance(engine, type) or not issubclass(engine, Engine):
            raise NotAnEngineError("The Engine must be classified as an Engine in Rocket Components list")
        if not engine.USE_INTERNAL_FUEL:
            self._fuel = 0
        self._engine = engine

    def remove_engine(self) -> None:
        self._fuel = 0
        self._engine = None

    @property
    def uses_internal_fuel(self) -> bool:
        return (
            self.engine is not None
            and self.engine.USE_INTERNAL_FUEL
        )

    @property
    def capacity(self) -> int:
        if self._engine is None:
            return 0
        elif issubclass(self._engine, InternalFuelEngine):
            return self._engine.CAPACITY
        else:
            return 0

    @property
    def fuel(self) -> float:
        return self._fuel
        
    def set_fuel(self, amount: float) -> None:
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise InvalidAmountError("Fuel must take a valid integer")
        if amount < 0:
            raise InvalidAmountError("Fuel value must be either 0 or positive")
        if not self.uses_internal_fuel:
            raise WrongEngineTypeError("Wrong type of Engine. Only Steam Engine can store fuel")
        if amount > self.capacity:
            raise CapacityError("Not Enough Capacity")
        self._fuel = amount

    @property
    def thruster_count(self) -> int:
        return sum(self._thruster.values())

    # Thrusters are assumed full
    @property
    def mass(self) -> float:
        mass = self._engine.MASS if self._engine else 0
        for thruster in self._thruster:
            mass += thruster.MASS * self._thruster[thruster]
        mass += self.fuel
        return mass

    @property
    def extra_thrust(self) -> float:
        thrust = 0
        for thruster in self._thruster:
            thrust += self._thruster[thruster] * thruster.EFFICIENCY * FULL_THRUSTER_FUEL # Hardcoded thruster as full, should be worked on later.
        return thrust
    
    def add_thruster(self, thruster: type[BaseThruster] = Thruster) -> None:
        if self.thruster_count >= MAX_THRUSTERS:
            raise LimitExceededError("No point in adding this many thrusters")
        self._thruster[thruster] += 1

    def remove_thruster(self, thruster: type[BaseThruster]) -> None:
        if self._thruster[thruster] <= 0:
            raise NoModulesError("Rocket has no thrusters to remove")
        self._thruster[thruster] -= 1