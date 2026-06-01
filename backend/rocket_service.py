"""Service Layer for ONI Rocket Calculator"""
# filename: rocket_service.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from component_bases import OxidizerType
from component_registry import registry
from config import MAX_EXTRA_MODULE_COUNT, MAX_FUEL_TANKS, MAX_OXI_TANKS, MAX_THRUSTERS
from rocket import Rocket
from rocket_configurator import configure_rocket_for_range
from schema import ComponentMetaData, EngineMetaData, TankMetaData

# ------------------------------------------------------------------
# 2. Rocket Service
# ------------------------------------------------------------------
class RocketService:
    def supply_rocket_components(self):
        pass
    
    def supply_constants(self) -> dict[str, int]:
        return {
            "MAX_THRUSTERS": MAX_THRUSTERS,
            "MAX_FUEL_TANKS": MAX_FUEL_TANKS,
            "MAX_EXTRA_MODULE_COUNT": MAX_EXTRA_MODULE_COUNT,
            "MAX_OXI_TANKS": MAX_OXI_TANKS
        }

    def supply_commands(self) -> list[ComponentMetaData]:
        return registry.list_commands_metadata()
    
    def supply_engines(self) -> list[EngineMetaData]:
        return registry.list_engines_metadata()
    
    def supply_fuel_tanks(self) -> list[TankMetaData]:
        return registry.list_fuel_tanks_metadata()

    def supply_oxidizer_tanks(self) -> list[TankMetaData]:
        return registry.list_oxidizer_tanks_metadata()
    
    def supply_extra_modules(self) -> list[ComponentMetaData]:
        return registry.list_extra_modules_metadata()

    def supply_thrusters(self) -> list[ComponentMetaData]:
        return registry.list_thrusters_metadata()
    
    def configure_rocket_for_range(self, rocket: Rocket, desired_range: float, oxidizer: OxidizerType | None) -> Rocket:
        return configure_rocket_for_range(rocket, desired_range, oxidizer)
    
    def calculate_range(self, rocket: Rocket) -> float:
        return rocket.calculate_range()