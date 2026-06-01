"""Central registry of all rocket components.
Provides string-to-class lookup and reverse lookup,
grouped listings for the API, and validation.
"""
# filename: component_registry.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from typing import Mapping, Any, Sequence
from component_bases import BaseCommand, BaseFuelTank, BaseThruster, Component, Engine, ExtraModule, InternalFuelEngine, ModuleRole, Tank, OxidizerTank

from exceptions import UnknownComponentError
from schema import ComponentMetaData, EngineMetaData, TankMetaData

# ------------------------------------------------------------------
# 2. The registry class
# ------------------------------------------------------------------
class ComponentRegistry:
    """
    Single source of truth for all known rocket parts.
    Maps the external key (the SHORT_NAME class attribute) to the class itself.
    """

    def __init__(self) -> None:
        self._command: dict[str, type[BaseCommand]] = {}
        self._engines: dict[str, type[Engine]] = {}
        self._fuel_tanks: dict[str, type[BaseFuelTank]] = {}
        self._oxidizer_tanks: dict[str, type[OxidizerTank]] = {}
        self._extra_modules: dict[str, type[ExtraModule]] = {}
        self._thrusters: dict[str, type[BaseThruster]] = {}

    # --------------------------------------------------------------
    # 3. Register
    # --------------------------------------------------------------
    def _universal_register(self, cls: type[Component], target_dict: dict[str, Any], category_name: str):
        if not hasattr(cls, "KEY") or not cls.KEY:
            raise UnknownComponentError(f"Class {cls.__name__} must define a valid string 'KEY' attribute.")
        if cls.KEY in target_dict:
            raise ValueError(f"Component '{cls}' already registered.")
        # I'm not so sure about adding in two 
        target_dict[cls.KEY] = cls
    
    # --------------------------------------------------------------
    # 4. Decorators
    # --------------------------------------------------------------
    def command(self, cls: type[BaseCommand]) -> type[BaseCommand]:
        self._universal_register(cls, self._command, "Command")
        return cls

    def engine(self, cls: type[Engine]) -> type[Engine]:
        if not issubclass(cls, Engine):
            raise TypeError(f"{cls.__name__} is not an Engine subclass.")
        self._universal_register(cls, self._engines, "Engine")
        return cls

    def fuel_tank(self, cls: type[BaseFuelTank]) -> type[BaseFuelTank]:
        if cls.ROLE != ModuleRole.FUEL_TANK:
            raise TypeError(f"{cls.__name__} does not have role FUEL_TANK.")
        self._universal_register(cls, self._fuel_tanks, "Fuel Tank")
        return cls

    def oxidizer_tank(self, cls: type[OxidizerTank]) -> type[OxidizerTank]:
        if cls.ROLE != ModuleRole.OXI_TANK:
            raise TypeError(f"{cls.__name__} does not have role OXI_TANK.")
        self._universal_register(cls, self._oxidizer_tanks, "Oxidizer Tank")
        return cls

    def extra_module(self, cls: type[ExtraModule]) -> type[ExtraModule]:
        if cls.ROLE != ModuleRole.EXTRA:
            raise TypeError(f"{cls.__name__} is not an extra module.")
        self._universal_register(cls, self._extra_modules, "Extra Module")
        return cls

    def thruster(self, cls: type[BaseThruster]) -> type[BaseThruster]:
        if cls.ROLE != ModuleRole.THRUSTER:
            raise TypeError(f"{cls.__name__} is not a Thruster.")
        self._universal_register(cls, self._thrusters, "Thruster")
        return cls

    # --------------------------------------------------------------
    # 5. Public lookup methods
    # --------------------------------------------------------------
    def get_command(self, key: str) -> type[BaseCommand]:
        """Return the command capsule class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._command[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown command capsule: '{key}'")


    def get_engine(self, key: str) -> type[Engine]:
        """Return the engine class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._engines[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown engine: '{key}'")

    def get_fuel_tank(self, key: str) -> type[BaseFuelTank]:
        """Return the fuel tank class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._fuel_tanks[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown fuel tank: '{key}'")

    def get_oxidizer_tank(self, key: str) -> type[OxidizerTank]:
        """Return the oxidizer tank class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._oxidizer_tanks[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown oxidizer tank: '{key}'")

    def get_tank(self, key: str) -> type[Tank]:
        """Return the fuel or oxidizer tank class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._fuel_tanks[key]
        except KeyError:
            try:
                return self._oxidizer_tanks[key]
            except KeyError:
                raise UnknownComponentError(f"Unknown oxidizer tank: '{key}'")

    def get_extra_module(self, key: str) -> type[ExtraModule]:
        """Return the module class for the given external key and makes sure it has role of 'Extra Module'
        Raises UnknownComponentError if not found.
        """
        try:
            return self._extra_modules[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown extra module: '{key}'")

    def get_thruster(self, key: str) -> type[BaseThruster]:
        """Return the thruster class for the given external key.
        Raises UnknownComponentError if not found.
        """
        try:
            return self._thrusters[key]
        except KeyError:
            raise UnknownComponentError(f"Unknown thruster: '{key}'")

    # --------------------------------------------------------------
    # 6. Reverse lookup – class → key
    # --------------------------------------------------------------
    def get_key(self, cls: type[Component]) -> str:
        """Return the external key for a component class.
        Useful when writing a Rocket back to a DTO.
        """
        # Search in all dictionaries; exactly one should contain it.
        for mapping in (self._command, self._engines, self._fuel_tanks, self._oxidizer_tanks,
                        self._extra_modules, self._thrusters):
            for key, registered_cls in mapping.items():
                if registered_cls is cls:
                    return key
        raise UnknownComponentError(f"No key registered for class {cls.__name__}")

    # --------------------------------------------------------------
    # 7. Listing methods – return classes for domain
    # --------------------------------------------------------------
    def list_commands(self) -> list[type[Component]]:
        return list(self._command.values())
    
    def list_engines(self) -> list[type[Engine]]:
        return list(self._engines.values())
    
    def list_fuel_tanks(self) -> list[type[BaseFuelTank]]:
        return list(self._fuel_tanks.values())
    
    def list_oxidizer_tanks(self) -> list[type[OxidizerTank]]:
        return list(self._oxidizer_tanks.values())

    def list_tanks(self) -> Sequence[type[Tank]]:
        return self.list_fuel_tanks() + self.list_oxidizer_tanks()
    
    def list_extra_modules(self) -> list[type[ExtraModule]]:
        return list(self._extra_modules.values())
    
    def list_thrusters(self) -> list[type[BaseThruster]]:
        return list(self._thrusters.values())
    
    def list_all_modules(self) -> Sequence[type[Component]]:
        all_modules: Sequence[type[Component]] = []
        all_modules.extend(self.list_commands())
        all_modules.extend(self.list_engines())
        all_modules.extend(self.list_tanks())
        all_modules.extend(self.list_extra_modules())
        all_modules.extend(self.list_thrusters())
        return all_modules

    # --------------------------------------------------------------
    # 8. Listing methods – return metadata for frontend
    # --------------------------------------------------------------
    def list_commands_metadata(self) -> list[ComponentMetaData]:
        return self._build_metadata(self._command)
    
    def list_engines_metadata(self) -> list[EngineMetaData]:
        return self._build_engine_metadata(self._engines)

    def list_fuel_tanks_metadata(self) -> list[TankMetaData]:
        return self._build_tank_metadata(self._fuel_tanks)

    def list_oxidizer_tanks_metadata(self) -> list[TankMetaData]:
        return self._build_tank_metadata(self._oxidizer_tanks)
    
    def list_tanks_metadata(self) -> list[TankMetaData]:
        return self.list_fuel_tanks_metadata() + self.list_oxidizer_tanks_metadata()
    
    def list_extra_modules_metadata(self) -> list[ComponentMetaData]:
        return self._build_metadata(self._extra_modules)

    def list_thrusters_metadata(self) -> list[ComponentMetaData]:
        return self._build_metadata(self._thrusters)

    def all_metadata(self) -> dict[str, Sequence[ComponentMetaData]]:
        """Return a dict of all grouped metadata, e.g. for the /reference-data endpoint."""
        return {
            "commands":       self.list_commands_metadata(),
            "engines":        self.list_engines_metadata(),
            "fuel_tanks":     self.list_fuel_tanks_metadata(),
            "oxidizer_tanks": self.list_oxidizer_tanks_metadata(),
            "extra_modules":  self.list_extra_modules_metadata(),
            "thrusters":      self.list_thrusters_metadata(),
        }

    # ----- internal helpers -----
    def _build_metadata(self, mapping: Mapping[str, type[Component]]) -> list[ComponentMetaData]:
        """Turn a component map into a list of descriptions."""
        result = []
        for key, cls in mapping.items():
            result.append(ComponentMetaData(
                key=key,
                display_name=cls.DISPLAY_NAME,
                mass=cls.MASS))
        return result
    
    def _build_engine_metadata(self, mapping: Mapping[str, type[Engine]]) -> list[EngineMetaData]:
        """Turn an engine map into a list of descriptions."""
        result = []
        for key, cls in mapping.items():
            result.append(EngineMetaData(
                key=key,
                display_name=cls.DISPLAY_NAME,
                mass=cls.MASS,
                capacity= cls.CAPACITY if issubclass(cls, InternalFuelEngine) else None,
                uses_internal_fuel=True if issubclass(cls, InternalFuelEngine) else False
            ))
        return result
    
    def _build_tank_metadata(self, mapping: Mapping[str, type[Tank]]) -> list[TankMetaData]:
        result = []
        for key, cls in mapping.items():
            result.append(TankMetaData(
                key=key,
                display_name=cls.DISPLAY_NAME,
                mass=cls.MASS,
                resource_type=cls.RESOURCE_TYPE.value,
                capacity=cls.CAPACITY
            ))
        return result

# ------------------------------------------------------------------
# 9. Module‑level singleton
# ------------------------------------------------------------------
# Create one instance that the whole app can import
registry = ComponentRegistry()