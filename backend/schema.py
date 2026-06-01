"""Pydantic Schemas"""
# filename: schema.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------

from pydantic import BaseModel, Field
from component_bases import OxidizerType

class ComponentMetaData(BaseModel):
    key: str
    display_name: str
    mass: int

class EngineMetaData(ComponentMetaData):
    capacity: int | None
    uses_internal_fuel: bool

class TankMetaData(ComponentMetaData):
    resource_type: str
    capacity: int

class EngineRecipe(BaseModel):
    engine: str | None
    thrusters: int = 0
    internal_fuel: float = 0
    internal_capacity: int = 0

class FuelDTO(BaseModel):
    tank_count: int = 0
    fuel_amount: float = 0

class RocketRecipe(BaseModel):
    engine_system: EngineRecipe
    fuel_system: dict[str, FuelDTO] = Field(default_factory=dict)
    modules: dict[str, int] = Field(default_factory=dict)

class ConfigurationRequest(BaseModel):
    rocket_recipe: RocketRecipe
    desired_range: float
    oxidizer: OxidizerType | None

class ReferenceData(BaseModel):
    constants: dict[str, int]
    commands: list[ComponentMetaData]
    engines: list[EngineMetaData]
    fuel_tanks: list[TankMetaData]
    oxidizer_tanks: list[TankMetaData]
    extra_modules: list[ComponentMetaData]
    thrusters: list[ComponentMetaData]